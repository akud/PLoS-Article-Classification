source('common.R')

cross.split <- function(trainingData,y,k){
#split the training data in to k piecies
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
#Return the complement of ith portion of split training data
#split - result of calling cross.split()
#i - the component to exclude
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

cross.error <- function(trainingData,y,k,modelFunc){
#compute the expected test errror by cross-validation
#This is the average of average number of misclassifications on each of the k components
#trainingData - x values of training data
#y - y values of training data
#k - how many pieces to split the training data in to
#modelFunc - function to build models.  must take arguments x and y, in that order
   split <- cross.split(trainingData,y,k)
   errors <- vector()
   for (i in 1:k){
       train <- cross.complement(split,i)
       model <- modelFunc(train$x,train$y)
       errors <- c(errors,
           common.misclassifications(model,split[[i]]$x,split[[i]]$y) / (dim(split[[i]]$x)[1]))
   }
   mean(errors)
}
