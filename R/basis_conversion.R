basis.correlated <- function(trainingData,yTrain) {
#order the input columns by their correlation to the response classes
    corMatrix <- cor(trainingData,yTrain)
    columns <- apply(corMatrix,2,order) #order each column of corMatrix
    columns <- c(t(columns)) #put in vector form, going along rows first
    rm(corMatrix)
    unique(columns) #return unique column list
}
