library('MASS')

lda.model <- function(trainingData,yTrain,type) {
    classes <- apply(yTrain,1,function(x) which(x == 1))
    fit <- if(type=='lda')
        lda(data.frame(trainingData),classes)
    else
        qda(data.frame(trainingData),classes)

    nclasses <- dim(yTrain)[2]

    function(x) {
        x <- common.matrix(x)
        predictedClasses <- predict(fit,x)$class
        output <- matrix(0,nrow=length(predictedClasses),ncol=nclasses)
        for (i in 1:length(predictedClasses))
            output[i,predictedClasses[i]] <- 1
            output
    }
}
lda.restricted <- function(trainingData,yTrain,columns,type='lda') {
    model <- lda.model(trainingData[,columns],yTrain,type)
    function(x) {
        x <- common.matrix(x)
        x <- matrix(x[,columns],ncol=length(columns))
        model(x)
    }
}
lda.pcModel <- function(trainingData,yTrain,k,pcConverter=NULL,type='lda') {
    if (is.null(pcConverter))
        pcConverter <- pca.converter(trainingData)
    model <- lda.model( pcConverter$orig[,1:k],yTrain,type )
    function(x) {
      x <- common.matrix( pcConverter$convert(x)[,1:k] )
      model(x)
    }
}

qda.model <- function(trainingData,yTrain) {
    lda.model(trainingData,yTrain,'qda')
}

qda.restricted <- function(trainingData,yTrain,columns) {
    lda.restricted(trainingData,yTrain,columns,'qda')
}

qda.pcModel <- function(trainingData,yTrain,k) {
    lda.pcModel(trainingData,yTrain,k,'qda')
}
