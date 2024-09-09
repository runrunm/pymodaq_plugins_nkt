import pylablib as pll
from pylablib.devices import NKT


class Extreme:
    def __init__(self):

        self._laser_port = None

        self.laser_addr = 15  # 15 for Extreme/Fianum lasers

        # Port autodetection
        laser_found = False
        for port in pll.list_backend_resources("serial"):
            device = NKT.GenericInterbusDevice(port)

            if self.laser_addr in device.ib_scan_devices():
                if not laser_found:
                    self._laser_port = port
                    laser_found = True
                elif laser_found:
                    err_msg = ('''Multiple NKT Lasers found on computer. This plugin does not handle
                    multiple NKT lasers yet.
                    ''')
                    raise RuntimeError(err_msg)

            device.close()  # Close all previously opened COM ports

        self.laser = NKT.GenericInterbusDevice(self._laser_port)

        self.laser.ib_set_reg(self.laser_addr, 0x30, 0, "u8")  # Turn OFF laser

    def system_type(self):
        register_address = 0x61
        return self.laser.ib_get_reg(self.laser_addr, register_address, "u8")

    def close(self):
        register_address = 0x30
        self.laser.ib_set_reg(self.laser_addr, register_address, 0, "u8")  # Turn OFF laser
        self.laser.close()

    def set_power(self, value: int):
        register_address = 0x37
        self.laser.ib_set_reg(self.laser_addr, register_address, value, "u16")

    def set_emission(self, state):
        register_address = 0x30
        self.laser.ib_set_reg(self.laser_addr, register_address, state, "u8")


if __name__ == "__main__":
    laser = Extreme()
    print(laser.system_type())