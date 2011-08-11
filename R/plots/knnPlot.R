source('setup.R')

k <- 2:12

errors2 <- vector()
errors4 <- vector()

for (i in k) {
    model2 <- function(X,Y) knn.pc(X,Y,i,2)
    error2 <- cross.validation(trainingData,yTrain,2,model2)
    common.log('Error for k=',i,'with 2 pcs:',error2)
    errors2 <- c(errors2,error2)
    model4 <- function(X,Y) knn.pc(X,Y,i,4)
     error4 <- cross.validation(trainingData,yTrain,2,model4)
    common.log('Error for k=',i,'with 4 pcs:',error4)
    errors4 <- c(errors4,error4)
}

jpeg('plots/performance_images/knn.jpg')
ylim <- c(min(c(errors2,errors4)),max(c(errors2,errors4)))
plot(k,errors2,type='l',col='orange',xlab='k',ylab='Expected Error',
    main='KNN 2-fold Cross Validation Error',ylim=ylim)
lines(k,errors4,col='turquoise')
legend('topleft',c('2 PCs','4 PCs'),fill=c('orange','turquoise'))
dev.off()

common.log('computing 10-fold cross validation error for standard lda')
cross.validation(trainingData,yTrain,10,lda.model)
