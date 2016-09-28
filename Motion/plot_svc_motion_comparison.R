library(data.table)
library(dplyr)
library(tidyr)
library(ggplot2)

#Remember to extract the files from TestAcc.tar.gz first
cvFiles <- dir('./cv_output/sss_svc_run2', pattern='*_TestAcc.csv', full.names = TRUE) 
lst <- lapply(cvFiles, fread)
cvData <- rbindlist(lst)
cvData[,'file'] <- cvFiles
cvData <- cvData[, c('cvMethod', 'classifier', 'mt', 'n', 'i'):=tstrsplit(tstrsplit(file, '/')[[4]], '_(mt|n|i)*')]

setnames(cvData, 'V1', 'TestAcc')

cvData <- cvData[, mt:=factor(mt, levels=seq(2, 50, 2))]
cvData <- cvData[, n:=factor(n, levels=seq(30, 100, 10))]

summaryCV <- cvData[, as.list(quantile(TestAcc, probs=c(.05, .5, .95))), keyby=c('mt', 'n')]

N_labels <- paste0('N = ', levels(cvData$n))
names(N_labels) <- levels(cvData$n)

#+ fig.width=10, fig.height=6
ggplot(cvData, aes(x=mt, y=TestAcc))+
	geom_point(alpha=.01, position=position_jitter(w=.2, h=.1))+
	geom_line(aes(group=n), stat='smooth', method='loess', 
		  position=position_dodge(w=1))+
	geom_point(data=summaryCV, aes(x=mt, y=`50%`),
		   position=position_dodge(w=1))+
	geom_errorbar(data=summaryCV, aes(x=mt, y=NULL, ymin=`5%`, ymax=`95%`),
		   position=position_dodge(w=1), width=0)+
	facet_wrap(~n, nrow=2, labeller=labeller(n=N_labels))+
	theme(panel.background=element_rect(fill='white'))+
	labs(x='Motion Threshold', y='Predictive Accuracy (ASD Dx)')


#+ fig.width=6, fig.height=6
ggplot(cvData, aes(x=n, y=TestAcc, group=mt, color=mt))+
	geom_point(alpha=.0, position=position_jitter(width=.5, height=.1))+
	geom_errorbar(data=summaryCV, aes(x=n, y=NULL, ymin=`5%`, ymax=`95%`),
		   width=2, alpha=.5, position=position_dodge(w=0))+
	geom_point(data=summaryCV, aes(x=n, y=`50%`), position=position_dodge(w=0))+
	geom_line(aes(group=mt, color=mt), stat='smooth', method='loess', alpha=.5)+ 
	theme(panel.background=element_rect(fill='white'))+
	labs(x='Sample Size', y='Predictive Accuracy (ASD Dx)',
	     color='Motion\nThreshold')
