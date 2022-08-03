from gym import Env
from gym.spaces.discrete import Discrete
from gym.spaces import Box, Dict, Discrete, MultiDiscrete
import numpy as np
from models.System_Models import Chiller, Tower, Pump, Fan, Exchanger, AHU
from models.Environment_Models import Air_Node, Water_Node, Room, Outdoor

from stable_baselines3 import PPO 

from stable_baselines3.common.vec_env import dummy_vec_env

from stable_baselines3.common.policies import BasePolicy 

from stable_baselines3.common.env_checker import check_env

import random

import streamlit as st

class GuBeiEnv(Env):
    def __init__(self):
        self.architecture() #结构声明下
        self.action_space = MultiDiscrete([3 for _ in  [ 'LS_A1_r', 'LS_A2_r','LS_A1_Te', 'LS_A2_Te', 'LD_A1_G', 'LD_A2_G', 'LQ_A1_G', 'LQ_A2_G']])# action space to be discrete, 
        # 1 integer at a time
        #action inputs shall vary according to a specific percentage range of each device's capacity

        #先只管冷冻水
       # for device in [ 'LS_A1_r', 'LS_A2_r','LS_A1_Te', 'LS_A2_Te', 'LD_A1_G', 'LD_A2_G', 'LQ_A1_G', 'LQ_A2_G']: #假设 LD_Ai_G和LT_Ai_G相同

        #    self.action_space[device] = Discrete(101) #百分比频率值

        #出水温度，压缩机功率，冷冻泵功率，冷却泵功率
        self.observation_space = Box(low = np.array([0, 0, 0, 0]),
        high = np.array([35, np.inf, np.inf, np.inf]),
        shape = (4,),
        dtype = np.float64
        )
        self.state = [20, 0, 0, 0]

        self.duration_length = 10 # 10个小时，或者分钟或者半小时/ 看古北路系统情况

        self.r1 = 0.5
        self.r2 = 0.5

        self.G_w_e_1 = 160.2
        self.G_w_e_2 = 160.2

        self.Te1 = 24
        self.Te2 = 24

        self.T_tower_w_E_1 = 26 #假设水塔进出固定设定温度
        self.T_tower_w_L_1 = 23

        self.T_tower_w_E_2 = 26 #假设水塔进出固定设定温度
        self.T_tower_w_L_2 = 23

        self.G_w_c_1 = 160.2
        self.G_w_c_2 = 160.2




    def step(self, action): #环境反馈，包含室外情况 + 经过ahu换热后的回水温度 + 新的负荷需求
        #feed_back = {'hall_Q', 'platform_Q', 'ahu_1_T_w_L', 'ahu_2_T_w_L', 'G_tower_a', 'h_a_E', 'h_as_E'  }
        '''
        
        if feed_back['hall_Q'] + feed_back['platform_Q'] < 0.85 * self.Chiller_LS_A1.Qe_max:
    
            self.Chiller_LS_A1.T_w_e_E = 0.5 * (feed_back['ahu_1_T_w_L'] + feed_back['ahu_2_T_w_L'])
            self.Chiller_LS_A1.Qe = feed_back['hall_Q'] + feed_back['platform_Q']

            G_w_e = action['LD_A1_G']/100 * 320.5 #t/h
            self.Cooling_Pump_LD_A1.run_pump(G_w_e)

            self.Chiller_LS_A1.G_w_e = self.Cooling_Pump_LD_A1.flow_rate
            self.Tower_LT_A1 = self.Cooling_Pump_LD_A1.flow_rate

            r1 = self.Chiller_LS_A1.Qe / self.Chiller_LS_A1.Qe_max

            Te = action['LS_A1_Te'] * 35

            T_tower_w_E = 26 #假设水塔进出固定设定温度
            T_tower_w_L = 23

            G_w_c = action['LQ_A1_G'] * 320.5

            self.Chilled_Pump_LQ_A1.run_pump(G_w_c)
            
            self.Chiller_LS_A1.simple_run(r1, Te, T_tower_w_E, T_tower_w_L)
        
        '''
        
        #elif feed_back['hall_Q'] + feed_back['platform_Q'] >= self.Chiller_LS_A1 * 0.85:
        
        #不考虑负载调配策略

        self.hall_Q = [ 300 + random.randint(-100, 100) for i in range(self.duration_length) ] 
        self.platform_Q = [ 300 + random.randint(-100, 100) for i in range(self.duration_length) ]
        self.ahu_1_T_w_L = [28 + random.randint(-3, 3) for i in range(self.duration_length)]
        self.ahu_2_T_w_L = [28 + random.randint(-3, 3) for i in range(self.duration_length)]

        feed_back = {
            'ahu_1_T_w_L': self.ahu_1_T_w_L,
            'ahu_2_T_w_L': self.ahu_2_T_w_L,
            'hall_Q': self.hall_Q,
            'platform_Q': self.platform_Q,
        }

        #[ 'LS_A1_r', 'LS_A2_r','LS_A1_Te', 'LS_A2_Te', 'LD_A1_G', 'LD_A2_G', 'LQ_A1_G', 'LQ_A2_G']

        self.duration_length -= 1
        
        self.r1 += (action[0] - 1) / 100
        self.r2 += (action[1] - 1) / 100
        #可能需要结合上一时刻的陆良来统计分配均值权重
        self.Chiller_LS_A1.T_w_e_E = 0.5 * (feed_back['ahu_1_T_w_L'][self.duration_length] + feed_back['ahu_2_T_w_L'][self.duration_length])
        self.Chiller_LS_A1.Qe = self.r1 * (feed_back['hall_Q'][self.duration_length] + feed_back['platform_Q'][self.duration_length])

        self.Chiller_LS_A2.T_w_e_E = 0.5 * (feed_back['ahu_1_T_w_L'][self.duration_length] + feed_back['ahu_2_T_w_L'][self.duration_length])
        self.Chiller_LS_A2.Qe = self.r2 * (feed_back['hall_Q'][self.duration_length] + feed_back['platform_Q'][self.duration_length])

        self.G_w_e_1 += (action[4] - 1) / 100 * 320.5
        self.G_w_e_2 += (action[5] - 1) / 100 * 320.5

        self.Cooling_Pump_LD_A1.run_pump(self.G_w_e_1)
        self.Cooling_Pump_LD_A2.run_pump(self.G_w_e_2)

        self.Chiller_LS_A1.G_w_e = self.Cooling_Pump_LD_A1.flow_rate
        self.Chiller_LS_A2.G_w_e = self.Cooling_Pump_LD_A2.flow_rate


        self.Tower_LT_A1.G_w = self.Cooling_Pump_LD_A1.flow_rate
        self.Tower_LT_A2.G_w = self.Cooling_Pump_LD_A2.flow_rate

        self.Te1 += (action[2] - 1) / 100 * 35
        self.Te2 += (action[3] - 1) / 100 * 35

        self.G_w_c_1 += (action[6] - 1) / 100 * 320.5
        self.G_w_c_2 += (action[7] - 1) / 100 * 320.5

        self.Chiller_LS_A1.G_w_c = self.G_w_c_1
        self.Chiller_LS_A2.G_w_c = self.G_w_c_2

        self.Chiller_LS_A1.Tower = self.Tower_LT_A1 
        self.Chiller_LS_A2.Tower = self.Tower_LT_A2

        self.Chilled_Pump_LQ_A1.run_pump(self.G_w_c_1)
        self.Chilled_Pump_LQ_A2.run_pump(self.G_w_c_2)

        self.Chiller_LS_A1.simple_run(self.r1, self.Te1, self.T_tower_w_E_1, self.T_tower_w_L_1)
        self.Chiller_LS_A2.simple_run(self.r2, self.Te2, self.T_tower_w_E_2, self.T_tower_w_L_2)
        
        self.state[0] = 0.5 * (self.Chiller_LS_A1.T_w_e_L + self.Chiller_LS_A2.T_w_e_L) #出水温度
        self.state[1] = self.Chiller_LS_A1.Ncom + self.Chiller_LS_A2.Ncom #冷水机组能耗
        self.state[2] = self.Cooling_Pump_LD_A1.Npump + self.Cooling_Pump_LD_A2.Npump #冷冻泵能耗
        self.state[3] = self.Chilled_Pump_LQ_A1.Npump + self.Chilled_Pump_LQ_A2.Npump #冷却泵能耗
        self.state = np.array(self.state)
        reward = 0

        if self.state[0] < 29:
            reward += 1
        else:
            reward -= 1

        if self.state[1] < 800:
            reward += 1
        else:
            reward -= 1

        if self.state[2] < 500:
            reward += 1
        else: 
            reward -= 1
    
        if self.state[3] < 500:
            reward += 1
        else: 
            reward -= 1

        if self.duration_length <= 0:
            done = True
        else:
            done = False

        info = {}

        return self.state, reward, done, info

    def architecture(self):
        pumping_head = 10 #m?
        Chiller_Evaporator_Cooling_Rate = 666 #kW
        self.Chiller_LS_A1 = Chiller(Chiller_Evaporator_Cooling_Rate)
        self.Chiller_LS_A2 = Chiller(Chiller_Evaporator_Cooling_Rate)

        self.Chiller_LS_A1.T_w_e_E = 12
        self.Chiller_LS_A2.T_w_e_E = 12
        self.Chiller_LS_A1.T_w_e_L = 7
        self.Chiller_LS_A2.T_w_e_L = 7

        self.Chiller_LS_A1.T_w_c_E = 32
        self.Chiller_LS_A2.T_w_c_E = 32
        self.Chiller_LS_A1.T_w_c_L = 37
        self.Chiller_LS_A2.T_w_c_L = 37

        #得有cooling pump和chilled pump
        #额定还是设计还是最小还是某频率下的？
        Cooling_Pump_G = 320.5 #t/h/
        Chilled_Pump_G = 320.5 #t/h
        self.Cooling_Pump_LD_A1 = Pump(pumping_head)
        self.Cooling_Pump_LD_A2 = Pump(pumping_head)
        self.Cooling_Pump_LD_A1.flow_rate = Cooling_Pump_G
        self.Cooling_Pump_LD_A2.flow_rate = Cooling_Pump_G

        self.Chilled_Pump_LQ_A1 = Pump(pumping_head)
        self.Chilled_Pump_LQ_A2 = Pump(pumping_head)
        self.Chilled_Pump_LQ_A1.flow_rate = Chilled_Pump_G
        self.Chilled_Pump_LQ_A2.flow_rate = Chilled_Pump_G

        self.Tower_LT_A1 = Tower()
        self.Tower_LT_A2 = Tower()

        self.Tower_LT_A1.Pump = Pump(pumping_head)
        self.Tower_LT_A2.Pump = Pump(pumping_head)

        self.Water_Distributor = Water_Node()

        self.Outdoor_Tower = Outdoor()

    def render(self):
        pass

    def reset(self):
        self.state = np.array([24, 0, 0, 0])

        self.duration_length = 10 # 10个小时，或者分钟或者半小时/ 看古北路系统情况

        return self.state

def app():
    st.markdown('# Gym Training and Modelling')
    st.write('Train a reinforcement learning agent and watches as it learn and execute system control performances')
    env = GuBeiEnv()
    check_env(env)
    env = GuBeiEnv()

    st.markdown('## Learning Settings')
    policy = st.selectbox('Choose a RL policy', (['MlpPolicy']))
    model = PPO(policy = policy, env = env, verbose = 1)

    learn_steps = st.number_input('number of learning timesteps', value = 10, step = 10)

    model.learn(total_timesteps= learn_steps)

    obs = env.reset()

    actions = []
    observations = []
    rewards = []
    for i in range(100):
        #print(i)
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)

        #环境效应方案1
            #后续要将其它被动参数放入env.state/obs中，可以在env里头设定一个物理引擎，然后在这个外部循环引进被动参数或者环境参数的真实值
            # obs的部分参数 与 what we really got参数数值相互对比，误差可以反馈给env的物理引擎使其可以自我纠正
        #方案2
            #将feedback作为环境反馈代表，每次预测一部分需求和回水温度，然后学习一次，或者每学习

        actions.append(action)
        observations.append(obs)
        rewards.append(reward)

        env.render()
        if done:
            obs = env.reset()
        
    env.close()
    st.markdown('## Observation')
    st.write(observations)
