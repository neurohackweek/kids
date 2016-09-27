library(data.table)
library(dplyr)
library(tidyr)
library(ggplot2)

cvFiles <- data.table(file=dir('./cv_output/', pattern='*TestAcc.csv', full.names = TRUE)) 
cvFiles <- cvFiles[, TestAcc:=fread(file), by=file]
cvFiles <- cvFiles[, c('cvMethod', 'classifier', 'mt', 'n', 'i'):=tstrsplit(tstrsplit(file, '/')[[4]], '_(mt|n|i)*')]

cvFiles <- cvFiles[, mt:=factor(mt, levels=seq(5, 50, 5))]
cvFiles <- cvFiles[, n:=factor(n, levels=seq(30, 100, 10))]

summaryCV <- cvFiles[, as.list(quantile(TestAcc, probs=c(.05, .5, .95))), keyby=c('mt', 'n')]

N_labels <- paste0('N = ', levels(cvFiles$n))
names(N_labels) <- levels(cvFiles$n)

#+ fig.width=10, fig.height=6
ggplot(cvFiles, aes(x=mt, y=TestAcc))+
	geom_point(alpha=.05, position=position_jitter(w=1, h=.1))+
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
ggplot(cvFiles, aes(x=n, y=TestAcc, group=mt, color=mt))+
	geom_point(alpha=.025, position=position_jitter(width=.5, height=.1))+
	geom_errorbar(data=summaryCV, aes(x=n, y=NULL, ymin=`5%`, ymax=`95%`),
		   width=.1, alpha=.25)+
	geom_point(data=summaryCV, aes(x=n, y=`50%`))+
	geom_line(aes(group=mt, color=mt), stat='smooth', method='loess', alpha=.75)+ 
	theme(panel.background=element_rect(fill='white'))+
	labs(x='Sample Size', y='Predictive Accuracy (ASD Dx)',
	     color='Motion\nThreshold')
