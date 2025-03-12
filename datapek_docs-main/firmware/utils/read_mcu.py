import smbus
import time

# MPU9250
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
TEMP_OUT_H = 0x41
Device_Address = 0x68  

# AK8963 magnetometer 
AK8963_ADDRESS = 0x0C
MAG_XOUT_L = 0x03
MAG_YOUT_L = 0x05
MAG_ZOUT_L = 0x07
CNTL1 = 0x0A

class GY_91:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.MPU_Init()
        self.AK8963_Init()

    def MPU_Init(self):
        """Initialize the MPU9250 with the standard settings."""
        self.bus.write_byte_data(Device_Address, PWR_MGMT_1, 0x00)  
        self.bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
        self.bus.write_byte_data(Device_Address, CONFIG, 0)
        self.bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
        self.bus.write_byte_data(Device_Address, ACCEL_CONFIG, 0x00) 
        self.bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    def AK8963_Init(self):
        """Initialize the AK8963 magnetometer inside the MPU9250."""
        self.bus.write_byte_data(AK8963_ADDRESS, CNTL1, 0x16)  # Continuous measurement mode 2
        time.sleep(0.01)  

    def read_raw_data(self, addr, device=Device_Address):
        """Read the raw data from the sensor."""
        high = self.bus.read_byte_data(device, addr)
        low = self.bus.read_byte_data(device, addr + 1)
        value = ((high << 8) | low)
        if value > 32768:
            value -= 65536
        return value

    def read_magnetometer(self):
        data = self.bus.read_i2c_block_data(AK8963_ADDRESS, MAG_XOUT_L, 6)
        mag_x = data[1] << 8 | data[0]
        mag_y = data[3] << 8 | data[2]
        mag_z = data[5] << 8 | data[4]

        # Convert signed values
        mag_x = mag_x - 65536 if mag_x > 32768 else mag_x
        mag_y = mag_y - 65536 if mag_y > 32768 else mag_y
        mag_z = mag_z - 65536 if mag_z > 32768 else mag_z

        return mag_x, mag_y, mag_z

