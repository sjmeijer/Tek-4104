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
        self.rm = visa.ResourceManager()
        self.scope = self.rm.open_resource(ID)

    def getOffsets(self):
        self.scope.write('DATA:SOU CH1')
        self.scope.write('DATA:WIDTH 1')
        self.scope.write('DATA:ENC RPB')

        self.ymult = float(self.scope.ask('WFMPRE:YMULT?'))
        self.yzero = float(self.scope.ask('WFMPRE:YZERO?'))
        self.yoff  = float(self.scope.ask('WFMPRE:YOFF?'))
        self.xincr = float(self.scope.ask('WFMPRE:XINCR?'))

        offsets = [self.ymult,self.yzero,self.yoff,self.xincr]
        return offsets

    def checkTrigger(self):
        self.state = self.scope.ask('TRIGGER:STATE?')
        return self.state

    def setTriggerNorm(self):
        self.scope.write('TRIGGER:A:MODe NORMAL')
        return 0

    def readData(self):
        self.scope.write('CURVE?')
        self.data = self.scope.read_raw()
        return self.data

    def unpackData(self):
        headerlen = 2 + int(self.data[1])
        header = self.data[:headerlen]
        ADC_wave = self.data[headerlen:-1]

        ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
        self.volts = (ADC_wave - self.yoff)*self.ymult + self.yzero
        self.time = np.arange(0,self.xincr*len(self.volts),self.xincr)

        return [self.time,self.volts]
