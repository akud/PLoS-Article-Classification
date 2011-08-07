common.misclassifications <- function(model,X,Y) {
#compute the number of misclassifications of a model on given data
	predictions <- model(X)	
    ncol <- dim(Y)[2]

    res <- apply(cbind(Y,predictions),1,function(t) which(t != 0)) #indexes of predicted classes, next to true classes
    sum(apply(res,2,function(t) if(t[2] - ncol != t[1]) 1 else 0))
}

common.classRows <- function(Y,i) {
#Get a list of the rows of the given class
    classes <- apply(Y,1,function(x) which(x == 1))
    which(classes == i)
}

common.classPoints <- function(X,Y,i){
#Get a matrix of the points of the given class
    rows <- common.classRows(Y,i)
    points <- X[rows,] 
    common.matrix(points)
}

common.classCenter <- function(X,Y,i) {
#compute the class center (mean)
    points <- common.classPoints(X,Y,i)
    apply(points,2,mean) 
}

common.matrix(x) {
#utility function to convert to a single row matrix if
# the argument isn't already a matrix
    if(class(x) != 'matrix')
        x <- matrix(x,nrow=1)
    x
}

common.predictor <- function(model) {
#Get the predictor element of a model - 
# if the argument is a function, it is itself returned
# else return the first element of it which is a function
    if( class(model) == 'function') {
        model
    } else {
        predictor <- NULL
        for(el in 1:length(model)){
            if(class(model[[el]]) == 'function'){
                predictor <- model[[el]]
                break
            }
        }
        if (predictor != NULL) 
            predictor
        else 
           function(x) {
               x <- common.matrix(x)               
               predict(model,x)
           }
    }
}
