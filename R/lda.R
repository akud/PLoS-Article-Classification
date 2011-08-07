library('MASS')

lda.model <- function(trainingData,yTrain) {
    classes <- apply(yTrain,1,function(x) which(x == 1))
    fit <- lda(classes ~ trainingData)
    nclasses <- dim(yTrain)[2]

    function(x) {
        clazz <- predict(fit,x)
        vec <- rep(0,times=nclasses)
        vec[clazz] <- 1
        vec
    }
}


lda.restricted <- function(trainingData,yTrain,columns) {
    lda.model(trainingData[,columns],yTrain)
}
