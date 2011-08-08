source('setup.R')

x <- seq(20,1000,by=20)

errors <- vector()

for (i in x) {
    common.log('running LDA with',i,'PCs')
    modelFunc <- function(X,Y) lda.pcModel(X,Y,i)
    errors <- c(errors,cross.validation(pc$orig,yTrain,10,modelFunc))
    rm(modelFunc)
}

common.log('got errors:',common.tostring(errors))
jpeg('pc_images/pc_lda.jpg')
plot(x,errors,type='l',col='orange',xlab='Number of PCs',ylab='Expected Error',
    main='10-fold Cross Validation Error\n for LDA with PC Decomposition')
