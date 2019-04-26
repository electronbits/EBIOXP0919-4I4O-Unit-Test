"""
ElectronBits 2018-2019
The script tests EBIOXP0910-4I4O board
Testing 4 output relays and 4 inputs
"""
import smbus
from time import sleep
from sys import exit

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class IOXP4I4O:
    RD_REGISTER = 0x00 
    WR_REGISTER = 0x01
    CFG_REGISTER = 0x03
    MAX_RELAY = 4
    def __init__(self,chip_address=0x3f):
        print("\n"+Colors.OKGREEN+"\t\tTesting EBIOXP0919-4I4O\n"+Colors.ENDC)
        self.chip_address = chip_address
        self.bus = smbus.SMBus(1)
        self.error_counter = 0
        self.board_init()
        
    def board_init(self):
        try:
            self.bus.write_byte_data(self.chip_address,IOXP4I4O.CFG_REGISTER,0xf0)
            self.bus.write_byte_data(self.chip_address,IOXP4I4O.WR_REGISTER,0x0)
        except OSError as e:
            print(e)
            print(Colors.FAIL+"Device not found on I/O bus"+Colors.ENDC)
            self.error_counter+=1
            print(self)
            exit(1)

    def clean_up(self):
        print(Colors.HEADER+"cleaning up"+Colors.ENDC)
        self.bus.write_byte_data(self.chip_address,IOXP4I4O.WR_REGISTER,0x0)
        self.bus.close()


    def check_inputs(self):
        expected_values = {"Input 1":0xe,"Input 2":0xd,"Input 3":0xb,"Input 4":0x7}
        for input_name,value in expected_values.items():
            print("Checking input: %s"%(input_name))
            try:
                res = 0
                while not (res==value):
                    res= (self.bus.read_byte_data(self.chip_address,IOXP4I4O.RD_REGISTER))>>4
                print(Colors.OKBLUE+"%s verfied with value 0x%x"%(input_name,res)+Colors.ENDC)    
            except KeyboardInterrupt:
                self.error_counter += 1

    def check_relays(self):
        for i in range(IOXP4I4O.MAX_RELAY):
            try:
                print(Colors.OKBLUE+"Checking Relay: %s"%(i+1)+Colors.ENDC)
                self.bus.write_byte_data(self.chip_address,IOXP4I4O.WR_REGISTER,1 << i)
                sleep(0.3)
            except Exception as e:
                self.error_counter+=1
                print(Colors.FAIL+"Error happend as:\n%s"%(e)+Colors.ENDC)
        
    def __repr__(self):
        text_color = Colors.FAIL if self.error_counter else Colors.OKGREEN
        return text_color+"Test has been Done with %s error(s)."%(self.error_counter)+Colors.ENDC

if __name__ == "__main__":
    ioexp_test = IOXP4I4O()
    ioexp_test.check_relays()
    ioexp_test.check_inputs()
    ioexp_test.clean_up()
    print(ioexp_test)
    exit(0)

