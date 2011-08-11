source('setup.R')

x <- 10:20

plainErrors <- vector()
pcErrors <- vector()

for (i in x) {
    pc <- function(X,Y) lda.pcMostCorrelated(X,Y,i)
    error <- cross.validation(trainingData,yTrain,5,pc)
    pcErrors <- c(pcErrors,error)
    common.log('Error for most correlated pcs:',error)
    rm(pc)
}

jpeg('plots/performance_images/lda_mostCorr10_20.jpg')
plot(x,pcErrors,type='l',col='orange',xlab='k',ylab='Expected Error',
    main='5-fold Cross Validation Error')
dev.off()
