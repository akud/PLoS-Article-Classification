common.misclassifications <- function(model,X,Y) {
	predictions <- model(X)	
    ncol <- dim(Y)[2]

    res <- apply(cbind(Y,predictions),1,function(t) which(t != 0)) #indexes of predicted classes, next to true classes
    sum(apply(res,2,function(t) if(t[2] - ncol != t[1]) 1 else 0))
}
