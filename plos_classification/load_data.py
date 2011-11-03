'''
Holds functions for loading data from csv files
'''
import csv, numpy

def load(xfile,yfile,np=False):
    '''
    Load the data from the specified csv files
    xfile - file-like object or string pointing to csv holding x data
    yfile - file-like object or string pointing to csv holding y data
    np - if true, return the data as numpy arrays
    '''
    x = []
    y = []
    if isinstance(xfile,str) or isinstance(xfile,unicode):
        xfile = open(xfile)
    if isinstance(yfile,str) or isinstance(yfile,unicode):
        yfile = open(yfile)

    for row in csv.reader(xfile):
        x.append([float(f) for f in row])

    for row in csv.reader(yfile):
        try:
            y.append(row.index('1'))
        except ValueError:
            y.append(-1)
    if not np:
        return x,y
    else:
        return numpy.asarray(x),numpy.asarray(y)
