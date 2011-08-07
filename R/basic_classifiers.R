library(lars)

basic.linReg <- function(trainingData,y){
	U1 <- cbind(1,trainingData)
	beta <- vector()
	tryCatch({
		beta <- solve(crossprod(U1),t(U1))%*%y
	},error=function(e){
		print(paste('singular system for linear regression, dim(U)=[',dim(trainingData)[1],',',dim(trainingData)[2],']; returning 0-predictor'))
	})
    print(dim(beta))
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

basic.pcr <- function(trainingData,y,k){

#center the data first
	means <- apply(trainingData,2,mean)
	Ucentered <- t(apply(trainingData,1,function(x) x - means)) #for some reason apply() is transposing

#do svd
	decomp <- svd(Ucentered)
	u <- decomp$u
	v <- decomp$v
	d <- diag(decomp$d)
#only keep the first k pc's
	u <- u[,1:k]

	u1 <- cbind(1,u)
	bhat <- vector()
	tryCatch({
		bhat <- solve(t(u1)%*%u1)%*%t(u1)%*%y
	},error=function(e){ 
		print(paste('singular system for pcr, dim(U)=[',dim(trainingData)[1],',',dim(trainingData)[2],']; returning 0-predictor'))
	})	
	if(length(bhat)==0){
		bhat <- rep(0,times=(dim(u1)[2]))
	}

#return the function to make predictions
	function(x){
		x <- x - means
		#convert to PC coordinates
		x <- x%*%v%*%solve(d)
#drop extra coordinates
		x <- x[1:k]
#make prediction
		raw <- c(1,x)%*%bhat
        res <- rep(0,times=dim(X)[2])
        res[which(raw == max(raw))] <- 1
        res
	}
}
