import serial
ser = serial.Serial('com3',115200)
data = ''
while 1:
         
    while ser.inWaiting() > 0:
      data += str(ser.read(1), 'utf-8')
    if data != '':
      print (data)
      data=''
