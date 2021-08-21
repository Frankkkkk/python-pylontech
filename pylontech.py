import serial
import construct

class HexToByte(construct.Adapter):
    def _decode(self, obj, context, path) -> bytes:
        # called at building time to return a modified version of obj
        hexstr = [chr(x) for x in obj]
        #print('hello')
        #print(hexstr)
        hex2 = [chr(int(''.join(hexstr[i:i+2]), 16)) for i in range(0, len(hexstr), 2)]
        #hex2 = [chr(int(hexstr[i:i+2], 16)) for i in range(0, len(hexstr), 2)]
        return ''.join(hex2).encode()

class HexToInt(construct.Adapter):
    def _decode(self, obj, context, path) -> bytes:
        hexstr = [chr(x) for x in obj]

        #print('hello')
        #print(hexstr)
        hex2 = [chr(int(''.join(hexstr[i:i+2]), 16)) for i in range(0, len(hexstr), 2)]
        #hex2 = [chr(int(hexstr[i:i+2], 16)) for i in range(0, len(hexstr), 2)]
        return ''.join(hex2).encode()

class JoinBytes(construct.Adapter):
    def _decode(self, obj, context, path) -> bytes:
        print(obj)
        return ''.join([chr(x) for x in obj]).encode()


class Pylontech:
    manufacturer_info_fmt = construct.Struct(
        "DeviceName" / JoinBytes(construct.Array(10, construct.Byte)),
        "SoftwareVersion" / construct.Array(2, construct.Byte),
        "ManufacturerName" / JoinBytes(construct.GreedyRange(construct.Byte)),
    )

    system_parameters_fmt = construct.Struct(  # XXX Yields invalid parsing
        "CellHighVoltageLimit" / construct.Array(2, construct.Byte),
        "CellLowVoltageLimit" / construct.Array(2, construct.Byte),
        "CellUnderVoltageLimit" / construct.Array(2, construct.Byte),
        "ChargeHighTemperatureLimit" / construct.Array(2, construct.Byte),
        "ChargeLowTemperatureLimit" / construct.Array(2, construct.Byte),
        "ChargeCurrentLimit" / construct.Array(2, construct.Byte),
        "ModuleHighVoltageLimit" / construct.Array(2, construct.Byte),
        "ModuleLowVoltageLimit" / construct.Array(2, construct.Byte),
        "ModuleUnderVoltageLimit" / construct.Array(2, construct.Byte),
        "DischargeHighTemperatureLimit" / construct.Array(2, construct.Byte),
        "DischargeLowTemperatureLimit" / construct.Array(2, construct.Byte),
        "DischargeCurrentLimit" / construct.Array(2, construct.Byte),
    )

    def __init__(self):
        port = '/dev/ttyUSB0'
        self.s = serial.Serial(port, 115200, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=2)

    def get_frame_checksum(self, frame: bytes):
        assert isinstance(frame, bytes)

        sum = 0
        for byte in frame:
            sum += byte
        sum = ~sum
        #sum &= 0xFFFF
        sum %= 0x10000
        sum += 1
        return sum


    def send_cmd(self, address: int, cmd, info):
        raw_frame = self._encode_cmd(address, cmd, info)
        print(f">> {raw_frame}")
        self.s.write(raw_frame)


    def _encode_cmd(self, address: int, cid2: int, info):
        cid1 = 0x46
        if len(info) != 0:
            raise Exception('Unimplemented for now')

        info_length = 0

        frame = "{:02X}{:02X}{:02X}{:02X}{:04X}".format(0x20, address, cid1, cid2, info_length).encode()

        frame_chksum = self.get_frame_checksum(frame)
        whole_frame = (b"~" + frame + "{:04X}".format(frame_chksum).encode() + b"\r")
        return whole_frame


    def _decode_hw_frame(self, raw_frame: bytes) -> bytes:
        # XXX construct
        frame_data = raw_frame[1:len(raw_frame)-5]
        frame_chksum = raw_frame[len(raw_frame)-5:-1]

        got_frame_checksum = self.get_frame_checksum(frame_data)
        assert got_frame_checksum == int(frame_chksum, 16)

        return frame_data

    def _decode_frame(self, frame):
        format = construct.Struct(
            "ver" / HexToByte(construct.Array(2, construct.Byte)),
            "adr" / HexToByte(construct.Array(2, construct.Byte)),
            "cid1" / HexToByte(construct.Array(2, construct.Byte)),
            "cid2" / HexToByte(construct.Array(2, construct.Byte)),
            "infolength" / HexToByte(construct.Array(2, construct.Byte)) + HexToByte(construct.Array(2, construct.Byte)),
            "info" / HexToByte(construct.GreedyRange(construct.Byte)),
        )

        return format.parse(frame)


    def read_frame(self):
        raw_frame = self.s.readline()
        f = self._decode_hw_frame(raw_frame=raw_frame)
        return self._decode_frame(f)



    def get_protocol_version(self):
        # XXX TODO
        self.send_cmd(0, 0x4f, '')
        rea = self.s.readline()
        print(f"<< {rea}")


    def get_manufacturer_info(self):
        self.send_cmd(0, 0x51, '')
        f = self.read_frame()

        ff = self.manufacturer_info_fmt.parse(f.info)
        print(ff)


    def get_system_parameters(self):
        self.send_cmd(2, 0x47, '')
        f = self.read_frame()
        print(f)
        print(f.info)

        ff = self.system_parameters_fmt.parse(f.info)
        print(ff)


if __name__ == '__main__':
    p = Pylontech()
    p.get_system_parameters()