# Tek-4104
Some basic code for interacting with a Tektronix DPO4104 oscilloscope

This code was tested on OS X, but should work on pretty much anything.

In order to use this you will need to have PyVISA installed. This can be done with a
> pip install -U pyvisa

The PyVISA code relies on having a VISA (virtual instrument software architecture) library installed. The one I used is freely available from National Instruments (here)[http://www.ni.com/visa/], though they make you register with them.

In order to talk to your instrument, you will need to make a VISA string to describe it.

If you are using an ethernet connection, set up the scope in person to make sure you know it's IP address, then it will just use the following format:
> 'TCPIP::192.168.1.234::INSTR'

where you can replace the 192.168.1.234 with whatever your actual IP address was

The Tektronix scopes also allow connection through USB and a GPIB adapter of some kind; I never needed it, so never added this functionality, but it would probably be something like
> 'USB0::0x0699::0x0401::No_Serial::INSTR'

for a USB device, and just give up on GPIB already, the future is now.
