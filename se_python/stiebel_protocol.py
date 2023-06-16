from can.message import Message
from enum import Enum

from se_python.se_variables import SEVariable


class DeviceType(Enum):
    HEATPUMP = 3
    UNKNOWN2 = 4
    HEATCIRCLE = 6
    SENSOR = 8
    UNKNOWN4 = 9
    UNKNOWN = 10
    UNKNOWN3 = 12
    DISPLAY = 13


class OperationType(Enum):
    WRITE = 0
    REQUEST = 1
    RESPONSE = 2
    REGISTER = 6


class StiebelMessage():
    source = None
    target = None
    operation_type = None
    variable = None
    variable_extension = None

    def fromCanMessage(msg: Message):
        stiebelMessage = None
        source = (DeviceType(msg.arbitration_id >> 7), msg.arbitration_id & 0x7F)
        target = (DeviceType(msg.data[0] >> 4), (msg.data[1]))
        operationType = OperationType(msg.data[0] & 0x0F)
        variable = SEVariable(msg.data[2])
        variableExtension = SEVariable((msg.data[3] << 8) | msg.data[4])
        value = (msg.data[5] << 8) | msg.data[6]
        if operationType == OperationType.REQUEST:
            stiebelMessage = StiebelRequestMessage(source, target, operationType, variable, variableExtension)
        elif operationType == OperationType.RESPONSE:
            stiebelMessage = StiebelResponseMessage(source, target, operationType, variable, variableExtension, value)
        elif operationType == OperationType.WRITE:
            stiebelMessage = StiebelWriteMessage(source, target, variable, variableExtension, value)
        elif operationType == OperationType.REGISTER:
            stiebelMessage = StiebelRegisterMessage(source, target, operationType, variable, variableExtension)
        return stiebelMessage

    def toCanMessage(msg):
        data = [0, 0, 0, 0, 0, 0, 0]

        data[0] = (msg.target[0].value << 4) | msg.operation_type.value
        data[1] = msg.target[1]
        data[2] = msg.variable.value
        data[3] = msg.variable_extension.value >> 8
        data[4] = msg.variable_extension.value & 0xFF
        if isinstance(msg, StiebelValueMessage):
            data[5] = msg.value >> 8
            data[6] = msg.value & 0xFF
        canMessage = Message(arbitration_id=(msg.source[0].value << 7) | (msg.source[1]),
                             is_extended_id=False,
                             is_remote_frame=False,
                             is_error_frame=False,
                             data=data,
                             dlc=7)
        return canMessage

    def __init__(self, source, target, operation_type: OperationType, variable, variable_extension):
        self.source = source
        self.target = target
        self.operation_type = operation_type
        self.variable = variable
        self.variable_extension = variable_extension


class StiebelRequestMessage(StiebelMessage):
    def __str__(self) -> str:
        return self.operation_type.name+": "+self.source[0].name+":"+str(self.source[1])+" -> "+self.target[0].name+":"+str(self.target[1]) \
                + " Variable: "+self.variable.name+" Variable extenson: "+self.variable_extension.name
    


class StiebelValueMessage(StiebelMessage):
    def __init__(self, source, target, operation_type: OperationType, variable, variable_extension, value):
        super().__init__(source, target, operation_type, variable, variable_extension)
        self.value = value

    def __str__(self) -> str:
        return self.operation_type.name+": "+self.source[0].name+":"+str(self.source[1])+" -> "+self.target[0].name+":"+str(self.target[1]) \
                +" Variable: "+self.variable.name+" Variable extenson: "+self.variable_extension.name+" Value: "+str(self.value)+" ("+hex(self.value)+")"


class StiebelResponseMessage(StiebelValueMessage):
    pass


class StiebelWriteMessage(StiebelValueMessage):
    def __init__(self, source, target, variable, variable_extension, value):
        super().__init__(source, target, OperationType.WRITE, variable, variable_extension, value)


class StiebelRegisterMessage(StiebelMessage):
    pass
