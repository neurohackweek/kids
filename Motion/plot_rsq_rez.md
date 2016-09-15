    library(ggplot2)
    #check how percent and mean fd are related:
    aDF <- read.csv('../../Phenotypic_V1_0b_preprocessed1.csv')
    aplot <- ggplot(aDF, aes(y=func_mean_fd, x=func_perc_fd))+
        geom_point(alpha=.3)+
        geom_smooth()
    print(aplot)

    ## Warning: Removed 13 rows containing non-finite values (stat_smooth).

    ## Warning: Removed 13 rows containing missing values (geom_point).

![](plot_rsq_rez_files/figure-markdown_strict/unnamed-chunk-1-1.png)

    #ggsave(aplot, filename='mean_by_perc_fd.png',  width=10, height=10, units='in', dpi=150) 

    rsqDF <- read.csv('./RESULTS/SummaryRsqs.csv', stringsAsFactors=F)

    head(rsqDF) 

    ##   motion_thresh   med_rsq      CI_95   n age_l age_u
    ## 1            40 0.9572487 0.03649907 270     6     9
    ## 2            15 0.9643414 0.04910226  90    15    18
    ## 3            50 0.9694590 0.04284391  90    12    15
    ## 4            40 0.9718624 0.04441847 120    15    18
    ## 5            15 0.9645524 0.04696635 120    15    18
    ## 6            45 0.9080782 0.17544432  30    11    14

    #Check frequencies and distributions
    table(rsqDF$motion_thresh)

    ## 
    ##   5  10  15  20  25  30  35  40  45  50 
    ## 100 100 100 100 100 100 100 100 100 100

    table(rsqDF$n)

    ## 
    ##  30  60  90 120 150 180 210 240 270 300 
    ## 100 100 100 100 100 100 100 100 100 100

    table(rsqDF$age_l-rsqDF$age_u)

    ## 
    ##   -3 
    ## 1000

    table(rsqDF[,c('motion_thresh', 'n')])

    ##              n
    ## motion_thresh 30 60 90 120 150 180 210 240 270 300
    ##            5  10 10 10  10  10  10  10  10  10  10
    ##            10 10 10 10  10  10  10  10  10  10  10
    ##            15 10 10 10  10  10  10  10  10  10  10
    ##            20 10 10 10  10  10  10  10  10  10  10
    ##            25 10 10 10  10  10  10  10  10  10  10
    ##            30 10 10 10  10  10  10  10  10  10  10
    ##            35 10 10 10  10  10  10  10  10  10  10
    ##            40 10 10 10  10  10  10  10  10  10  10
    ##            45 10 10 10  10  10  10  10  10  10  10
    ##            50 10 10 10  10  10  10  10  10  10  10

    table(rsqDF[,c('age_l', 'n')])

    ##      n
    ## age_l 30 60 90 120 150 180 210 240 270 300
    ##    6  10 10 10  10  10  10  10  10  10  10
    ##    7  10 10 10  10  10  10  10  10  10  10
    ##    8  10 10 10  10  10  10  10  10  10  10
    ##    9  10 10 10  10  10  10  10  10  10  10
    ##    10 10 10 10  10  10  10  10  10  10  10
    ##    11 10 10 10  10  10  10  10  10  10  10
    ##    12 10 10 10  10  10  10  10  10  10  10
    ##    13 10 10 10  10  10  10  10  10  10  10
    ##    14 10 10 10  10  10  10  10  10  10  10
    ##    15 10 10 10  10  10  10  10  10  10  10

    table(rsqDF[,c('motion_thresh', 'age_l')])

    ##              age_l
    ## motion_thresh  6  7  8  9 10 11 12 13 14 15
    ##            5  10 10 10 10 10 10 10 10 10 10
    ##            10 10 10 10 10 10 10 10 10 10 10
    ##            15 10 10 10 10 10 10 10 10 10 10
    ##            20 10 10 10 10 10 10 10 10 10 10
    ##            25 10 10 10 10 10 10 10 10 10 10
    ##            30 10 10 10 10 10 10 10 10 10 10
    ##            35 10 10 10 10 10 10 10 10 10 10
    ##            40 10 10 10 10 10 10 10 10 10 10
    ##            45 10 10 10 10 10 10 10 10 10 10
    ##            50 10 10 10 10 10 10 10 10 10 10

    qplot(rsqDF$med_rsq)

    ## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.

![](plot_rsq_rez_files/figure-markdown_strict/freq_check-1.png)

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

![](plot_rsq_rez_files/figure-markdown_strict/fun_plots-1.png)

    plotThing(age_color_n_facet)

![](plot_rsq_rez_files/figure-markdown_strict/fun_plots-2.png)
