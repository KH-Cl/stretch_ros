#!/usr/bin/env python3
'''
    File name: StretchControlEngine.py
    Author: Pratyusha Ghosh, Alex Chow, and Arthi Haripriyan
    Email: p1ghosh@ucsd.edu
    Date created: 5/4/2022
    Date last modified: 4/2/2023
    Version: 1.0.1
    Python Version: 3
'''

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
#import stretch_body.robot
from joint_command_manager import JointCommandManager
from joint_controller import JointController
from stretch_control.msg import JointCommands, SingleJointCommand
#from ModeManager import ModeManager


class StretchControlEngine:
    """
    The class for handling the different moving parts of the Stretch control system.
    The program is separated into three stages: initialization, main loop, and termination.
    In the initialization stage, setup() and start() should be called in that order.
    In the main loop, control(), update(), and sleep() should be called in that order.
    In the termination phase, cleanup() should be called.
    Currently, the only object that implements the update() function is the joint_state_manager,
    which gets the most up-to-date joint states information from the Stretch and publishes it
    to the ROS topic /stretch/joint_states.
    """

    def __init__(self):
        self.rate = None
        self.joint_command_manager = None
        self.joint_controller = None

    def setup(self):
        """
        The top-level function that sets up any variables for initial configurations
        """
        # KARA NOTE: I'm leaving this here in case we do want to bring the mode manager in at some point but I'm not bringing it in now
        # self.mode_manager = ModeManager(self.robot)
        self.joint_command_manager = JointCommandManager()
        self.joint_controller = JointController(self.joint_command_manager)

    def start(self):
        """
        The top-level function that kicks off any sub-programs or nodes that
        need to be run.
        """
        rospy.Subscriber('stretch/joint_commands', JointCommands, self.handle_command)
        self.rate = rospy.Rate(15)

    def has_program_ended(self):
        """
        The helper function to check if the program has ended. Essential for
        the main loop.
        """
        return rospy.is_shutdown()

    def handle_command(self, data):
        """
        The callback function for receiving command strings to move Stretch
        joints through the ROS topic stretch/move_joints

        :param data: the message that contains the command string
        """
        self.joint_command_manager.handle_command(data)

    def control(self):
        """
        The top-level function for controlling any parts of the robot.
        It can only be controlled when the teleoperation interface is running.
        """
        # KARA NOTE: I'm leaving this here in case we do want to bring the mode manager in at some point but I'm not bringing it in now
        # if self.mode_manager.mode:
        self.joint_controller.control()

    def update(self):
        """
        The top-level function for calling the common update() function on 
        objects that define it for each iteration.
        """
        # KARA NOTE: not using this right now
        pass
        for object in self.objects:
            object.update()

    def sleep(self):
        """
        The top-level function for pausing the thread for a bit of time,
        as specified by the rate.
        """
        self.rate.sleep()

    def cleanup(self):
        """
        The unimplemented, top-level function to perform any program cleanups.
        """
        pass
