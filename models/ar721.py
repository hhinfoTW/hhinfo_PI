from time import sleep
import serial
from datetime import datetime
import chkcard as chkcard
import WebApiClient.remote as remote
import globals

def callback(uid):
    print("__________do_read_ar721________________")
    uid =str(uid).zfill(10)
    chkcard.chkcard(uid)


def write_command_to_node(func):
    #print("ar721-",node," send =",func)
    node=1
    xor=255^node^int(func,16)
    sum=node+int(func,16)+xor
    sum =sum % 256
    comm=b'\x7e\x04'+ bytes([node])+ bytes([int(func,16)]) + bytes([xor])+ bytes([sum])
    ser = serial.Serial(globals._scanner.sname, globals._scanner.baurate, timeout=1)
    ser.write(comm)
    sleep(0.2)
    
def do_read_ar721():
    ser = serial.Serial(globals._scanner.sname, globals._scanner.baurate, timeout=1)
    ser.flushInput()  # flush input buffer
    ser.flushOutput()  # flush output buffer
    node = 1
    while True:
       
        write_command_to_node('0x25')
        try:
            output = ser.read(64)
            # print('node=',node,output,len(output))
            # print(hex(output[0]))
            # print(hex(output[1]))
            # print(hex(output[2]))
        except:
            print('read error')
        if len(output)==31:
            today=str(datetime.now().strftime('%Y-%m-%d'))
            time=str(datetime.now().strftime('%H:%M:%S'))
            ScanDate = "20" + str(output[11]).zfill(2) + "-" + str(output[10]).zfill(2) + "-" + str(output[9]).zfill(2)
            ScanTime = str(output[7]).zfill(2) + ":" + str(output[6]).zfill(2) + ":" + str(output[5]).zfill(2)
            #print(today,ScanDate)
            
            if today==ScanDate:
                # print('系統時間=',today,time)
                # print('721時間=',ScanDate,ScanTime)
                # print('array len=',len(output))
                if output[3]==0x3 and output[1]==0x1d:
                    UID =  bytearray(b'\x00\x00\x00\x00')
                    UID[0] = output[19]
                    UID[1] = output[20]
                    UID[2] = output[23]
                    UID[3] = output[24]
                    uid = int.from_bytes(UID, byteorder='big')
                    print('ar721刷卡記錄,node=',node,uid,ScanDate,ScanTime)
                    write_command_to_node('0x37')
                    sleep(0.2)
                    callback(uid)
                else :
                    write_command_to_node('0x37')
                    sleep(0.2)
            else:
                write_command_to_node('0x37')
        

# if __name__=='__main__':
#     print('____ar721_init___')
    #sname='/dev/ttyUSB0'
    # sname='/dev/ttyUSB0'
    # baurate=9600
    #do_read_ar721(sname,baurate)
