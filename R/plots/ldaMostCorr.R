source('setup.R')

x <- 1:50

plainErrors <- vector()
pcErrors <- vector()

for (i in x) {
    common.log('running LDA with',i,'PCs')
    plain <- function(X,Y) lda.mostCorrelated(X,Y,i)
    plainErrors <- c(errors,cross.validation(pc$orig,yTrain,10,plain))
    rm(plain)
    pc <- function(X,Y) lda.pcMostCorrelated(X,Y,i)
    pcErrors <- c(errors,cross.validation(pc$orig,yTrain,10,pc))
    rm(pc)
}

jpeg('plots/lda_images/lda_mostCorr.jpg')
plot(x,plainErrors,type='l',col='orange',xlab='k',ylab='Expected Error',
    main='10-fold Cross Validation Error')
lines(x,pcErrors,col='turquoise')
legend('topleft',c('Most Correlated PCs','Most Correlated Columns'),fill=c('turquoise','orange'))
dev.off()
