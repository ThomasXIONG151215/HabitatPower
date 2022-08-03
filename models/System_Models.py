

class Tower():
    def __init__(self):
        self.Tower_efficiency = 0.5 # to adjust later
        self.G_a = 0
        self.G_w = 0
        self.c_w = 10
        self.T_tower_w_E = 0

        self.h_as_E = 0
        self.h_a_E = 0

        self.h_as_L = 0
        self.h_a_L = 0

        self.A_tower = 1
        self.B_tower = 1

        self.Q_tower = 0
        self.T_tower_w_L = 0
        self.Pump = 0 # 水塔有自己的泵

        #水塔还可以考虑空气温湿度

    def heat_reject_capacity(self, G_a, G_w, h_as_E, h_a_E):

        self.G_a = G_a
        self.G_w = G_w
        self.h_as_E = h_as_E
        self.h_a_E = h_a_E

        #equation 1
        self.Q_tower = self.Tower_efficiency * self.G_a * (self.h_as_E - self.h_a_E) #'as' for saturated moist air
        #equation 2
        # self.Q_tower = self.c_w * self.G_w * (self.T_tower_w_E - self.T_tower_w_L)

        #两个equations一起可以计算出水塔出水温度
        return self.Q_tower
    

    def tower_efficiency(self): # 
        import numpy as np
        import math

        self.m = self.G_a / self.G_w * (self.h_as_E - self.h_as_L) / (self.T_tower_w_E - self.T_tower_w_L)
        self.Ntu = self.A * (self.G_a / self.G_w) ** self.B
        self.Tower_efficiency = (1 - math.exp(- self.Ntu * (1 - self.m))) / (1 - self.m * math.exp(-self.Ntu * (1 - self.m)))#related to Gtower,a, Gtower,w, h_as_E, h_as_L, t_tower_w_E, t_tower_w_L, A and B

        #to whether follow the above equations would mainly depends on the possibility to acquire all these parameters
        # otherwise another DL model considering less parameters is to be employed


    def Outlet_water_T(self, Twe):
        self.T_tower_w_E = Twe
        self.Pump.run_pump(self.G_w)
        self.T_tower_w_L = self.T_tower_w_E - self.Q_tower / (self.c_w * self.G_w)

        return self.T_tower_w_L


class Pump(): #主要围绕frequency和flow_rate设定的经验模型
    def __init__(self, H):
        self.flow_rate = 0 #t/h
        self.frequency = 0
        self.pumping_head = H #structure
        self.rho = 1 #t/m3
        #self.pump_efficiency = 0.7 # could be obtained empirically
        self.Npump = 0

        self.A = 1 #empirical representation of (factor coefficient / pump efficiency) based on G/G0


    def run_pump(self, G):
        self.flow_rate = G
        self.consumming_power()
        #self.frequency = F

    def consumming_power(self):
        self.Npump = (self.rho * self.A * self.flow_rate * self.pumping_head)



class Chiller(): 
    def __init__(self, cap): #physic + energy model
        self.Qe_max = cap # cooling capacity of the evaporator
        self.Qe = 0
        self.c_w = 10 #to adjust, water specific heat
        #parameters to vary
        self.r = 100 #operative load ratio, to be given during operations
        self.Ncom = 0
        self.COP = self.Qe + self.Ncom
        self.Tc = 0
        self.Te = 0
        self.a1 = 0
        self.a2 = 0
        self.G_w_c = 0
        self.G_w_e = 0
        self.T_w_c_E = 0
        self.T_w_e_E = 0
        self.T_w_e_L = 0
        self.T_w_c_L = 0
        self.Q_c = 0
        #辅助组件的参数
        self.G_tower_a = 0
        self.G_tower_w = 0
        self.h_as_E = 0
        self.h_a_E = 0
        self.T_tower_L = 0
        self.T_tower_E = 0
        self.state = 0 #开否,开1关0

        self.tower_limit_range = 0.01 #range of performance acceptance
    
    def assign(self, Tower, T_w_e_E): #与水塔耦合运行
        #self.Pump = Pump
        self.Tower = Tower
        self.T_w_e_E = T_w_e_E

    def condenser_rate(self): # comes from the tower
        return self.c_w * self.G_w_c * (self.T_w_c_L - self.T_w_c_E) #公式一， #还有一个公式可以用
        #公式二: Ncom + Qe
    
    def condenser_rate_and_tower_rate(self, T_tower_w_E, h_a_E, h_as_E, G_tower_a, G_tower_w): #一头得到水塔散热量，一头得到需求散热量
        self.Q_tower = self.Tower.heat_reject_capacity(G_tower_a, G_tower_w, h_a_E, h_as_E)
        self.T_tower_E = T_tower_w_E
        self.T_tower_L = self.Tower.Outlet_water_T(T_tower_w_E)
        #self.G_w_c = G_w_c #外部设定
        self.T_w_c_E = self.T_tower_L #需要修正
        self.T_w_c_L = self.T_tower_E #需要修正
        self.Q_c = self.condenser_rate()

    def heat_transfer_coeff(self, G):
        return 0.8 * G # to train and fit as an empirical function depending on Gwc and/or Gwe, may have to rotate between the two

    def loss_function_T(self, Tc, Te): # to train, fit and modify
        return 0.9 * Tc / Te 

    def consumming_power(self): #实际当中 Qc需要Ncom才能算出来，而Ncom一般而言可以通过仪表获得 / 
        #假设g_w_c和g_tower_w之间无损失
        #self.G_w_c = self.
        self.Tc = self.T_w_c_E + self.Q_c / (self.c_w * self.heat_transfer_coeff(self.G_w_c))
        self.COP = self.r / (self.r * (self.Tc / self.Te - 1) + self.loss_function_T(self.Te, self.Tc))
        self.Ncom = self.Qe / self.COP

    def simple_run(self, r, Te, T_tower_w_E, T_tower_w_L):
        #暂时先无视水塔
        self.T_tower_E = T_tower_w_E
        self.T_tower_L = T_tower_w_L
        self.T_w_c_E = self.T_tower_L
        self.T_w_c_L = self.T_tower_E
        self.Qc = self.condenser_rate()
        self.Te = Te
        self.r = r
        self.consumming_power()
        self.T_w_e_L = self.T_w_e_E - self.Qe / (self.c_w * self.G_w_e)
        return self.Ncom

    def run_core(self, r, Te, T_tower_w_E, h_a_E, h_as_E, G_tower_a, G_tower_w, epsilon):
        self.T_tower_E = T_tower_w_E
        self.condenser_rate_and_tower_rate(self.T_tower_E, h_a_E, h_as_E, G_tower_a, G_tower_w)
        
        self.tower_limit_range = epsilon
        self.Te = Te
        self.r = r
        
       # self.Pump.run_pump(pump_flow_rate, pump_frequency)

        while self.Q_c - self.Q_tower > self.tower_limit_range: #相当于通过调整T_tower_E配合当前天气来匹配水塔与冷凝器各自的散热

            self.T_tower_E = self.T_tower_E + (self.T_w_c_L - self.T_w_c_E)
            #self.T_w_c_L = self.T_tower_E #假设没有热量散出就设为1
            #self.T_w_c_E = self.T_tower_L
            self.condenser_rate_and_tower_rate(self.T_tower_E, h_a_E, h_as_E, G_tower_a, G_tower_w)
            #self.Pump.run_pump(pump_flow_rate, pump_frequency)
            
            
            if self.Q_c - self.Q_tower <= self.tower_limit_range:
                break

        self.consumming_power()
        return self.Ncom

class Exchanger(): #water to air/ air是热源，water是冷源因为地铁只在炎热时制冷
    def __init__(self):
        #self.U = U #coefficient global fixe de transfert de chaleur
        #self.A = A # surface d'echange thermique
        self.c_a = 10 #to adjust,   specific heat of air
        self.c_w = 10
        self.C_a = 0
        self.C_w = 0 #taux de capacite thermique
        self.C_min = 0
        self.Q_real = 0
        self.Q_max_poss = 0
        self.epsilon = 0 #efficacite de transfert
        self.m_a = 0
        self.m_w = 0
        self.t_a_E = 0
        self.t_w_E = 0
        self.t_a_L = 0
        self.t_w_L = 0
        self.t_s_E = 0
        self.t_s_L = 0
        self.G_w = 0
        self.G_a = 0

        # 假设t_w_L是t_chiller_E所以可以测量
        # t_a_L
    
    def running_conditions(self, twe, twl, gw): #先最简单的
        #Q = Cw(Tw,L - Tw,E)
        self.t_w_E = twe
        self.t_w_L = twl
        self.G_w = gw
        self.Q_real = self.G_w * self.c_w * (self.t_w_L - self.t_w_E)

        return self.Q_real

class Fan(): #假设都是variable speed fan
    def __init__(self, G):
        #self.flow_rate = 0
        #self.frequency = 0
        self.rho = 1000 #kg/m3
        self.fan_efficiency = 0.7 # could be obtained empirically
        self.Nfan = 0
        self.G = G # fan volumetric flow rate at design conditions (m3/s)
        self.n = 0 # fan speed at any conditions (rpm)
        self.P = 0 #total pressure of the fan under a certain speed


        self.A = 1
        self.B = 1
        self.C = 1
        self.D = 1
        self.E = 1

    def run_fan(self, n, n0):
        self.n = n
        self.n0 = n0 #不是特别确定什么时候的n是n0
        self.n_ratio = (self.n / self.n0)

    def consumming_power(self):
        self.Nfan = self.A * self.n_ratio ** 2 + self.B * self.n_ratio * self.G + self.C * self.G ** 2 + self.D * self.n_ratio * self.G ** 3 + self.G ** 4 * self.E * self.n_ratio ** 2
        #self.P = ....  # 以后可以加，但是目前不了解管道气压计算的价值

# Air Handling Unit
# exchanger + fan
class AHU():
    def __init__(self, exchanger, fan):
        self.exchanger = exchanger
        self.fan = fan