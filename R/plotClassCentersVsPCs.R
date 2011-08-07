source('setup.R')

converter <- pca.converter(trainingData)
graphColors <- colors()[sample(1:length(colors()),53)]
centers <- vector()
for (i in 1:53){
   centers <- c(centers,common.classCenter(converter$orig,y,i)) 
   print(paste('computed center for class',i),quote=FALSE)
}
title <- 'Class Centers'
for (i in 1:10) {
    for (j in 1:10) {
        if (i != j) {
            jpeg(paste('pc_',i,'_vs_',j,'.jpg',sep=''))
            plot(centers[1][i],centers[1][j],col=graphColors[1],
                type='p',xlab=paste('PC',i),paste('PC',j),main=title)
            for( f in 1:53) {
                points(centers[f][i],centers[f][j],col=graphColors[f],
                type='p',xlab=paste('PC',i),paste('PC',j),main=title)
            }
            dev.off()
        }
    }
}

