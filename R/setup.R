source('basic_classifiers.R')
source('common.R')
source('cross_validation.R')
source('forward_stepwise.R')
source('basis_conversion.R')
source('pca.R')
source('lda.R')

common.log('loading training data...')
trainingData <- as.matrix(read.csv('../data/train.csv',header=FALSE))
yTrain <- as.matrix(read.csv('../data/ytrain.csv',header=FALSE))

common.log('removing 0-vectors...')
zeroVectors <- which(apply(trainingData,1,function(x) length(which(x != 0)) == 0))
trainingData <- trainingData[-1*zeroVectors,]
yTrain <- yTrain[-1*zeroVectors,]
common.log('removed',length(zeroVectors),'vectors') 
rm(zeroVectors)
common.log('finished; stored word count vectors in trainingData, subject indicator vectors in yTrain')
