source('setup.R')

x <- seq(20,1000,by=20)

plainErrors <- vector()
pcErrors <- vector()

for (i in x) {
    common.log('running LDA with',i,'most correlated PCs and columns')
    plain <- function(X,Y) lda.mostCorrelated(X,Y,i)
    error <- cross.validation(trainingData,yTrain,5,plain)
    plainErrors <- c(plainErrors,error)
    common.log('Error for most correlated columns:',error)
    rm(plain)
    pc <- function(X,Y) lda.pcMostCorrelated(X,Y,i)
    error <- cross.validation(trainingData,yTrain,5,pc)
    pcErrors <- c(pcErrors,error)
    common.log('Error for most correlated pcs:',error)
    rm(pc)
}

jpeg('plots/lda_images/lda_mostCorr.jpg')
plot(x,plainErrors,type='l',col='orange',xlab='k',ylab='Expected Error',
    main='10-fold Cross Validation Error')
lines(x,pcErrors,col='turquoise')
legend('topleft',c('Most Correlated PCs','Most Correlated Columns'),fill=c('turquoise','orange'))
dev.off()
