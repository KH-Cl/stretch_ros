#!/usr/bin/env python3
'''
    File name: Joint.py
    Author: Pratyusha Ghosh, Alex Chow, and Arthi Haripriyan
    Email: p1ghosh@ucsd.edu
    Date created: 5/4/2022
    Date last modified: 2/12/2024
    Version: 1.0.2
    Python Version: 3
'''

class Joint:
    """
    A class that stores all the names of the joints on the Stretch robot as constants 
    as well as dictionary of range of motion for each joint (if applicable).

    These names are consistent with the Hello Robot GitHub repository.
    """
    HEAD_PAN = 'joint_head_pan'
    HEAD_TILT = 'joint_head_tilt'
    BASE_TRANSLATE = 'translate_mobile_base'
    BASE_ROTATE = 'rotate_mobile_base'
    BASE = 'base'
    LIFT = 'joint_lift'
    ARM = 'wrist_extension'
    WRIST_YAW = 'joint_wrist_yaw'
    GRIPPER = 'joint_gripper_finger_left'

    RANGE_OF_MOTION_DICT = {
        HEAD_PAN: (-2.80, 2.90),    # radians
        HEAD_TILT: (-1.60, 0.40),   # radians
        LIFT: (0.15, 0.95),         # meters
        ARM: (0.00, 0.49),          # meters
        WRIST_YAW: (-1.75, 4.00),   # radians
        GRIPPER: (-8.9, 3.69),      # radians
    }