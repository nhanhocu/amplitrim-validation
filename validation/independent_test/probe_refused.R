# What are the refused pairs with no acceptable end-to-end overlap? Usage: Rscript probe_refused.R READS_DIR truncF truncR eeF eeR N_SAMPLES OUT_TSV
# For each refused pair, an overlap alignment (end gaps free, so overhangs and indels are allowed) of the denoised forward sequence and the reverse complement
# of the denoised reverse sequence, and the amplicon length it implies.
# Also writes OUT_TSV with _accepted.tsv in place of .tsv: the forward and reverse sequence numbers of every pair that merged, per sample.
suppressMessages({library(dada2); library(Biostrings); library(pwalign)}); a <- commandArgs(TRUE); set.seed(20261106)
fn1 <- sort(list.files(a[1], "_R1\\.fastq\\.gz$", full.names=TRUE))[seq_len(as.integer(a[6]))]; fn2 <- sub("_R1\\.fastq","_R2.fastq",fn1)
d <- tempfile(); dir.create(d); f1 <- file.path(d,basename(fn1)); f2 <- file.path(d,basename(fn2))
suppressWarnings(filterAndTrim(fn1,f1,fn2,f2,truncLen=as.integer(a[2:3]),maxN=0,maxEE=as.numeric(a[4:5]),truncQ=2,compress=TRUE,multithread=2))
eF <- suppressMessages(learnErrors(f1,multithread=2,verbose=FALSE)); eR <- suppressMessages(learnErrors(f2,multithread=2,verbose=FALSE))
dF <- suppressMessages(dada(f1,err=eF,multithread=2,verbose=FALSE)); dR <- suppressMessages(dada(f2,err=eR,multithread=2,verbose=FALSE))
sm <- pwalign::nucleotideSubstitutionMatrix(match = 1, mismatch = -2, baseOnly = TRUE)
rows <- list(); acc_rows <- list()
for (k in seq_along(f1)) {
  m <- mergePairs(dF[[k]], f1[k], dR[[k]], f2[k], minOverlap=12, maxMismatch=0, returnRejects=TRUE, verbose=FALSE)
  fs <- dF[[k]]$sequence; rs <- dR[[k]]$sequence
  acc_rows[[k]] <- data.frame(sample=sub("_R1.*","",basename(f1[k])), forward=m$forward[m$accept], reverse=m$reverse[m$accept], abundance=m$abundance[m$accept])
  for (j in which(!m$accept)) {
    f <- fs[m$forward[j]]; r <- rc(rs[m$reverse[j]])
    al <- pwalign::pairwiseAlignment(DNAString(r), DNAString(f), type = "overlap", substitutionMatrix = sm, gapOpening = 5, gapExtension = 2)
    p <- as.character(alignedPattern(al)); s <- as.character(alignedSubject(al)); L <- nchar(p)
    mm <- sum(strsplit(p, "")[[1]] != strsplit(s, "")[[1]] & strsplit(p, "")[[1]] != "-" & strsplit(s, "")[[1]] != "-")
    gaps <- sum(strsplit(p, "")[[1]] == "-") + sum(strsplit(s, "")[[1]] == "-")
    fst <- start(subject(al)); rst <- start(pattern(al))     # where the overlap starts in the forward read, and in the reverse complement
    amp <- if (rst == 1) fst - 1 + nchar(r) else NA            # the reverse complement starts inside the forward read: the amplicon length
    rows[[length(rows)+1]] <- data.frame(sample=sub("_R1.*","",basename(f1[k])), abundance=m$abundance[j], f_len=nchar(f), r_len=nchar(r),
      forward=m$forward[j], reverse=m$reverse[j], aln_len=L, mismatches=mm, gaps=gaps, f_start=fst, r_start=rst, amplicon=amp, score=score(al), fseq=f, rseq=r)
  } }
r <- do.call(rbind, rows); write.table(r, a[7], sep="\t", quote=FALSE, row.names=FALSE)
write.table(do.call(rbind, acc_rows), sub(".tsv", "_accepted.tsv", a[7], fixed=TRUE), sep="\t", quote=FALSE, row.names=FALSE)
r$cls <- with(r, ifelse(aln_len < 12, "no overlap of 12 nt", ifelse(gaps > 0 & (mismatches + gaps) / aln_len <= 0.1, "indel", ifelse(mismatches / aln_len <= 0.1,
  ifelse(!is.na(amplicon) & amplicon < f_len, "overhang (amplicon shorter than the forward read)", "mismatches"), "no good overlap"))))
print(aggregate(abundance ~ cls, r, sum))
cat("refused reads", sum(r$abundance), "\n")
ng <- r[r$cls %in% c("no good overlap", "no overlap of 12 nt"), ]; ng <- ng[order(-ng$abundance), ]
print(head(ng[, c("sample","abundance","f_len","r_len","aln_len","mismatches","gaps","f_start","r_start","amplicon")], 12))
