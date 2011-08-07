pca.converter <- function(trainingData) {
    print(paste(date(),'centering data...'),quote=FALSE)
    means <- apply(trainingData,2,mean)
    centered <- t(apply(trainingData,1,function(x) x - means))
    print(paste(date(),'finished'),quote=FALSE)
    
    print(paste(date(),'running svd decomposition...'),quote=FALSE)
    decomp <- svd(centered)
    print(paste(date(),'finished'),quote=FALSE)
    u <- decomp$u
    v <- decomp$v
    dInverse <- solve(diag(decomp$d))

    list(orig=u,
    convert=function(x){
        x <- common.matrix(x)
        x <- t(apply(x,1,function(r) r - means))
        x%*%v%*%dInverse
    })
}
