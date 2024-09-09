import pylablib as pll
from pylablib.devices import NKT


class Extreme:
    def __init__(self):

        self._laser_port = None

        self.laser_addr = 15  # 15 for Extreme/Fianum lasers

        laser_found = False
        for port in pll.list_backend_resources("serial"):
            device = NKT.GenericInterbusDevice(port)

            if self.laser_addr in device.ib_scan_devices() and not laser_found:
                self._laser_port = port
                laser_found = True

            device.close()

        self.laser = NKT.GenericInterbusDevice(self._laser_port)

        self.laser.ib_set_reg(self.laser_addr, 0x30, 0, "u8")  # Turn OFF laser

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


# if __name__ == "__main__":
#     laser = Extreme()