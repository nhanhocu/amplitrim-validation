# Usage: Rscript export_err.R RUN_DIR OUT_DIR
# Exports the DADA2 error models of arm D (one .rds per flow cell, written by dada2_arm.R)
# as tables of substitution rate by quality score, for sim_reads.py (mode tq).
a <- commandArgs(TRUE); dir.create(a[2], showWarnings = FALSE, recursive = TRUE)
for (x in Sys.glob(file.path(a[1], "D_err_*.rds"))) {
  fc <- sub("D_err_", "", sub(".rds", "", basename(x), fixed = TRUE), fixed = TRUE); e <- readRDS(x)
  for (d in c("eF", "eR")) { m <- dada2::getErrors(e[[d]])
    df <- data.frame(trans = rep(rownames(m), ncol(m)), q = rep(as.integer(colnames(m)), each = nrow(m)), rate = as.vector(m))
    write.table(df, file.path(a[2], sprintf("%s_%s.tsv", fc, d)), sep = "\t", quote = FALSE, row.names = FALSE) } }
