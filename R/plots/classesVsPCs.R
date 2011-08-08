source('setup.R')

title <- 'Classes'
numPCs <- 10
imgDir <- 'plots/pc_images/all'
numClasses <- dim(yTrain)[2]
numDimensions <- dim(trainingData)[2]
converter <- pca.converter(trainingData)
graphColors <- colors()[sample(1:length(colors()),53)]

for (i in 1:(numPCs - 1)) {
    for ( j in (i + 1):numPCs ) {
        common.log('plotting class in PC dimensions',i,'and',j)
        jpeg(paste(imgDir,'/pc_',i,'_vs_',j,'.jpg',sep=''))

        xlim <- c(min(converter$orig[,i]),max(converter$orig[,i]))
        ylim <- c(min(converter$orig[,j]),max(converter$orig[,j]))

        classPoints <- common.classPoints(converter$orig,yTrain,1)
        plot( classPoints[,i],classPoints[,j],col=graphColors[1],
            type='p',xlab=paste('PC',i),ylab=paste('PC',j),
            pch='.',main=title,xlim=xlim,ylim=ylim )

        for( f in 1:numClasses ) {
            classPoints <- common.classPoints(converter$orig,yTrain,f)
            points(classPoints[,i],classPoints[,j],
                col=graphColors[f],pch='.')
        }
        dev.off()
    }
}
