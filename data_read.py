import csv

def loadFile(fileName):
    result = [l for l in csv.reader(open(fileName,'rb'),delimiter=",")]
    return result


# l is a list of numbers, foo() does something to numbers
def fooIt(l):
    return [foo(x) for x in l]


def loadFile(fileName):
    data = [l for l in csv.reader(open(fileName,'rb'),delimiter=',')]
    header = data[0]
    result = [dict([(header[i],l[i])
                    for i in range(min(len(header),len(l)))])
                   for l in data[1:]]
    return result

def makeTuples(line, header):
    return [(header[i],line[i]) for i in range(min(len(header),len(line)))]


def loadFile(fileName):
    data = [l for l in csv.reader(open(fileName,'rb'),delimiter=',')]
    header = data[0]
    result = [dict(makeTuples(header,l)) for l in data[1:]]
    return result

import json
def toJSON(data):
    return json.dumps(data)



def loadData(fileName):
    reader = csv.reader(open(fileName,'rb'),delimiter=",")
    header = reader.next()
    m = dict( [ (header[i],i) for i in range(len(header)) ] )
    # This is a set of x,y points with an id, name,
    # and visibility attribute.
    cols = {
        "id":int,
        "x":float,
        "y":float,
        "name":str,
        "visible":int
    }
    result = {}
    for line in reader:
        # make a dict for each line, using the constructor in
        # the cols dict to build the right object.
        lineMap = dict([ cols[c](line[m[c]]) for c in cols.keys ])
        result[lineMap['id']] = lineMap
    return result
