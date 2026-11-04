# One DADA2 run of the long-read truth test (longread_truth.py): one condition, on the files of one library type.
#   Rscript truth_dada2.R <file with one FASTQ path per line> <output prefix> <maxEE> <minLen> <maxLen or Inf> <BAND_SIZE> <pool: TRUE, FALSE or pseudo> <threads>
#                         <error function: PacBioErrfun, or binned:<the quality values, comma separated>> [<forward primer> <reverse primer as ordered>]
# With the two primers, DADA2's own removePrimers (its defaults, orient = TRUE) is run first on the files; without them the files are taken as already cut between the primers.
# Then: filterAndTrim with ONLY maxEE and the length window acting (no truncation, minQ 0, maxN 0, no PhiX removal), learnErrors with the chosen error function
# (PacBioErrfun needs the quality score 93 and falls back to standard fitting without it; makeBinnedQualErrfun is for binned scores such as those of Revio),
# dada, makeSequenceTable and removeBimeraDenovo (consensus). Writes <prefix>_filter.tsv (sample, reads_in, reads_out) and
# <prefix>_asv.tsv (sequence, chimera = flagged by removeBimeraDenovo, and one column of read counts per sample).
suppressMessages(library(dada2))
a <- commandArgs(TRUE)
files <- readLines(a[1])
prefix <- a[2]
ee <- as.numeric(a[3])
minLen <- as.numeric(a[4])
maxLen <- as.numeric(a[5])
band <- as.integer(a[6])
pool <- a[7]
threads <- as.integer(a[8])
errarg <- a[9]
mt <- threads != 1
errfun <- if (errarg == "PacBioErrfun") {
  PacBioErrfun
} else if (startsWith(errarg, "binned:")) {
  if (!exists("makeBinnedQualErrfun")) stop("This DADA2 has no makeBinnedQualErrfun: update DADA2.")
  makeBinnedQualErrfun(as.integer(strsplit(sub("binned:", "", errarg), ",")[[1]]))
} else stop(paste("Unknown error function:", errarg))
tmp <- file.path(tempdir(), "truth")
dir.create(tmp, showWarnings = FALSE, recursive = TRUE)
samples <- sub("\\.fastq(\\.gz)?$", "", basename(files))

if (length(a) >= 11 && nzchar(a[10])) {
  trimmed <- file.path(tmp, paste0(samples, "_primers.fastq.gz"))
  suppressWarnings(removePrimers(files, trimmed, primer.fwd = a[10], primer.rev = dada2:::rc(a[11]), orient = TRUE, verbose = FALSE))
  files <- trimmed[file.exists(trimmed)]
  samples <- sub("_primers\\.fastq\\.gz$", "", basename(files))
}

filt <- file.path(tmp, paste0(samples, "_filt.fastq.gz"))
res <- suppressWarnings(filterAndTrim(files, filt, maxEE = ee, truncQ = 0, minQ = 0, maxN = 0, minLen = minLen, maxLen = maxLen,
                                      rm.phix = FALSE, compress = TRUE, multithread = FALSE))
write.table(data.frame(sample = samples, reads_in = res[, 1], reads_out = res[, 2]), paste0(prefix, "_filter.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
keep <- file.exists(filt) & res[, 2] > 0
if (!any(keep)) stop("No read passed the filter.")
filt <- filt[keep]
names(filt) <- samples[keep]

err <- learnErrors(filt, errorEstimationFunction = errfun, BAND_SIZE = band, multithread = mt, verbose = FALSE)
dd <- dada(filt, err = err, BAND_SIZE = band, pool = if (pool == "TRUE") TRUE else if (pool == "FALSE") FALSE else pool, multithread = mt, verbose = FALSE)
if (inherits(dd, "dada")) dd <- list(dd)
names(dd) <- names(filt)
st <- makeSequenceTable(dd)
nochim <- removeBimeraDenovo(st, method = "consensus", multithread = mt, verbose = FALSE)
flag <- !(colnames(st) %in% colnames(nochim))
tab <- data.frame(sequence = colnames(st), chimera = flag, t(st), check.names = FALSE, stringsAsFactors = FALSE)
write.table(tab, paste0(prefix, "_asv.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
