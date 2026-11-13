# Usage: Rscript dada2_arm.R READS_DIR truncF truncR eeF eeR OUT_PREFIX
suppressMessages(library(dada2)); a <- commandArgs(TRUE)
tl <- as.integer(a[2:3]); ee <- as.numeric(a[4:5]); pre <- a[6]; set.seed(20261106)
fn1 <- sort(list.files(a[1], "_R1\\.fastq\\.gz$", full.names=TRUE)); fn2 <- sub("_R1\\.fastq","_R2.fastq",fn1); nm <- sub("_R1.*","",basename(fn1))
d <- tempfile("filt"); dir.create(d); f1 <- file.path(d,basename(fn1)); f2 <- file.path(d,basename(fn2))
out <- suppressWarnings(filterAndTrim(fn1,f1,fn2,f2,truncLen=tl,maxN=0,maxEE=ee,truncQ=2,rm.phix=FALSE,compress=TRUE,multithread=2))
keep <- file.exists(f1)&file.exists(f2)
flow <- vapply(fn1,function(f){h<-readLines(gzfile(f),1); p<-strsplit(strsplit(h," ")[[1]][2],":")[[1]]; if(length(p)>2) p[3] else "NA"},"")
tracks <- list(); merged_all <- list()
for (fc in unique(flow[keep])) { i <- which(keep & flow==fc)
  eF <- suppressMessages(learnErrors(f1[i],multithread=2,verbose=FALSE)); eR <- suppressMessages(learnErrors(f2[i],multithread=2,verbose=FALSE))
  dF <- suppressMessages(dada(f1[i],err=eF,multithread=2,verbose=FALSE)); dR <- suppressMessages(dada(f2[i],err=eR,multithread=2,verbose=FALSE))
  if(length(i)==1){dF<-list(dF);dR<-list(dR)}
  mg <- mergePairs(dF,f1[i],dR,f2[i],minOverlap=12,maxMismatch=0,verbose=FALSE); if(is.data.frame(mg)) mg<-list(mg)
  names(mg) <- nm[i]; merged_all <- c(merged_all,mg)
  tracks[[fc]] <- data.frame(sample=nm[i],flowcell=fc,denoised_f=vapply(dF,function(x)sum(getUniques(x)),0),denoised_r=vapply(dR,function(x)sum(getUniques(x)),0),merged=vapply(mg,function(m)sum(m$abundance),0))
  saveRDS(list(eF=eF,eR=eR),paste0(pre,"_err_",fc,".rds")) }
tab <- makeSequenceTable(merged_all); nc <- removeBimeraDenovo(tab,method="consensus",multithread=2,verbose=FALSE)
tr <- do.call(rbind,tracks); tr$input <- out[match(tr$sample,nm),1]; tr$filtered <- out[match(tr$sample,nm),2]; tr$nonchim <- rowSums(nc)[tr$sample]
write.table(tr,paste0(pre,"_track.tsv"),sep="\t",quote=FALSE,row.names=FALSE)
write.table(nc,paste0(pre,"_seqtab.tsv"),sep="\t",quote=FALSE)
cat(sprintf("%s pass=%.4f merged=%.4f nonchim=%.4f asvs=%d flowcells=%d\n",basename(pre),sum(tr$filtered)/sum(tr$input),sum(tr$merged)/sum(tr$input),sum(tr$nonchim)/sum(tr$input),ncol(nc),length(tracks)))
