
import numpy as np
import RobotClass
import sys



num_stacks = 3
basefile_name = f'/home/lee/parasol/multi-robot-experiments/gantry_stack/stacks_{num_stacks}/'
data_gantry = np.loadtxt(basefile_name+'NBS-31163221::FinalPath::gantry_0')
plan = data_gantry
print(plan)

robot = RobotClass.gantry()

def main():
    robot.execute_plan(plan,60)
    

if __name__ == '__main__':
    main()
    

