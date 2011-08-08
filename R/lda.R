library('MASS')

lda.model <- function(trainingData,yTrain) {
#Fit a standard LDA model on all the columns in the given X matrix
    classes <- apply(yTrain,1,function(x) which(x == 1))
    fit <- lda(data.frame(trainingData),classes)
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
lda.restricted <- function(trainingData,yTrain,columns) {
#Fit an LDA model restricted to the given columns.  
    model <- lda.model(trainingData[,columns],yTrain)
    function(x) {
        x <- common.matrix(x)
        x <- common.matrix(x[,columns])
        model(x)
    }
}
lda.pcRestricted <- function(trainingData,yTrain,columns,pcConverter=NULL) {
#fit an LDA model by using the given PCs
    if(is.null(pcConverter))
        pcConverter <- pca.converter(trainingData)
    model <- lda.model( pcConverter$orig[,columns],yTrain )
    function(x) {
      x <- common.matrix( pcConverter$convert(x)[,columns] )
      model(x)
    }
}
lda.pcModel <- function(trainingData,yTrain,k) {
#Fit an LDA model by using only the first k PCs
    lda.pcRestricted(trainingData,yTrain,1:k)
}
lda.mostCorrelated <- function(trainingData,yTrain,k){
#fit an LDA model on the input columns which are most correlated to the output classes
#k - the number of columns to use for each class; i.e. for each class we will choose the k most 
#    correlated columns to use in the model. Note that only unique columns will be selected, so 
#    the model may be trained on less than dim(yTrain)[2]*k columns
    common.log('computing',k,'most correlated columns for each class...')
    columns <- apply( cor(trainingData,yTrain),2,function(x) order(x)[1:k] )
    columns <- unique(c(columns)) 
    common.log('finished, got',length(columns),'columns to use')
    lda.restricted(trainingData,yTrain,columns)
}
lda.pcMostCorrelated <- function(trainingData,yTrain,k) {
#fit an LDA model on the PCs which are most correlated to the response classes
#k - the number of columns to use for each class
    converter <- pca.converter(trainingData)
    common.log('computing',k,'most correlated pcs for each class...')
    columns <- apply( cor(converter$orig,yTrain),2,function(x) order(x)[1:k] )
    columns <- unique(c(columns)) 
    common.log('finished, got',length(columns),'pcs to use')
    lda.pcRestricted(trainingData,yTrain,columns,pcConverter=converter)
}
