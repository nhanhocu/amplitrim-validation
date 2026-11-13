# Usage: Rscript raw_merge_refused.R READS_DIR truncF truncR eeF eeR OUT_DIR
# Do the reads of the pairs that DADA2's mergePairs refuses merge with vsearch, as AmpliTrim merges them for its yield estimate?
# Filters as DADA2 does (truncQ 2, maxN 0), learns one error model per read direction over all samples (HDP has one flow cell), denoises, merges
# (minOverlap 12, maxMismatch 0), then traces every filtered read pair to its denoised pair: lost in denoising, merged, or refused. Refused pairs are
# classed by the overlap of their two denoised sequences (close: 12 nt or more with at most 10% mismatches; poor: 12 nt or more with more; none),
# and flagged when both halves also merged with other partners in the same sample. Writes OUT_DIR/merged_asvs.tsv (each sample's merged sequences), OUT_DIR/refused_R1/R2.fastq and merged_R1/R2.fastq
# (the filtered reads, names carrying sample, class and flag), then runs vsearch on both sets with AmpliTrim's two settings:
# tolerant (--fastq_minovlen 12 --fastq_allowmergestagger, vsearch's default limits on differences) and strict (the same with --fastq_maxdiffs 0).
suppressMessages({library(dada2); library(ShortRead)}); a <- commandArgs(TRUE); out <- a[6]; dir.create(out, showWarnings = FALSE, recursive = TRUE)
fn1 <- sort(list.files(a[1], "_R1\\.fastq\\.gz$", full.names = TRUE)); fn2 <- sub("_R1\\.fastq", "_R2.fastq", fn1)
d <- file.path(out, "filtered"); dir.create(d, showWarnings = FALSE); f1 <- file.path(d, basename(fn1)); f2 <- file.path(d, basename(fn2))
suppressWarnings(filterAndTrim(fn1, f1, fn2, f2, truncLen = as.integer(a[2:3]), maxN = 0, maxEE = as.numeric(a[4:5]), truncQ = 2, compress = TRUE, multithread = 2))
keep <- file.exists(f1) & file.exists(f2); f1 <- f1[keep]; f2 <- f2[keep]
eF <- suppressMessages(learnErrors(f1, multithread = 2, verbose = FALSE)); eR <- suppressMessages(learnErrors(f2, multithread = 2, verbose = FALSE))
best_overlap <- function(f, r) {   # lowest share of mismatches over overlaps of 12 nt or more between the end of f and the start of r
  nf <- nchar(f); best <- c(0, 1)
  for (o in 12:min(nf, nchar(r))) { mm <- sum(strsplit(substr(f, nf - o + 1, nf), "")[[1]] != strsplit(substr(r, 1, o), "")[[1]])
    if (mm / o < best[2]) best <- c(o, mm / o) }
  best }
fq <- list(refused_R1 = list(), refused_R2 = list(), merged_R1 = list(), merged_R2 = list()); counts <- list(); asvs <- list()
for (k in seq_along(f1)) {
  s <- sub("_R1.*", "", basename(f1[k]))
  drF <- derepFastq(f1[k]); drR <- derepFastq(f2[k])
  dF <- dada(drF, err = eF, multithread = 2, verbose = FALSE); dR <- dada(drR, err = eR, multithread = 2, verbose = FALSE)
  m <- mergePairs(dF, drF, dR, drR, minOverlap = 12, maxMismatch = 0, returnRejects = TRUE)
  rf <- dF$map[drF$map]; rr <- dR$map[drR$map]
  key <- paste(rf, rr); mkey <- paste(m$forward, m$reverse)
  st <- ifelse(is.na(rf) | is.na(rr), "lost", ifelse(m$accept[match(key, mkey)], "merged", "refused"))
  accF <- unique(m$forward[m$accept]); accR <- unique(m$reverse[m$accept])
  cls <- rep(NA_character_, length(st)); both <- rep(NA, length(st))
  for (j in which(!m$accept)) {
    b <- best_overlap(dF$sequence[m$forward[j]], rc(dR$sequence[m$reverse[j]]))
    c <- if (b[1] == 0) "none" else if (b[2] <= 0.1) "close" else "poor"
    idx <- which(key == mkey[j]); cls[idx] <- c; both[idx] <- (m$forward[j] %in% accF) && (m$reverse[j] %in% accR) }
  r1 <- readFastq(f1[k]); r2 <- readFastq(f2[k])
  for (w in c("refused", "merged")) { i <- which(st == w); if (!length(i)) next
    tag <- if (w == "refused") paste0(";cls=", cls[i], ";both=", as.integer(both[i])) else ""
    nm <- BStringSet(paste0(s, "_", i, tag))
    fq[[paste0(w, "_R1")]][[k]] <- ShortReadQ(sread(r1)[i], quality(r1)[i], nm)
    fq[[paste0(w, "_R2")]][[k]] <- ShortReadQ(sread(r2)[i], quality(r2)[i], nm) }
  asvs[[k]] <- data.frame(sample = s, sequence = m$sequence[m$accept], abundance = m$abundance[m$accept])
  counts[[k]] <- data.frame(sample = s, filtered = length(st), lost = sum(st == "lost"), merged = sum(st == "merged"), refused = sum(st == "refused"))
}
for (n in names(fq)) { p <- file.path(out, paste0(n, ".fastq")); if (file.exists(p)) file.remove(p)
  for (x in fq[[n]]) if (!is.null(x)) writeFastq(x, p, mode = "a", compress = FALSE) }
write.table(do.call(rbind, asvs), file.path(out, "merged_asvs.tsv"), sep = "	", quote = FALSE, row.names = FALSE)
write.table(do.call(rbind, counts), file.path(out, "trace_counts.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
for (w in c("refused", "merged")) for (set in c("tolerant", "strict")) {
  args <- c("--fastq_mergepairs", file.path(out, paste0(w, "_R1.fastq")), "--reverse", file.path(out, paste0(w, "_R2.fastq")),
            "--fastaout", file.path(out, sprintf("%s.%s.merged.fasta", w, set)), "--fastq_minovlen", "12", "--fastq_allowmergestagger",
            "--threads", "2", "--log", file.path(out, sprintf("%s.%s.vsearch.log", w, set)), "--quiet")
  if (set == "strict") args <- c(args, "--fastq_maxdiffs", "0")
  system2("vsearch", args) }
unlink(d, recursive = TRUE)
