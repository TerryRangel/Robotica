"""Pentagrama controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()


r=0.195/2
L=0.35

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())
left_wheel = wb_robot_get_device("left wheel");
right_wheel = wb_robot_get_device("right wheel");


left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))

left_wheel.setVelocity(0.0)
right_wheel.setVelocity(0.0)

v=1.0
omega=0.0
  
  
  
# Main loop:
# - perform simulation steps until Webots is stopping the controller

for i in range (5):
    tiempo = robot.getTime()
    while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
