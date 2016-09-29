import visa
import numpy as np
from struct import unpack

class Tektronix4104():

    armed = 'ARM\n'
    auto = 'AUTO\n'
    ready = 'READY\n'
    save = 'SAVE\n'
    trigger = 'TRIG\n'

    def __init__(self,ID):
        print "Setting up resource manager..."
        # import pdb; pdb.set_trace()

        self.rm = visa.ResourceManager()
        print "Opening resource..."
        self.scope = self.rm.open_resource(ID)

    def write(self,arg):
        return self.scope.write(arg)

    def query(self,arg):
        return self.scope.ask(arg)

    def read_raw(self):
        return self.scope.read_raw()

    def getOffsets(self):
        self.write('DATA:SOU CH1')
        self.write('DATA:WIDTH 1')
        self.write('DATA:ENC RPB')

        self.ymult = float(self.query('WFMPRE:YMULT?'))
        self.yzero = float(self.query('WFMPRE:YZERO?'))
        self.yoff  = float(self.query('WFMPRE:YOFF?'))
        self.xincr = float(self.query('WFMPRE:XINCR?'))

        offsets = [self.ymult,self.yzero,self.yoff,self.xincr]
        return offsets

    def checkTrigger(self):
        self.state = self.query('TRIGGER:STATE?')
        return self.state

    def setTriggerNorm(self):
        self.write('TRIGGER:A:MODe NORMAL')
        return 0

    def readData(self):
        self.write('CURVE?')
        self.data = self.read_raw()
        return np.shape(self.data)

    def unpackData(self):
        headerlen = 2 + int(self.data[1])
        header = self.data[:headerlen]
        ADC_wave = self.data[headerlen:-1]

        ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))

        self.volts = (ADC_wave - self.yoff)*self.ymult + self.yzero
        self.time = np.arange(0,self.xincr*len(self.volts),self.xincr)

        return [self.time,self.volts]
