source('basic_classifiers.R')
source('common.R')
source('cross_validation.R')
source('forward_stepwise.R')
source('pca.R')
source('lda_and_qda.R')

print(paste(date(),'loading training data...'),quote=FALSE)
trainingData <- as.matrix(read.csv('../data/train.csv',header=FALSE))
yTrain <- as.matrix(read.csv('../data/ytrain.csv',header=FALSE))

print(paste(date(),'removing 0-vectors...'),quote=FALSE)
zeroVectors <- which(apply(trainingData,1,function(x) length(which(x != 0)) == 0))
trainingData <- trainingData[-1*zeroVectors,]
yTrain <- yTrain[-1*zeroVectors,]
print(paste(date(),'removed',length(zeroVectors),'vectors; stored word count vectors in trainingData, classes in yTrain'),quote=FALSE)
