#!/usr/bin/env python3
'''
    File name: Utils.py
    Author: Pratyusha Ghosh, Alex Chow, and Arthi Haripriyan
    Email: p1ghosh@ucsd.edu
    Date created: 5/4/2022
    Date last modified: 2/12/2024
    Version: 1.0.1
    Python Version: 3
'''

from joint import Joint

class Utils:
    """
    A class that contains general utility functions.
    """

    @staticmethod
    def find_value_by_key(dictionary, target_key):
        """
        A function that extracts a value from a dictionary mapped to target_key.
        
        If there is a key in the first level of the dictionary, then return that value.
        Otherwise, recurse and go in a level deeper and try to find it there.
        If the target_key is not found anywhere, return None

        :param dictionary: the dictionary to find target_key in
        :param target_key: the target key to be searched for in the dictionary
        :returns: the value mapped to target_key. None if key does not exist
        """
        if not dictionary or not target_key or not type(dictionary) == dict: return None
        if target_key in dictionary: return dictionary[target_key]

        for key in dictionary:
            value = Utils.find_value_by_key(dictionary[key], target_key)
            if value is not None: return value
        
        return None
    
    @staticmethod
    def within_limits(joint, value):
        """
        :param joint: the joint name as specified in Joint.py
        :returns: whether or not the value is within allowed limits of the specific joint
        """
        lower, upper = Joint.RANGE_OF_MOTION_DICT[joint]
        return lower <= value <= upper
    
    @staticmethod
    def clamp(joint, value):
        """
        :param joint: the joint name as specified in Joint.py
        :returns: value clipped to within allowed limits of the specific joint
        """
        lower, upper = Joint.RANGE_OF_MOTION_DICT[joint]
        return max(lower, min(upper, value))