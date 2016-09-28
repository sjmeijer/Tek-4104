import visa
import numpy as np
from struct import unpack
import pylab
import matplotlib.pyplot as plt




def init(visaDevice):
    rm = visa.ResourceManager()
    scope = rm.open_resource(visaDevice)
    # scope = rm.open_resource('USB0::0x0699::0x0401::No_Serial::INSTR')

    return [rm,scope]

def getOffsets(scope):
    scope.write('DATA:SOU CH1')
    scope.write('DATA:WIDTH 1')
    scope.write('DATA:ENC RPB')

    ymult = float(scope.ask('WFMPRE:YMULT?'))
    yzero = float(scope.ask('WFMPRE:YZERO?'))
    yoff  = float(scope.ask('WFMPRE:YOFF?'))
    xincr = float(scope.ask('WFMPRE:XINCR?'))

    offsets = [ymult,yzero,yoff,xincr]

    return offsets

def getTriggerConditions():
    armed = 'ARM\n'
    auto = 'AUTO\n'
    ready = 'READY\n'
    save = 'SAVE\n'
    trigger = 'TRIG\n'

    return [armed,auto,ready,save,trigger]

def checkTrigger(scope):
    state = scope.ask('TRIGGER:STATE?')

    return state

def setTriggerNorm(scope):
    scope.write('TRIGGER:MODe NORMAL')
    return 0

def readData(scope):
    scope.write('CURVE?')
    data = scope.read_raw()

    return data

def unpackData(data,offsets):
    [ymult,yzero,yoff,xincr] = offsets

    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    ADC_wave = data[headerlen:-1]

    ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
    volts = (ADC_wave - yoff)*ymult + yzero
    time = np.arange(0,xincr*len(volts),xincr)

    return [time,volts]

def main():
    try:
        ID = 'TCPIP::152.19.204.238::INSTR'
        [rm,scope] = init(ID)
        offsets = getOffsets(scope)
        [armed,auto,ready,save,trigger] = getTriggerConditions()

        state = checkTrigger(scope)

        plt.ion()
        fig = plt.figure()

        triggerCount = 0;
        checkCount = 1;
        while(True):
            if(state == trigger):
                triggerCount+=1;
                print "Scope has triggered %d/%d, reading out data now" % (triggerCount,checkCount)
                data = readData(scope)
                [time,volts] = unpackData(data,offsets)
                plt.plot(time,volts)
                plt.show()
                plt.pause(0.0001)
                if (state == auto):
                    setTriggerNorm(scope)

        # else:
            #print "State was: ", state

            state = checkTrigger(scope)
            checkCount+=1
        rm.close()

    finally:
        print "closing..."
    return 0

if __name__ == "__main__":
    main()
