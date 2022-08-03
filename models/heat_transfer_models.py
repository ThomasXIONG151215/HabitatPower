import numpy as np 
#from air_characteristics import air
import CoolProp.CoolProp as cp
from models.gas_jet import Gas_Jet
import pandas as pd
air = Gas_Jet()
import plotly.express as px
#mass volumique kg/m3 et chaleur specifique W/m.K
def air_rho_cp(T, P):
    return cp.PropsSI('D', 'T', T, 'P', P, 'Air'), cp.PropsSI('C', 'T', T, 'P', P, 'Air') #W/m.K

def source_coordinates(xs, ys, zs, ax, bx, cx, air_outlets): #空调出风口位置
    #等比例网格化
    axx = np.linspace(0, xs, ax, retstep=True)[0]
    bxx = np.linspace(0, ys, bx, retstep=True)[0]
    cxx = np.linspace(0, zs, cx, retstep=True)[0]

    #修正下长度
    ax = len(axx)
    bx = len(bxx)
    cx = len(cxx)

    axxx = np.array([[i] * bx * cx for i in axx])
    bxxx = np.array([[[j] * cx for j in bxx] * ax ])
    cxxx = np.array([[k for k in cxx] * ax * bx])

    axxx = axxx.flatten()
    bxxx = bxxx.flatten()
    cxxx = cxxx.flatten()
    #xxx, yyy, zzz = np.where(zeros == 0)
    zzz = np.reshape(cxxx, (ax, bx, cx))
    yyy = np.reshape(bxxx, (ax, bx, cx))
    xxx = np.reshape(axxx, (ax, bx, cx))

    coors = np.concatenate((xxx[:, :, :, None], yyy[:, :, :, None], zzz[:, :, :, None]), axis=-1)
    outlet_projections = []
    for x in range(len(coors)): 
        for y in range(len(coors[0])): 
            for z in range(len(coors[0][0])):
                xval = coors[x][y][z][0]
                yval = coors[x][y][z][1]
                zval = coors[x][y][z][2]
                #print((y, yval))
                if int(xval) in [int(air_outlets[i][0]) for i in range(len(air_outlets))]: 
                #or int(xval) in [int(air_outlets[i][0]) - 1 for i in range(len(air_outlets))] or int(xval) in [int(air_outlets[i][0]) + 1 for i in range(len(air_outlets))]: 
                    #print('1')
                    if int(yval) in [int(air_outlets[i][1]) for i in range(len(air_outlets))]: 
                    #or int(yval) in [int(air_outlets[i][1]) - 1 for i in range(len(air_outlets))] or int(yval) in [int(air_outlets[i][1]) + 1 for i in range(len(air_outlets))] : 
                        #print('2')
                        if int(zval) in [int(air_outlets[i][2]) for i in range(len(air_outlets))]: 
                        #or int(zval) in [int(air_outlets[i][2]) - 1 for i in range(len(air_outlets))] or int(zval) in [int(air_outlets[i][2]) + 1 for i in range(len(air_outlets))]: 
                            outlet_projections.append((xval, yval, zval))

    return coors, outlet_projections


def structure(coors, projection_outlets, d0, a, Te, T0, v0, cx, zs, alpha): #Setting initial temperatures of the environmental block according to the ac outlet's gas jet characteristics
    

    bundle = {'x': [], 'y': [], 'z': [], 'T': [], 'P': [], 'Rho': [], 'Cp': [], 'Type': []}

    Temperatures = []
    Receive_or_not = []
    cooling_umbrella = [] #umbrella顶点记录下来，谁在下面谁受冷

    for x in range(len(coors)):
        #print(x)
        Temperatures.append([])
        Receive_or_not.append([])

        for y in range(len(coors[0])):
            Temperatures[x].append([])
            Receive_or_not[x].append([])
            #print((x,y))
            s = y #从这儿看
            R = air.R(a, s, d0/2)
            T_jet = air.T(Te, T0, R, s, v0, d0/2)
            #print(z_deviation)
            for z in range(len(coors[0][0])):
                #print(z)
                xval = coors[x][y][z][0]
                yval = coors[x][y][z][1]
                zval = coors[x][y][z][2]

                bundle['x'].append(xval)
                bundle['y'].append(yval)
                bundle['z'].append(zval)


                if (xval,yval,zval) in projection_outlets: #固定出风口位置
                    #print('出风口位置')
                    T = T0
                    bundle['Type'].append('Active') #Active相当是自发热or发冷，Passive受热or受冷
                    Receive_or_not[x][y].append(False)
                    cooling_umbrella.append((y,z))

                elif zval < projection_outlets[0][2] and xval in [int(projection_outlets[i][0]) for i in range(len(projection_outlets))]: #横向射流影响
                    #print(T_jet)
                    s = abs(yval - y) #相对于出风口的s，如果出风口y=3， yva=4，s= yval - y，
                    z_deviation, traj = air.trajectory(d0, s, alpha, a ,T0, Te, v0)
                    if zval == projection_outlets[0][2] + int(z_deviation): #出风口射流经过位置
                    #z_deviation在这里是负数因为不考虑浮力，
                        T = T_jet
                        bundle['Type'].append('Active')
                        Receive_or_not[x][y].append(False)
                        cooling_umbrella.append((y,z))
                    else:
                        T = Te
                        bundle['Type'].append('Passive')
                        Receive_or_not[x][y].append(True)
                
                elif (xval, yval) in [(projection_outlets[i][0], projection_outlets[i][1]) for i in range(len(projection_outlets))] and zval < projection_outlets[0][2]: #出风口正下方
                    T = Te - 3 * (zval) / (zs) 
                    bundle['Type'].append('Active') #Active相当是自发热or发冷，Passive受热or受冷
                    Receive_or_not[x][y].append(False)
                    cooling_umbrella.append((y,z))

                else:
                    T = Te
                    bundle['Type'].append('Passive')
                    Receive_or_not[x][y].append(True)
                            
                    #cooling_umbrella.append(None) #不是umbrella就是None
                
                Temperatures[x][y].append(T)
                bundle['T'].append(T) #大家都一样
                bundle['P'].append(10350) #pascal
                rho, Cp = air_rho_cp(T + 273.15, 10350)
                bundle['Rho'].append(rho)
                bundle['Cp'].append(Cp)
    print((len(bundle['T']), len(bundle['P']), len(bundle['Rho']), len(bundle['Cp']), len(bundle['x']),
    len(bundle['y']), len(bundle['z'])))
    df = pd.DataFrame(bundle)
    df['R'] = air.R(a=a, s = df['y'], r0 = d0/2)
    df['Qv'] = air.Qv(Qv0= 300, R = df['R'], r0 = d0/2)
    df['v2'] = air.v2(v0 = v0,Qv=df['Qv'], Qv0=300)
    return df, Temperatures, cooling_umbrella, Receive_or_not

def heat_transfer(df, ax, bx, cx, zs, dt, dx, lamb, d0, T0, passengers, v0, total_time_of_simulation, Temperatures, cooling_umbrella, Receive_or_not):
    
    cs = Temperatures.copy() #current state
    df['moment 0 T']= df['T'].copy()
    count = 0
    cold_q = 0
    for t in range(int(total_time_of_simulation)):
        print(t)
        ns = cs.copy()
        new_T_list = []
        for x in range(ax):
            count += 1 
            for y in range(bx):
                count += 1
                for z in range(cx):
                    count += 1
                    
                    a = lamb / (df['Rho'][x+y+z] * df['Cp'][x+y+z]) 
                    dy = dx
                    dz = dx

                    #if y == 0 and z == 5:
                    #    new_value = T0

                    #else:
                    if x == ax - 1:
                        A = 0
                    else:
                        A = cs[x + 1][y][z]
                    
                    if x == 0:
                        B = 0
                    else:
                        B = cs[x - 1][y][z]
                    
                    if y == bx - 1:
                        C = 0
                    else:
                        C = cs[x][y + 1][z]
                    
                    if y == 0:
                        D = 0
                    else:
                        D = cs[x][y - 1][z]
                    
                    if z == cx - 1:
                        E = 0
                    else:
                        E = cs[x][y][z + 1]
                    
                    if z == 0:
                        F = 0
                    else:
                        F = cs[x][y][z - 1]

                        #if count < 600:
                        #    if df['v2'][count] > 1.9:
                        #        cold_q = 200
                        #    elif df['v2'][count] < 1.6:
                        #        cold_q = 80
                        #    rho = df['Rho'][count]
                        #    Cp = df['Cp'][count]
                        #else:
                        #    cold_q = 0
                        #    rho = 1
                        #    Cp = 1000
                    for (yu,zu) in cooling_umbrella:
                        if y == yu and z < zu:
                            #print(y,z)
                            cold_q = 100 * (z+1 / zu+1) #垂直等比例扩散
                            pass
                        #else:
                        #   cold_q = 0
                    
                    #if (x, y) in [(projection_outlets[i][0], projection_outlets[i][0]) for i in range(len(air_outlets))]: #在出风口地下的会受到定期冷量
                        #   cold_q = 10 * (z+1) / (zs+1)
                    
                    if (x,y) in passengers and z in [0, 1 * cx / zs, 2 * cx / zs]:
                        hot_q = 100 * ( z+1 / 3)
                    else:
                        hot_q = 0

                    rho = 1
                    Cp = 1000

                    if count < ax*bx*cx and Receive_or_not[x][y][z] == False:
                        #print((x,y,z))
                        #print('Active')
                        s = y #从这儿看
                        R = air.R(a, s, d0/2)
                        Te_t = np.mean([i for i in [A, B, C, D, E, F] if i != 0])
                        T_jet = air.T(Te_t, T0, air.R(a, s, d0/2), s, v0, d0/2)
                    else:
                        ns[x][y][z] = cs[x][y][z] - a * dt *( (A - 2 * cs[x][y][z] + B)/dx**2 +(C - 2 * cs[x][y][z] + D)/dy**2 + 
                        (E - 2 * cs[x][y][z] + F)/dz**2 ) - dt * cold_q / (rho * Cp) + dt * hot_q / (rho * Cp)
                    new_value = ns[x][y][z]

                    new_T_list.append(new_value)

        cs = ns.copy()
        #print(new_T_list)
        df['moment ' + str(t) + ' T'] = new_T_list.copy() #以一维形式传回到dataframe方便可视化

    return df