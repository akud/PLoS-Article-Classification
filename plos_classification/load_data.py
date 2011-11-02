import csv

def load(xfile,yfile):
    x = []
    y = []
    for row in csv.reader(open(xfile)):
        x.append([float(f) for f in row])
    for row in csv.reader(open(yfile)):
        try:
            y.append(row.index('1'))
        except ValueError:
            y.append(-1)
    return x,y
