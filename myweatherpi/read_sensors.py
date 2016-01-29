# read_sensors.py
#

import smbus

ADDRESS = 0x4E
BOARD_VERSION_COMMAND = 0x24
BOARD_TEMP_COMMAND = 0x42
HUMIDITY_COMMAND = 0x43
PRESSURE_COMMAND = 0x47
TEMP_SENSOR_1 = 0x45
TEMP_SENSOR_2 = 0x46

bus = smbus.SMBus(0)

board_version = bus.read_byte_data(ADDRESS, BOARD_VERSION_COMMAND)
board_temp = bus.read_byte_data(ADDRESS, BOARD_TEMP_COMMAND)
humidity = bus.read_byte_data(ADDRESS, HUMIDITY_COMMAND)
pressure = bus.read_byte_data(ADDRESS, PRESSURE_COMMAND)
temp_1 = bus.read_byte_data(ADDRESS, TEMP_SENSOR_1)
temp_2 = bus.read_byte_data(ADDRESS, TEMP_SENSOR_2)

print("Board version    : {0}".format(board_version))
print("Board temperature: {0:.2f}C".format(board_temp))
print("Humidity         : {0}%".format(humidity))
print("Pressure         : {0}kPa".format(pressure))
print("Temp 1           : {0:.2f}C".format(0.1 * temp_1))
print("Temp 2           : {0:.2f}C".format(0.1 * temp_2))
