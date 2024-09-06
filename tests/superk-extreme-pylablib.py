from pylablib.devices import NKT

laser = NKT.GenericInterbusDevice("COM5")

# print(laser.ib_get_reg(15,0x11,"i16")/10)  # the register is temperature in 0.1C
# laser.ib_set_reg(15,0x37,170,"u16")  # set power to 60% (the register is power level in 0.1%)
#
# print(laser.ib_get_reg())
laser.close()
print(laser)