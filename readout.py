import pylab
import matplotlib.pyplot as plt
from TektronixClasses import Tektronix4104

def main():
    try:
        ID = 'TCPIP::152.19.204.238::INSTR'
        oscope = Tektronix4104(ID)

        oscope.getOffsets()
        armed   = oscope.armed
        auto    = oscope.auto
        ready   = oscope.ready
        save    = oscope.save
        trigger = oscope.trigger

        state = oscope.checkTrigger()

        plt.ion()
        fig = plt.figure()

        triggerCount = 0;
        checkCount = 1;
        while(True):
            if(oscope.state == oscope.trigger):
                triggerCount+=1;
                print "Scope has triggered %d/%d, reading out data now" % (triggerCount,checkCount)
                data = oscope.readData()
                [time,volts] = oscope.unpackData()
                plt.plot(time,volts)
                plt.show()
                plt.pause(0.0001)
                if (oscope.state == oscope.auto):
                    oscope.setTriggerNorm()

            state = oscope.checkTrigger()
            checkCount+=1
        rm.close()

    finally:
        print "closing..."
    return 0

if __name__ == "__main__":
    main()
