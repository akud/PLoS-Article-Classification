pca.converter <- function(trainingData) {
    common.log('centering data...')
    means <- apply(trainingData,2,mean)
    centered <- t(apply(trainingData,1,function(x) x - means))
    common.log('finished')
    
    common.log('running svd decomposition...')
    decomp <- svd(centered)
    common.log('finished')
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
