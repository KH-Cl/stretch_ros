class CommandMode:
    POSITIONAL = 'p'
    INCREMENTAL = 'i'

class JointCommand:
    def __init__(self, command_mode=CommandMode.POSITIONAL, command_value: float =0.0) -> None:
        self.command_mode = command_mode
        self.command_value = command_value

    def get_command_mode(self):
        return self.command_mode

    def set_command_mode(self, command_mode):
        # TODO: raise exception if invalid command mode
        if command_mode not in [CommandMode.POSITIONAL, CommandMode.INCREMENTAL]: return
        self.command_mode = command_mode

    def get_command_value(self):
        return self.command_value

    def set_command_value(self, command_value: float):
        self.command_value = command_value

    def get_command_value_mode(self):
        return self.command_value, self.command_mode

    def __str__(self):
        return str(self.command_value) + self.command_mode
    
    def __eq__(self, other):
        if (not isinstance(other, JointCommand)): return False
        if (self.get_command_mode() != other.get_command_mode()): return False
        if (self.get_command_value() != other.get_command_value()): return False

        return True