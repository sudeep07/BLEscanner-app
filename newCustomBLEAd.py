"""
Desktop         :       Sudeep R Dodda
Date created    :       09/15/2017
Description     :       Python script performs BLE advertisement scan and prints MAC address,
                        RSSI, Flags, UUID, Major, Minor and TX PWR.

                        Also defines two methods :

                        hexToInt(hexstr) & twos(hexstr) - commented later.

                        User inputs MAC address pattern used in BLE scan.
"""


from bluepy.btle import Scanner, DefaultDelegate

"""
    ##########################################################################
    hexToInt(hexStr) - converts a hex string into its equivalent integer value
    ##########################################################################
"""
def hexToInt(hexstr):
    hexSplit = [hexstr[2*i]+hexstr[2*i+1] for i in range(len(hexstr)/2)]
    toBits = map(lambda x: "{0:08b}".format(int(x, 16)), hexSplit)
    mergeBits = "".join(toBits)
    bitsToInt = int(mergeBits, 2)
    return bitsToInt

"""
    #############################################################################
    two(hexstr) - Performs two's complement on a hex string and returns the value
    #############################################################################
"""

def twos(hexstr):
    hexSplit = [hexstr[2*i]+hexstr[2*i+1] for i in range(len(hexstr)/2)]
    toBits = map(lambda x: "{0:08b}".format(int(x, 16)), hexSplit)
    compBits = ''
    for i in toBits[0]:
        if i == '0':
            compBits += '1'
        else:
            compBits += '0'
    return -1*(int(compBits,2)+1)

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    """def handleDiscovery(self, dev, isNewDev, isNewData):
        if str(dev.addr)[0:4] == str("00:a"):
            print "Found new LBeacon", dev.addr"""

BLEMac = raw_input("Enter the BLE mac address pattern: ")
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(1)
raw_data = []
for dev in devices:
    if dev.addr[0:len(BLEMac)] == BLEMac:
        print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Flags":
                a = value
            elif desc == "Manufacturer":
                b = value
        UUID = b[8:16]+"-"+b[16:20]+"-"+b[20:24]+"-"+b[24:28]+"-"+b[28:40]
        Major = hexToInt(b[40:44])
        Minor = hexToInt(b[44:48])
        TxPwr = twos(b[48:])
        print "Flags\t=\t" + a
        print "UUID\t=\t%s" %UUID 
        print "Major\t=\t%i" % Major
        print "Minor\t=\t%i" % Minor
        print "TX PWR\t=\t%idBs" % TxPwr
        print "*********************************************************"

