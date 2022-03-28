import serial
from serial import SerialException


def m701a_str_to_dict(info: str) -> dict:
    if len(info) != 17:
        raise IOError("Info Lenth mismatch")
    if not (info[0] == 0x3C and info[1] == 0x02):
        raise IOError("Header mismatch")
    new_info = [0 for i in range(17)]
    for i in range(17):
        new_info[i] = int(info[i])
    checksum = new_info[16]
    check_base = 0
    for i in range(16):
        check_base += new_info[i]
    check_base &= 0xFF
    if check_base != checksum:
        raise IOError("Checksum mismatch: %d vs %d" % (check_base, checksum))
    ret = {
        'CO2': new_info[2] * 256 + new_info[3],
        'CH2O': new_info[4] * 256 + new_info[5],
        'TVOC': new_info[6] * 256 + new_info[7],
        'PM2.5': new_info[8] * 256 + new_info[9],
        'PM10': new_info[10] * 256 + new_info[11],
        'Temperature': new_info[12] + new_info[13] * 0.1,
        'Humidity': new_info[14] + new_info[15] * 0.1
    }
    return ret


class connect_helper:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600):
        try:
            self.connect = serial.Serial(port=port, baudrate=baudrate)
        except SerialException as e:
            print(e)
            print('Cannot open serial port')
            print('Try: sudo chmod 666 "%s"' % port)

    def read(self):
        self.connect.reset_input_buffer()
        info = self.connect.read(17)
        info_dict = m701a_str_to_dict(info)
        return info_dict
