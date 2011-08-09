basis.correlated <- function(trainingData,yTrain) {
#order the input columns by their correlation to the response classes
    corMatrix <- cor(trainingData,yTrain)
    columns <- apply(corMatrix,2,function(x) order(x,decreasing=FALSE)) #order each column of corMatrix
    columns <- c(t(columns)) #put in vector form, going along rows first
    rm(corMatrix)
    unique(columns) #return unique column list
}

basis.quadratic <- function(x) {
    #function to transform input into the quadratic space of input columns
    make_prods <- function(x) {
        prods <- vector()
        for (i in 1:length(x)) for (j in i:length(x)) prods <- c(prods,x[i]*x[j])
        prods
    }
    common.matrix(apply(common.matrix(x),1,function(t) make_prods(c(1,t))))
}
