class DataPacket():
    def __init__(self, mode, loop_number, current_time, dt, voltage_a, voltage_b, euler, x, y, dx, yaw, current_u, servo_u):
        self.mode = mode
        self.loop_number = loop_number
        self.current_time = current_time
        self.dt = dt
        self.voltage_a = voltage_a
        self.voltage_b = voltage_b
        self.euler = euler
        self.y = y
        self.x = x
        self.dx = dx
        self.yaw = yaw
        self.current_u = current_u
        self.servo_u = servo_u
