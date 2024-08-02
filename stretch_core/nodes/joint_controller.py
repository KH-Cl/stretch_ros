#!/usr/bin/env python3
'''
    File name: JointController.py
    Author: Pratyusha Ghosh, Alex Chow, and Arthi Haripriyan
    Email: p1ghosh@ucsd.edu
    Date created: 5/4/2022
    Date last modified: 2/12/2024
    Version: 1.0.1
    Python Version: 3
'''

from joint import Joint
from joint_command_manager import JointCommandManager
from joint_command import *
import copy
from utils import Utils

# New imports
import rospy
import actionlib
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
from trajectory_msgs.msg import JointTrajectoryPoint

class JointController:
    """
    This class controls the physical Stretch joints by calling move_by or
    move_to.
    
    """

    def __init__(self, joint_commands_manager: JointCommandManager):
        self.joint_commands_map = joint_commands_manager.joint_commands_map
        self.prev_pos_joint_cmds_map = copy.deepcopy(self.joint_commands_map)
        self.trajectory_client = actionlib.SimpleActionClient('/stretch_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
        rospy.Subscriber('joint_states', JointState)
        self.interrupt_path_pub = rospy.Publisher('/funmap/interrupt_path', Bool, queue_size=1)

    def joint_state_cb(self,joint_state):
        self.joint_state = joint_state
    
    def has_command_value_changed(self, joint, curr_value):
            return curr_value != self.prev_pos_joint_cmds_map[joint]

    def increment(self, joint_points, joint, cmd_val):
        """
        If it would be within the joint's limit, increment current pose of joint by specified amount and add to
        list to be sent to stretch_driver
        :param joint_points: (JointTrajectoryPoint) contains list of joints and planned positions to be sent to action server
        :param joint: (Joint) name of current joint
        :param cmd_val: (number) amount to increment position by
        """
        if cmd_val != 0:
                curr_joint_state = self.joint_state[joint]
                if Utils.within_limits(joint, curr_joint_state + cmd_val):
                    joint_points.joint_names.append(joint)
                    joint_points.positions.append(curr_joint_state + cmd_val)
    
    def position(self, joint_points, joint, cmd_val):
        """
        If joint's command has changed, add joint and new position to list to be sent to stretch_driver
        :param joint_points: (JointTrajectoryPoint) contains list of joints and planned positions to be sent to action server
        :param joint: (Joint) name of current joint
        :param cmd_val: (number) position to move joint to
        """
        if self.has_command_value_changed(joint, cmd_val):
                joint_points.joint_names.append(joint)
                joint_points.positions.append(Utils.clamp(cmd_val))

    def control(self):
        """
        Moves each joint according to the message received. The joint commands
        are received over ROS websockets and are stored into joint_commands_map.
        It works with Hello Robot's robot APIs to move the Stretch joints.
        This is called continuously by the StretchControlEngine so that the joints move smoothly.
        Based on the value specified in the joint_commands_map, the joints will move either in
        increments or to a particular position.

        """

        joint_points = JointTrajectoryPoint()
        joint_points.time_from_start = rospy.Duration(0.0)
        # iterate through joint commands 
        for joint, joint_cmd in self.joint_commands_map.items():
            # KARA TODO: this would probably go into joint file instead but need to figure out the actual joint names that I was using
            if joint == Joint.BASE_ROTATE or joint == Joint.BASE_TRANSLATE:
                cmd_val = joint_cmd.get_command_value()
                # KARA TODO: I forget how I did this but maybe it was this?????? I forgot this detail but it definetely wasn't like increment
                self.position(joint_points, joint, cmd_val)
            else:    
                cmd_val, cmd_mode = joint_cmd.get_command_value_mode()
                if cmd_mode == CommandMode.INCREMENTAL:
                    self.increment(joint_points, joint, cmd_val)
                elif cmd_mode == CommandMode.POSITIONAL:
                    self.position(joint_points, joint, cmd_val)

        # if there are commands to send to action server
        if len(joint_points) > 0:
            # send signal to interrupt any path currently being taken
            self.interrupt_path_pub.publish(True)

            trajectory_goal = FollowJointTrajectoryGoal()
            trajectory_goal.goal_time_tolerance = rospy.Time(1.0)
            trajectory_goal.trajectory.header.stamp = rospy.Time.now()
            trajectory_goal.trajectory.points = [joint_points]
            self.trajectory_client.send_goal(trajectory_goal)