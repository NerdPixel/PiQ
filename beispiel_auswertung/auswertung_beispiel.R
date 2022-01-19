# set the path where you data is.
setwd("~/git/seminar-image-quality-wise21-22/2-Teil-projects/datenauswertung")

df <- read.csv(file = 'Beispiel.csv')

################################################################################
##### Some sanity checks ######

# explore the first entries in your data
head(df)

# sanity checks: how many groups do you expect per categorical variable?
# in these data we expect :
# 5 different k values
k_values <- unique(df$k)
print(k_values)

# 5 different g values
g_values <- unique(df$g)
print(g_values)


# 15 different pictures
unique(df$picture)


# we expect 5x5 different rows of possible k, g combinations
agg1 <- aggregate(df$quality_value, 
                  by = list(k=df$k, g=df$g), 
                  FUN = length)

print(agg1)

print(nrow(agg1))
# !! we only obtain 24 different rows.. 
# !! k=1.0 and g=1.0 was never presented...

# and 24 x 15 pictures = 360  different types of trials
agg2 <- aggregate(df$quality_value, 
                  by = list(k=df$k, g=df$g, picture=df$picture), 
                  FUN = length)
nrow(agg2)

# each of them with one entry
print(agg2)


################################################################################
#### Creating some visualizations #######
### we make a barplot using base R (we avoid to use ggplot on purpose here, 
# the logic of ggplot can be complicated to understand at first...)

###########################
###### for one picture
picname <- 'Abstrakt'

# I select the data from the main dataframe 
onepic <- df[df$picture==picname,]

# we aggregate around k values
agg_k <- aggregate(onepic$quality_value, by=list(k=onepic$k), FUN=mean)
agg_k.sd <- aggregate(onepic$quality_value, by=list(k=onepic$k), FUN=sd)

barCenters <- barplot(agg_k$x, names.arg = agg_k$k, xlab='Contrast', 
                      ylab='Quality', ylim = c(-3, 3), col='#e34a33')
arrows(barCenters, agg_k$x - agg_k.sd$x, 
       barCenters, agg_k$x + agg_k.sd$x,
       lwd = 1.5, angle = 90,
       code = 3, length = 0.05)

title(paste('Picture:', picname, sep=' '))

# we aggregate around g values
agg_g <- aggregate(onepic$quality_value, by=list(g=onepic$g), FUN=mean)
agg_g.sd <- aggregate(onepic$quality_value, by=list(g=onepic$g), FUN=sd)

barCenters <- barplot(agg_g$x, names.arg = agg_g$g, xlab='Gamma', ylab='Quality', 
                      ylim = c(-3, 3), col='#3182bd')
arrows(barCenters, agg_g$x - agg_g.sd$x, 
       barCenters, agg_g$x + agg_g.sd$x,
       lwd = 1.5, angle = 90,
       code = 3, length = 0.05)

title(paste('Picture:', picname, sep=' '))

###############################
# either for all pictures
#d <- df
#picname <- 'All'

# or for only one picture
d <- onepic


# to create a barplot for all k and g combinations, we need to create a dataframe 
# where rows and columns are k and g 
agg_mean <- aggregate(d$quality_value, by=list(g=d$g, k=d$k), FUN=mean)
colnames(agg_mean)[3] <- 'quality_value'

# reshape convert the table from "long" to "wide" format, 
# taking the idvar column as an index,timevar as the variable that will become the columns.
agg_mean <- reshape(agg_mean, idvar = "k", timevar = 'g', direction = "wide")
# we assign the values of k to each row.
rownames(agg_mean) <- agg_mean$k
# now we can drop the first column 
agg_mean <- agg_mean[-c(1)]
colnames(agg_mean) <- k_values

print(agg_mean)


# now we can finally plot
# a palette of 5 Greens (from https://colorbrewer2.org/)
palette <- c('#edf8e9', '#bae4b3', '#74c476', '#31a354', '#006d2c')

# calls barplot function
barCenters <- barplot(t(as.matrix(agg_mean)), beside=TRUE, xlab='Kontrast', 
                      ylab="Quality", 
                      col = palette, ylim=c(-3, 3))
box(bty="l")
legend("topright", legend = rownames(agg_mean), fill=palette, title='Gamma')
title(paste('Picture:', picname, sep=' '))


# I didn't do the panels, 
# it's more complicated to do without ggplot


######## Some statistical analysis #######
### t-test
k1 <- df[df$k==0.5,]
k2 <- df[df$k==1.0,]

t.test(k1$quality_value, k2$quality_value)


#### Two-way ANOVA
# setting up variables k and g as categorical data (as factors)
df$k <- as.factor(df$k)
df$g <- as.factor(df$g)

# ANOVA call
res.aov <- aov(quality_value ~ k + g, data=df)

print(summary(res.aov))

# post-hoc test: t-tests with Bonferroni correction
ph <- pairwise.t.test(df$quality_value, df$k, 
                paired=FALSE, p.adjust.method='bonf')


print(ph)

# EOF
