#import calkulate as calk
from numpy import genfromtxt

class Titration:
    
    def __init__(self, name):
        self.name = name
        
    def vindta(self, filename, delimiter='\t', skip_header=2):
        """Import a single VINDTA-style .dat file titration dataset."""
        tData = genfromtxt(filename, delimiter=delimiter,
            skip_header=skip_header)
        self.volAcid = tData[:, 0] # ml
        self.emf = tData[:, 1] # mV
        self.tempK = tData[:, 2] + 273.15 # K

testit = Titration('test')
testit.vindta('datfiles/Dickson1981sim.dat')
