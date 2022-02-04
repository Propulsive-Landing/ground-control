import serial

def serial_port_available(port):
    try:
        temp = serial.Serial(port)
        temp.close()
        return True
    except serial.SerialException:
        return False