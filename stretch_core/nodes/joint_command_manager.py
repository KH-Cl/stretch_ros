#!/usr/bin/env python3
'''
    File name: JointCommandManager.py
    Author: Pratyusha Ghosh, Alex Chow, and Arthi Haripriyan
    Email: p1ghosh@ucsd.edu
    Date created: 5/4/2022
    Date last modified: 2/12/2024
    Version: 1.0.1
    Python Version: 3
'''

from joint import Joint
from joint_command import *

class JointCommandManager:
    """
    A class that initializes and updates the commands to move each joint.
    """
    def __init__(self):
        self.joint_commands_map = {
            Joint.HEAD_PAN: JointCommand(),
            Joint.HEAD_TILT: JointCommand(),
            Joint.BASE_TRANSLATE: JointCommand(),
            Joint.BASE_ROTATE: JointCommand(),
            Joint.WRIST_YAW: JointCommand(),
            Joint.LIFT: JointCommand(command_value=0.5),
            Joint.GRIPPER: JointCommand(),
            Joint.ARM: JointCommand()
        }

    def set_joint_command_mode(self, joint, command_mode):
        self.joint_commands_map[joint].set_command_mode(command_mode)

    def set_joint_command_modes(self, joints, command_modes):
        for joint, command_mode in zip(joints, command_modes):
            self.set_joint_command_mode(joint, command_mode)

    def init_joint_positions(self, joint_state_msg):
        """
        Initializes positions for the position-based joints (the lift, gripper, and arm) 
        to match the current Stretch joint positions.

        :param joint_state_msg: the joint states from the Stretch
        """
        self.joint_commands_map[Joint.LIFT].set_command_value(joint_state_msg.position[2])
        self.joint_commands_map[Joint.GRIPPER].set_command_value(joint_state_msg.position[4])
        self.joint_commands_map[Joint.ARM].set_command_value(joint_state_msg.position[5])

    
    def handle_command(self, data):
        """
        Handle commands for moving Stretch joints.

        :param data: the message that contains the command string
        """
        commands = self._deserialize(data)
        self._update_joint_commands_map(commands)


    def _deserialize(self, message):
        """
        Deserialize a command string into a Python dictionary of joint names
        to command values.

        :param message: the message list of SingleJointCommands
        """
        joint_commands = {}
        for single_joint_command in message.joint_commands:
            joint_name = single_joint_command.joint_name
            command_value = single_joint_command.command_value
            command_mode = single_joint_command.command_mode
            joint_commands[joint_name] = JointCommand(command_mode, command_value)
        
        return joint_commands
    

    def _update_joint_commands_map(self, joint_commands_map):
        """
        Updates joint commands map from deserialized commands map.

        :param joint_commands_map: deserialized commands map
        """
        for joint, joint_command in joint_commands_map.items():
            command_value, command_mode = joint_command.get_command_value_mode()
            self.joint_commands_map[joint].set_command_mode(command_mode)
            self.joint_commands_map[joint].set_command_value(command_value)