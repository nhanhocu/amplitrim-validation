# Where pairs are lost at one setting. Usage: Rscript merge_breakdown.R READS_DIR truncF truncR eeF eeR LABEL OUT_TSV
# Columns: refused_mismatch = an overlap of 12 nt or more with 1 to 10% mismatches between the denoised sequences (refused_with_1mismatch and
# refused_with_2to3 split it); refused_short_overlap = no overlap of 12 nt or more with at most 10% mismatches (too short, or too many mismatches);
# refused_indel is not measured here (always 0); refused_other = an exact overlap that DADA2 still refused.
suppressMessages(library(dada2)); a <- commandArgs(TRUE); tl <- as.integer(a[2:3]); ee <- as.numeric(a[4:5]); set.seed(20261106)
fn1 <- sort(list.files(a[1], "_R1\\.fastq\\.gz$", full.names=TRUE)); fn2 <- sub("_R1\\.fastq","_R2.fastq",fn1); nm <- sub("_R1.*","",basename(fn1))
d <- tempfile("filt"); dir.create(d); f1 <- file.path(d,basename(fn1)); f2 <- file.path(d,basename(fn2))
out <- suppressWarnings(filterAndTrim(fn1,f1,fn2,f2,truncLen=tl,maxN=0,maxEE=ee,truncQ=2,rm.phix=FALSE,compress=TRUE,multithread=2))
keep <- file.exists(f1)&file.exists(f2)
flow <- vapply(fn1,function(f){h<-readLines(gzfile(f),1); p<-strsplit(strsplit(h," ")[[1]][2],":")[[1]]; if(length(p)>2) p[3] else "NA"},"")
rows <- list()
for (fc in unique(flow[keep])) { i <- which(keep & flow==fc)
  eF <- suppressMessages(learnErrors(f1[i],multithread=2,verbose=FALSE)); eR <- suppressMessages(learnErrors(f2[i],multithread=2,verbose=FALSE))
  dF <- suppressMessages(dada(f1[i],err=eF,multithread=2,verbose=FALSE)); dR <- suppressMessages(dada(f2[i],err=eR,multithread=2,verbose=FALSE))
  if(length(i)==1){dF<-list(dF);dR<-list(dR)}
  for (k in seq_along(i)) {
    m <- mergePairs(dF[[k]], f1[i[k]], dR[[k]], f2[i[k]], minOverlap=12, maxMismatch=0, returnRejects=TRUE, verbose=FALSE)
    acc <- m$accept
    # DADA2 reports a refused pair with nmatch 0 whatever the reason, so the overlap is measured here from the two denoised sequences:
    # the overlap length (12 nt or more) with the fewest mismatches between the end of the forward and the start of the reverse complement.
    fs <- dF[[k]]$sequence; rs <- dR[[k]]$sequence
    best <- t(vapply(which(!acc), function(j) { f <- fs[m$forward[j]]; r <- rc(rs[m$reverse[j]]); nf <- nchar(f)
      fv <- strsplit(f, "")[[1]]; rv <- strsplit(r, "")[[1]]
      o <- 12:min(nf, length(rv)); mm <- vapply(o, function(x) sum(fv[(nf - x + 1):nf] != rv[1:x]), 0)
      i <- which.min(mm / o); c(o[i], mm[i]) }, c(0, 0)))
    ovl <- rep(NA, nrow(m)); mmc <- rep(NA, nrow(m)); if (any(!acc)) { ovl[!acc] <- best[, 1]; mmc[!acc] <- best[, 2] }
    found <- !acc & !is.na(mmc) & mmc / ovl <= 0.1          # an overlap with at most 10% mismatches exists
    mis <- found & mmc > 0; short <- !acc & !found; ind <- rep(FALSE, nrow(m)); oth <- !acc & found & mmc == 0
    ov <- ifelse(acc, m$nmatch + m$nmismatch + m$nindel, ovl)
    rows[[length(rows)+1]] <- data.frame(label=a[6], sample=nm[i[k]], flowcell=fc, input=out[i[k],1], passed_filter=out[i[k],2],
      paired_after_denoise=sum(m$abundance), merged=sum(m$abundance[acc]), refused_short_overlap=sum(m$abundance[short]),
      refused_mismatch=sum(m$abundance[mis]), refused_indel=sum(m$abundance[ind]), refused_other=sum(m$abundance[oth]),
      refused_with_1mismatch=sum(m$abundance[mis & mmc==1]), refused_with_2to3=sum(m$abundance[mis & mmc %in% 2:3]),
      median_overlap_refused=if(any(!acc)) median(rep(ov[!acc], m$abundance[!acc])) else NA, median_overlap_merged=if(any(acc)) median(rep(ov[acc], m$abundance[acc])) else NA)
  } }
r <- do.call(rbind, rows); write.table(r, a[7], sep="\t", quote=FALSE, row.names=FALSE)
s <- colSums(r[, 4:13]); cat(sprintf("%s per 100 input: filter fail %.1f, lost denoising %.1f, merged %.1f, refused short %.1f, mismatch %.1f, indel %.1f, other %.1f\n", a[6],
  100*(s["input"]-s["passed_filter"])/s["input"], 100*(s["passed_filter"]-s["paired_after_denoise"])/s["input"], 100*s["merged"]/s["input"],
  100*s["refused_short_overlap"]/s["input"], 100*s["refused_mismatch"]/s["input"], 100*s["refused_indel"]/s["input"], 100*s["refused_other"]/s["input"]))
