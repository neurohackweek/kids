#'
#' # Understanding QC parameters
#'

library(ggplot2)
#check how percent and mean fd are related:
aDF <- read.csv('../../Phenotypic_V1_0b_preprocessed1.csv')
aplot <- ggplot(aDF, aes(y=func_mean_fd, x=func_perc_fd))+
	geom_point(alpha=.3)+
	geom_smooth()
print(aplot)


qplot(aDF$func_perc_fd)

summary(glm(round(func_perc_fd) ~ AGE_AT_SCAN, family='quasipoisson', data=aDF))

ggplot(aDF, aes(x=(AGE_AT_SCAN), y=round(func_perc_fd)))+
    geom_point()+
    geom_smooth(method='glm', method.args=list(family='quasipoisson'))

#'
#' The percentage of volumes with motion > threshold is basically
#' a count variable (normalized), so we should treat it as something
#' like poisson distributed (most people have only a few, bounded at
#' 0, but some people have a lot). We can predict the rate of bad
#' volumes with age and find a small decrease in the expected rate with age.
#' This is as expected. All this taken together can give us confidence
#' that we are interpreting this measure correctly.
#'
#'
#' #Data checking
#'

#+ "load-data"

rsqDF <- read.csv('./RESULTS/SummaryRsqs.csv', stringsAsFactors=F)

head(rsqDF) 

#+ "freq_check"
#Check frequencies and distributions
table(rsqDF$motion_thresh)
table(rsqDF$n)
table(rsqDF$age_l-rsqDF$age_u)
table(rsqDF[,c('motion_thresh', 'n')])
table(rsqDF[,c('age_l', 'n')])
table(rsqDF[,c('motion_thresh', 'age_l')])

ggplot(rsqDF, aes(x=med_rsq))+geom_histogram(aes(y=..density..))+geom_density()

#'
#' # $R^2$ plots
#'
#+ "fun_plots"
#Plot the fun stuff

n_color_age_facet <- ggplot(rsqDF, aes(x=motion_thresh, y=med_rsq, group=(n), color=(n)))+
	geom_errorbar(aes(ymin=med_rsq-CI_95/2, 
			  ymax=med_rsq+CI_95/2), 
		      width=0, alpha=.6)+
	facet_wrap(~age_l)+
	coord_cartesian(y=c(.5, 1))+
	scale_color_gradient(low='gray', high='darkblue')

age_color_n_facet <- ggplot(rsqDF, aes(x=motion_thresh, y=med_rsq, group=factor(age_l), color=factor(age_l)))+
	geom_errorbar(aes(ymin=med_rsq-CI_95/2, 
			  ymax=med_rsq+CI_95/2), 
		      width=0, alpha=.2)+
	coord_cartesian(y=c(.8, 1))+
	facet_wrap(~n)

plotThing <- function(aPlot){
	aPlot + 
		geom_point(alpha=.2)+
		geom_line(alpha=.5)+
		scale_x_continuous(trans='identity')+
		scale_y_continuous(trans='identity')
}

plotThing(n_color_age_facet)

plotThing(age_color_n_facet)

#'
#' # ICC plots
#' 

ggplot(rsqDF, aes(x=med_icc))+geom_histogram(aes(y=..density..))+geom_density()

#+ "fun_plots2"
#Plot the fun stuff

n_color_age_facet <- ggplot(rsqDF, aes(x=motion_thresh, y=med_icc, group=(n), color=(n)))+
	geom_errorbar(aes(ymin=med_icc-CI_95_icc/2, 
			  ymax=med_icc+CI_95_icc/2), 
		      width=0, alpha=.6)+
	facet_wrap(~age_l)+
	coord_cartesian(y=c(.5, 1))+
	scale_color_gradient(low='darkgray', high='darkblue')

age_color_n_facet <- ggplot(rsqDF, aes(x=motion_thresh, y=med_icc, group=factor(age_l), color=factor(age_l)))+
	geom_errorbar(aes(ymin=med_icc-CI_95_icc/2, 
			  ymax=med_icc+CI_95_icc/2), 
		      width=0, alpha=.5)+
	coord_cartesian(y=c(.8, 1))+
	facet_wrap(~n)

plotThing <- function(aPlot){
	aPlot + 
		geom_point(alpha=.5)+
		geom_line(alpha=.5)+
		scale_x_continuous(trans='identity')+
		scale_y_continuous(trans='identity')
}

plotThing(n_color_age_facet)

plotThing(age_color_n_facet)


#'
#' # Within motion cutoffs
#'

within_cutoff_plot <- ggplot(rsqDF, aes(x=n, y=med_icc, group=motion_thresh, color=motion_thresh))+
	geom_errorbar(aes(ymin=med_icc-CI_95_icc/2, 
			  ymax=med_icc+CI_95_icc/2), 
		      width=0, alpha=.5)+
	coord_cartesian(y=c(.8, 1))+
	facet_wrap(~age_l)
plotThing(within_cutoff_plot) 
