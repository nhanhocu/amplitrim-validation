# ITS follow-up: DADA2 on a folder of paired FASTQs (optionally with truncLen), then mergePairs on the SAME denoised reads at several mismatch limits.
# At the default limit (the first one, which must be 0) the rejected pairs are counted by reason and written pair by pair, with the length of their overlap.
# Writes two tables:
#   <sample table>: one row per sample (counts of read pairs): sample, input, filtered, reach (pairs of denoised sequences that enter the merge step),
#     rej_short (the alignment of the pair, matches + mismatches + indels, is shorter than minOverlap), rej_mismatch (the alignment is long enough and has a mismatch
#     or an indel, including a pair that has fewer than minOverlap matching bases only because of its mismatches), rej_other (a clean overlap that is still refused),
#     and for every limit k: merged_k<k> (pairs merged) and asv_k<k> (distinct merged sequences holding at least 0.1% of the merged pairs of the sample)
#   <pair table>: one row per distinct pair of denoised sequences at the default limit: sample, forward and reverse (the numbers of the two denoised sequences
#     within the sample), abundance, accept, nmatch, nmismatch, nindel
#   <sequence table>: the merged sequences at every limit: sample, k, sequence, abundance (pairs that merge into that sequence)
# Usage: Rscript its_followup.R <input_dir> <minLen> <maxEE> <minOverlap> <truncF> <truncR> <limits, e.g. 0,1,2,5> <sample table> <pair table> <sequence table>
#   truncF and truncR of 0 mean no truncation (the ITS setting). Part of TEST_REGISTER.md (the section for this follow-up).
suppressMessages(library(dada2))
a <- commandArgs(TRUE)
in_dir <- a[1]; min_len <- as.integer(a[2]); max_ee <- as.numeric(a[3]); min_ov <- as.integer(a[4])
trunc_f <- as.integer(a[5]); trunc_r <- as.integer(a[6]); limits <- as.integer(strsplit(a[7], ",")[[1]])
sample_path <- a[8]; pair_path <- a[9]; seq_path <- a[10]
stopifnot(length(limits) >= 1, limits[1] == 0L)
fn1 <- sort(list.files(in_dir, pattern = "_R1.*\\.f(ast)?q(\\.gz)?$", full.names = TRUE))
fn2 <- sort(list.files(in_dir, pattern = "_R2.*\\.f(ast)?q(\\.gz)?$", full.names = TRUE))
d <- file.path(tempdir(), "filt"); dir.create(d)
f1 <- file.path(d, basename(fn1)); f2 <- file.path(d, basename(fn2))
out <- suppressWarnings(filterAndTrim(fn1, f1, fn2, f2, truncLen = c(trunc_f, trunc_r), maxN = 0, maxEE = c(max_ee, max_ee), truncQ = 2, minLen = min_len,
                                      rm.phix = FALSE, compress = TRUE))
keep <- file.exists(f1) & file.exists(f2); idx <- which(keep)
eF <- suppressMessages(learnErrors(f1[keep], verbose = FALSE)); eR <- suppressMessages(learnErrors(f2[keep], verbose = FALSE))
dF <- suppressMessages(dada(f1[keep], err = eF, pool = FALSE, verbose = FALSE)); dR <- suppressMessages(dada(f2[keep], err = eR, pool = FALSE, verbose = FALSE))
as_frames <- function(m) if (is.data.frame(m)) list(m) else m
merge_at <- function(k) as_frames(suppressMessages(mergePairs(dF, f1[keep], dR, f2[keep], minOverlap = min_ov, maxMismatch = k, returnRejects = TRUE,
                                                              trimOverhang = FALSE, verbose = FALSE)))
merged <- lapply(limits, merge_at)
empty <- c(reach = 0, merged = 0, rej_short = 0, rej_mismatch = 0, rej_other = 0, asv = 0)
summarise <- function(m) {
  if (is.null(m) || nrow(m) == 0) return(empty)
  acc <- m$accept; aligned <- m$nmatch + m$nmismatch + m$nindel; short <- !acc & aligned < min_ov; mism <- !acc & !short & (m$nmismatch > 0 | m$nindel > 0); other <- !acc & !short & !mism
  total <- sum(m$abundance[acc])
  asv <- if (total > 0) sum(tapply(m$abundance[acc], as.character(m$sequence[acc]), sum) >= 0.001 * total) else 0
  c(reach = sum(m$abundance), merged = total, rej_short = sum(m$abundance[short]), rej_mismatch = sum(m$abundance[mism]), rej_other = sum(m$abundance[other]), asv = asv)
}
rows <- lapply(seq_along(fn1), function(i) {
  j <- match(i, idx)
  per_limit <- lapply(seq_along(limits), function(l) if (is.na(j)) empty else summarise(merged[[l]][[j]]))
  base <- per_limit[[1]]
  row <- data.frame(sample = sub("_R1.*$", "", basename(fn1[i])), input = out[i, 1], filtered = out[i, 2], reach = base[["reach"]], rej_short = base[["rej_short"]],
                    rej_mismatch = base[["rej_mismatch"]], rej_other = base[["rej_other"]], row.names = NULL)
  for (l in seq_along(limits)) {
    row[[paste0("merged_k", limits[l])]] <- per_limit[[l]][["merged"]]
    row[[paste0("asv_k", limits[l])]] <- per_limit[[l]][["asv"]]
  }
  row
})
tab <- do.call(rbind, rows)
write.table(tab, sample_path, sep = "\t", quote = FALSE, row.names = FALSE)
pairs <- lapply(seq_along(fn1), function(i) {
  j <- match(i, idx)
  if (is.na(j)) return(NULL)
  m <- merged[[1]][[j]]
  if (is.null(m) || nrow(m) == 0) return(NULL)
  data.frame(sample = sub("_R1.*$", "", basename(fn1[i])), forward = m$forward, reverse = m$reverse, abundance = m$abundance, accept = m$accept, nmatch = m$nmatch,
             nmismatch = m$nmismatch, nindel = m$nindel, row.names = NULL)
})
pairs <- do.call(rbind, pairs)
if (is.null(pairs)) pairs <- data.frame(sample = character(0), forward = numeric(0), reverse = numeric(0), abundance = numeric(0), accept = logical(0), nmatch = numeric(0), nmismatch = numeric(0),
                                                                  nindel = numeric(0))
write.table(pairs, pair_path, sep = "\t", quote = FALSE, row.names = FALSE)
seqs <- lapply(seq_along(limits), function(l) lapply(seq_along(fn1), function(i) {
  j <- match(i, idx)
  if (is.na(j)) return(NULL)
  m <- merged[[l]][[j]]
  if (is.null(m) || nrow(m) == 0) return(NULL)
  m <- m[m$accept, , drop = FALSE]
  if (nrow(m) == 0) return(NULL)
  s <- tapply(m$abundance, as.character(m$sequence), sum)
  data.frame(sample = sub("_R1.*$", "", basename(fn1[i])), k = limits[l], sequence = names(s), abundance = as.numeric(s), row.names = NULL)
}))
seqs <- do.call(rbind, unlist(seqs, recursive = FALSE))
if (is.null(seqs)) seqs <- data.frame(sample = character(0), k = integer(0), sequence = character(0), abundance = numeric(0))
write.table(seqs, seq_path, sep = "\t", quote = FALSE, row.names = FALSE)
cat(sprintf("%d samples, %d input pairs, %d merged at limit 0\n", nrow(tab), sum(tab$input), sum(tab$merged_k0)))
