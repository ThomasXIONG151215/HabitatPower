#详情请看 开放空间气体射流特性.ipynb
import math
class Gas_Jet():
    def __init__(self):
        self.A = 0.671
        self.B = 3.4
        self.C = 0.294
        self.D = 0.965
        self.E = 0.646
        self.F = 0.76
        self.G = 1.32
        self.I = 6.8
        self.J = 11.56
        self.K = 0.706
        self.O = 0.4545
        self.Q = 0.35 #or 0.11 apparently
        self.S = 0.51
        self.P = 0.015
    
    def sn(self, ro, a): #核心段长度
        return self.A * ro / a
    
    def R(self, a, s, r0): #截面半径
        return self.B * (a * s / r0 + self.C)

    def vm(self, v0, a, s, r0): #核心速度
        return v0 * self.D / (a * s / r0 + self.C)

    def Qv(self, Qv0, R, r0): #核心流量
        return Qv0 * self.E * R / r0
    
    def v1(self, v0, ro, R): #断面平均流速
        return v0 * ro / R

    def v2(self,v0, Qv, Qv0): #断面质量流速
        return v0 * Qv0 / Qv

    def v1n(self, v0, a, s, r0): #初始段平均流速
        x = a*s/r0
        return v0 * (1 + self.F * x + self.G * x**2) / (1 + self.I * x + self.J * x ** 2)

    def v2n(self, v0, a, s, r0):
        x = a*s/r0
        return v0 / (1 + self.F * x + self.G * x ** 2)

    def T(self, Te, T0, R, s, v0, r0): #接触面温度, #假设轴心温度等同于出口温度
        if s > 0: #速度越快，温差射流影响阻力越小，所以到达位置温度更接近出风口气温
            return (s+0.1 / R) ** (-self.P - 1/self.v1(v0, r0, R) ) * (T0 - Te) + Te
        else:
            return T0
      

    def T1(self, T0, Te, a, s, r0): #平均温度
        # 轴心温度或者别的温度都想
        return Te + self.K /(a*s/r0 + self.C) * (T0 - Te) 

    def T2(self, T0, Te, a, s, r0): #质量平均温度
        return Te + self.O /(a*s/r0 + self.C) * (T0 - Te)
    
    def trajectory(self, d0, s, alpha, a, T0, Te, v0):#射流轨迹
        g = 9.8
        Archi = g * d0 * (T0 - Te) / (v0**2 * Te)
        #s 在x轴上
        deviation = Archi * (s / (d0 * math.cos(alpha)) ** 2 * (self.S * a * s /(d0 * math.cos(alpha)) + self.Q))
        return deviation, d0 * ( s/d0 * math.tan(alpha) + deviation)

    