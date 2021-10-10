class DataPacket():
    def __init__(self):
        self.mode = 0
        self.loop_number = 0
        self.current_time = 0
        self.dt = 0
        self.voltage_a = 0
        self.voltage_b = 0
        self.euler = (0, 0, 0)
        self.y = (0, 0, 0, 0)
        self.x = (0, 0, 0, 0, 0, 0)
        self.dx = (0, 0, 0, 0, 0, 0)
        self.yaw = 0
        self.current_u = (0, 0)
        self.servo_u = (0, 0)
