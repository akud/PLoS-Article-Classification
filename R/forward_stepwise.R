forward.addNextColumn <- function(Xtrain,Ytrain,columns,modelFunc) {
#Create a vector of the given columns plus the next column which produces the best error 
#for the given model generating function
	minError <- length(Ytrain)
    ncol = dim(Xtrain)[2]
	bestColumn <- 0
	for ( j in sample(1:ncol,ncol) ) { 
		if (!(j %in% columns)) {
			model <- modelFunc(Xtrain,Ytrain,c(columns,j))	
			error <- common.misclassifications(common.predictor(model),Xtrain,Ytrain)
			if(error < minError) {
				minError <- error
				bestColumn <- j
				if(minError == 0) break #can't do better than that
			}
		}
	}
	c(columns,bestColumn)
}

forward.stepwiseModel <- function(Xtrain,Ytrain,k,modelFunc=basic.restrictedLin){
#create a forward stepwise model with k columns
#the model function given must take in arguments x,y,columns
#and return a model on x and y, restricted to the given columns
	columns <- vector()	
	for ( i in 1:k ) {
		columns <- forward.addNextColumn(Xtrain,Ytrain,columns,modelFunc)
	}
	modelFunc(Xtrain,Ytrain,columns)
}
