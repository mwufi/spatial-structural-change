import os
import numpy as np
import pandas as pd

DIR = r"/home/cz/Dropbox/Summer RA Model EP/Parameters/"

class Params(object):
    """
    Empty container that you can assign properties to!

    c = Params()
    c.beta = 2
    c.alpha = 2
    """
    pass


def _read_matrix(name):
    """
    read a matrix file, such as ep_wages1880.csv
    """
    myfile = os.path.join(DIR, 'ep_{}.csv'.format(name))
    mat = pd.read_csv(myfile, header=None).values
    print("{}: {}".format(name.rjust(10), mat.shape))

    return mat


def read_params(directory=DIR):
    """
    Reads ep_params.csv file and returns a Params() object
    Reads all matrices too
    """
    param = Params()
    with open(os.path.join(directory, 'ep_params.csv')) as f:
        lines = f.readlines()
        values = lines[0].split(',')
        names = lines[2].replace('[','').replace(']','').strip().split(' ')

        # check to see if the preprocessing above keeps the right values
        if len(values) != len(names):
            print('not sure how to read this...')
            print(lines)

        print('Found {} parameters'.format(len(values)))    
        for k,v in zip(names, values):
            print('{} = {}'.format(k,v))
            # this is how to configure the param object!
            setattr(param, k.split('.')[1], float(v))
    
    others = ["skill1880", "wage1880", "Q_A", "Q_NA","Z", "vA", "Capital", "phi", "tau", "amenities"]

    for x in others:
        mat = _read_matrix(x)
        setattr(param, x, mat)

    return param
