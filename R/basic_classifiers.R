basic.lin <- function(trainingData,y){
	U1 <- cbind(1,trainingData)
	beta <- vector()
	tryCatch({
		beta <- solve(crossprod(U1),t(U1))%*%y
	},error=function(e){
		print(paste('singular system for linear regression, dim(U)=[',dim(trainingData)[1],',',dim(trainingData)[2],']; returning 0-predictor'))
	})
#don't want to reach in global scope from the error function so we don't mess with ridge's beta
	if(length(beta) ==0) beta <- rep(0,times=(dim(U1)[2]))
	function(X){
		raw <- cbind(1,X)%*%beta
        t(apply(raw,1,function(t) {
            index <- which(t == max(t))
            res <- rep(0,times=length(t))
            res[index] <- 1
            res
        }))
	}
}

basic.ridge <- function(trainingData,y,lambda) {
	U1 <- cbind(1,trainingData)
	n <- dim(U1)[2]
	beta <- vector()
	tryCatch({
		beta <- solve(crossprod(U1) + lambda*diag(n),t(U1))%*%y
	},error=function(e){
		print(paste('singular system for ridge regression, dim(U)=[',dim(trainingData)[1],',',dim(trainingData)[2],
			'], lambda = ',lambda,'; returning 0-predictor'))
	})
	if(length(beta) == 0) beta <- rep(0,times=(dim(U1)[2]))
	function(X) {
		raw <- cbind(1,X)%*%beta
         t(apply(raw,1,function(t) {
            index <- which(t == max(t))
            res <- rep(0,times=length(t))
            res[index] <- 1
            res
        }))
	}
}

basic.restrictedLin <- function(Xtrain,Ytrain,columns) {
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


