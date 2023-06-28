from spatialmath import SE3
from roboticstoolbox.models.DH import Panda
from roboticstoolbox import DHRobot
from roboticstoolbox.tools import ctraj,jtraj
import numpy as np
import os


class gantry():
    def __init__(self,q0 = None):
        super().__init__()
        
        if(q0 == None):
            self.q0 = [0.]*5
        else:
            self.q0 = q0
        self.q = self.q0
        self.p = self.fk_pos(self.q)
        
        self.set_q(self.q,1)
    
    def fk_pos(self, q):
        p = [0., 0., 0.]
        p[0] = q[2]
        p[1] = q[3]
        p[2] = q[4]
        return p
    
    def string_q(self, q):
        s=''
        for value in q:
            s+=str(value)+' '
        return s
    
    def string_qs(self, qs):
        s=''
        for q in qs:
            q_filtered = q[2:]
            for value in q_filtered:
                s+=str(value)+' '
        return s

    def execute_plan(self,cfg_plan,t): # t is the time duration we want  
        n = len(cfg_plan)
        print("cfg plan length: ", n)
        dt = t/n
        os.system(f'ros2 run gantry_test multi_point_controller {n} {int(dt*1e9)} {self.string_qs(cfg_plan)}')
        
    def set_q(self, q, t):
        os.system(f'ros2 run chess_manipulator multi_point_controller 1 {int(t*1e9)} {self.string_q(q)} ')        
            
if __name__ == '__main__':
    robot = gantry()

