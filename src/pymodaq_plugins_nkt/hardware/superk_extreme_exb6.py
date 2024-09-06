from pylablib.devices import NKT


class Extreme:
    def __init__(self, com_port = "COM5"):

        self._com_port = com_port

        self.laser = NKT.GenericInterbusDevice(self._com_port)

    def close(self):
        register_address = 0x30
        self.laser.ib_set_reg(15, register_address, 0, "u8")  # Turn OFF laser
        self.laser.close()

    def scan_devices(self):
        self.laser.ib_scan_devices(dests=["COM4", "COM5"])

    def set_power(self, value: int):
        register_address = 0x37
        self.laser.ib_set_reg(15, register_address, value, "u16")

    def set_emission(self, state):

        register_address = 0x30
        self.laser.ib_set_reg(15, register_address, state, "u8")


# if __name__ == "__main__":
#     laser = Extreme()