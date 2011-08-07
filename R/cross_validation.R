source('common.R')

cross.split <- function(trainingData,y,k){
    nrows <- dim(trainingData)[1]
    rand  <- sample(1:nrows,nrows)
    numPer <- floor(nrows / k)
    samples <- list()
    for (i in 0:(k-1)){
       first <- numPer*i + 1
       last <- if (i < k - 1) first + numPer - 1 else nrows 
       rows <- rand[first:last]
       samples[[i+1]] <- list(x=trainingData[rows,],y=y[rows,])
    }
    samples
}

cross.complement <- function(split,i) {
    xcol <- dim(split[[1]]$x)[2]
    ycol <- dim(split[[1]]$y)[2]
    x <- matrix(ncol=xcol)
    y <- matrix(ncol=ycol)
    for(f in 1:length(split)){
        if(f != i) {
            x <- rbind(x,split[[f]]$x)
            y <- rbind(y,split[[f]]$y)
        }
    }
    x <- x[-1,]
    y <- y[-1,]
    list(x=x,y=y)
}

cross.error <- function(trainingData,y,modelFunc,k){
   split <- cross.split(trainingData,y,k)
   errors <- vector()
   for (i in 1:k){
       train <- cross.complement(split,i)
       model <- modelFunc(train$x,train$y)
       errors <- c(errors,
           common.misclassifications(
           model,split[[i]]$x,split[[i]]$y) / dim(split[[i]]$x)[1])
   }
   mean(errors)
}
