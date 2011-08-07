source('common.R')

forward.restrictedModel <- function(Xtrain,Ytrain,columns) {
#Create a linear regression model restricted to certain columns
#Xtrain - the matrix of X points for the training data
#Ytrain - the matrix of Y points for the training data
#columns - a vector of column indices to use in the model
	X <- Xtrain[,columns]
	X <- cbind(1,X)
	beta <- solve(crossprod(X),t(X))%*%Ytrain
	
	list(
	predict=function(x) { 
		if(class(x) == 'matrix') {
            nrow <- dim(x)[1]
			x <- x[,columns]
            dim(x) <- c(nrow,length(columns))
            print(dim(x))
		} else {
			x <- x[columns]
			x <- matrix(x,nrow=1)
            print(paste('converted to matrix:',dim(x)))
		}
        print(dim(beta))
		raw <- cbind(1,x)%*%beta
        t(apply(raw,1,function(t){
            index <- which(t == max(t))
            res <- rep(0,times=length(t))
            res[index] <- 1
            res
        }))
	}, 
	coefficients=beta,
	columns=columns )
}


forward.addNextColumn <- function(Xtrain,Ytrain,columns) {
#Create a vector of the given columns plus the next column which produces the best error 
#for a restricted linear regression model
	minError <- length(Ytrain)
    ncol = dim(Xtrain)[2]
	bestColumn <- 0
	for ( j in sample(1:ncol,ncol) ) { 
		if (!(j %in% columns)) {
			model <- forward.restrictedModel(Xtrain,Ytrain,c(columns,j))	
			error <- common.misclassifications(model$predict,Xtrain,Ytrain)
			if(error < minError) {
				minError <- error
				bestColumn <- j
				if(minError == 0) break #can't do better than that
			}
		}
	}
	c(columns,bestColumn)
}

forward.stepwiseModel <- function(Xtrain,Ytrain,k){
#create a forward stepwise linear model with k columns
	columns <- vector()	
	for ( i in 1:k ){
		columns <- forward.addNextColumn(Xtrain,Ytrain,columns)
	}
	forward.restrictedModel(Xtrain,Ytrain,columns)
}
