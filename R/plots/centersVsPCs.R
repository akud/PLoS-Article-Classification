source('setup.R')

title <- 'Class Centers'
numPCs <- 10
imgDir <- 'pc_images'
numClasses <- dim(yTrain)[2]
numDimensions <- dim(trainingData)[2]
converter <- pca.converter(trainingData)
graphColors <- colors()[sample(1:length(colors()),53)]
centers <- matrix(0,nrow=numClasses,ncol=numDimensions) 

common.log('computing class centers...')
for ( i in 1:numClasses ){
   centers[i,] <- common.classCenter(converter$orig,yTrain,i)
}
common.log('finished')
for (i in 1:(numPCs - 1)) {
    for ( j in (i + 1):numPCs ) {
        common.log('plotting class centers in PC dimensions',i,'and',j)
        jpeg(paste(imgDir,'/pc_',i,'_vs_',j,'_center.jpg',sep=''))
        xlim <- c(min(centers[,i]),max(centers[,i]))
        ylim <- c(min(centers[,j]),max(centers[,j]))
        plot(centers[1,i],centers[1,j],col=graphColors[1],
            type='p',xlab=paste('PC',i),ylab=paste('PC',j),
            main=title,xlim=xlim,ylim=ylim)
        for( f in 1:numClasses ) {
            points(centers[f,i],centers[f,j],col=graphColors[f])
        }
        dev.off()
    }
}

