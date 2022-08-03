

class Fluid_Node():
    def __init__(self):
        self.flow_rate = 0
        self.temperature = 0
        self.humidity = 0

class Air_Node(Fluid_Node):
    def __init__(self):
        Fluid_Node.flow_rate = 0
        Fluid_Node.temperature = 0
        Fluid_Node.humidity = 0

class Water_Node(Fluid_Node):
    def __init__(self):
        Fluid_Node.flow_rate = 0
        Fluid_Node.temperature = 0

class Room():
    def __init__(self):
        self.demand_wind = 0
        self.temperature = 0
        self.humidity = 0
        self.taking_wind = 0
        self.CO2 = 0
        self.zone_A_population = 0
        self.zone_B_population = 0

class Outdoor():
    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.air_enthalpy = 0
        self.moist_air_enthalpy = 0
        self.wind_speed = 0
        self.CO2 = 0