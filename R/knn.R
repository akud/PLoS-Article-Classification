knn.restrictedColumns <- function(trainingData,yTrain,k,columns) {
    distance <- function(x,y) sqrt(sum((x-y)**2))
    ncol <- dim(yTrain)[2]
    function(x) {
        x <- common.matrix(x)[,columns]
        common.log('finding',k,'nearest neghbors ..')
        neighbors <- apply(x,1,function(rowOfX)                          #for each row of X
            order(apply(trainingData[,columns],1,          #compute the distance to each row of trainingData
            function(trainingRow) distance(rowOfX,trainingRow)))[1:k])  #order and return k closest
        common.log('computing majority vote among responses...')
        responses <- apply(neighbors,2, function(rows) yTrain[rows,]) #get the responses 
        t(apply(responses,2, function(x) {
            mat <- matrix(x,ncol=ncol)
            votes <- apply(mat,2,sum)
            res <- rep(0,times=ncol)
            res[which(votes == max(votes))[1]] <- 1
            res
        }))
    }
}

knn.pc <- function(trainingData,yTrain,k,pcs) {
    converter <- pca.converter(trainingData)
    knnModel <- knn.restrictedColumns(converter$orig,yTrain,k,1:pcs)
    function(x) {
        knnModel(converter$convert(x))
    }
}

knn.mostCorrelated <- function(trainingData,yTrain,k,numColumns) {
    columns <- basis.correlated(trainingData,yTrain)[1:k]
    knn.restrictedColumns(trainingData,yTrain,k,columns)
}
