from can.message import Message
from enum import Enum


class Source(Enum):
    HEATPUMP = 0x180
    UNKNOWN_3 = 0x200
    HEATCIRCLE_1 = 0x301
    HEATCIRCLE_2 = 0x302
    SENSOR_0 = 0x401
    SENSOR_1 = 0x402
    SENSOR_2 = 0x403
    SENSOR_3 = 0x404
    UNKNOWN_0 = 0x480
    UNKNOWN_1 = 0x601
    UNKNOWN_2 = 0x602
    DISPLAY_0 = 0x69E
    DISPLAY_1 = 0x69F
    DISPLAY_2 = 0x6A0
    DISPLAY_3 = 0x6A1
    DISPLAY_4 = 0x6A2


class OperationTarget(Enum):
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
    operation_target = None
    operation_type = None
    operation_subtarget = None
    variable = None
    variable_extension = None

    def fromCanMessage(msg: Message):
        stiebelMessage = None
        source = Source(msg.arbitration_id)
        operationTarget = OperationTarget(msg.data[0] >> 4)
        operationSubtarget = msg.data[1]
        operationType = OperationType(msg.data[0] & 0x0F)
        variable = msg.data[2]
        variableExtension = (msg.data[3] << 8) | msg.data[4]
        value = (msg.data[5] << 8) | msg.data[6]
        if operationType == OperationType.REQUEST:
            stiebelMessage = StiebelRequestMessage(source, operationTarget, operationSubtarget, operationType, variable, variableExtension)
        elif operationType == OperationType.RESPONSE:
            stiebelMessage = StiebelResponseMessage(source, operationTarget, operationSubtarget, operationType, variable, variableExtension, value)
        elif operationType == OperationType.WRITE:
            stiebelMessage = StiebelWriteMessage(source, operationTarget, operationSubtarget, variable, variableExtension, value)
        elif operationType == OperationType.REGISTER:
            stiebelMessage = StiebelRegisterMessage(source, operationTarget, operationSubtarget, operationType, variable, variableExtension)
        return stiebelMessage

    def toCanMessage(msg):
        data = [0, 0, 0, 0, 0, 0, 0]

        data[0] = (msg.operation_target.value << 4) | msg.operation_type.value
        data[1] = msg.operation_subtarget
        data[2] = msg.variable
        data[3] = msg.variable_extension >> 8
        data[4] = msg.variable_extension & 0xFF
        if isinstance(msg, StiebelValueMessage):
            data[5] = msg.value >> 8
            data[6] = msg.value & 0xFF
        canMessage = Message(arbitration_id=msg.source.value,
                             is_extended_id=False,
                             is_remote_frame=False,
                             is_error_frame=False,
                             data=data,
                             dlc=7)
        return canMessage

    def __init__(self, source: Source, operation_target: OperationTarget, operation_subtarget, operation_type: OperationType, variable, variable_extension):
        self.source = source
        self.operation_target = operation_target
        self.operation_subtarget = operation_subtarget
        self.operation_type = operation_type
        self.variable = variable
        self.variable_extension = variable_extension


class StiebelRequestMessage(StiebelMessage):
    def __str__(self) -> str:
        return self.operation_type.name+": "+self.source.name+" -> "+self.operation_target.name+" "+str(self.operation_subtarget) \
                +" ("+hex(self.operation_subtarget)+") Variable: "+hex(self.variable)+" Variable extenson: "+hex(self.variable_extension)


class StiebelValueMessage(StiebelMessage):
    def __init__(self, source: Source, operation_target: OperationTarget, operation_subtarget, operation_type: OperationType, variable, variable_extension, value):
        super().__init__(source, operation_target, operation_subtarget, operation_type, variable, variable_extension)
        self.value = value

    def __str__(self) -> str:
        return self.operation_type.name+": "+self.source.name+" -> "+self.operation_target.name+" "+str(self.operation_subtarget) \
                +" ("+hex(self.operation_subtarget)+") Variable: "+hex(self.variable)+" Variable extenson: "+hex(self.variable_extension)+" Value: "+str(self.value)+" ("+hex(self.value)+")"


class StiebelResponseMessage(StiebelValueMessage):
    pass


class StiebelWriteMessage(StiebelValueMessage):
    def __init__(self, source: Source, operation_target: OperationTarget, operation_subtarget, variable, variable_extension, value):
        super().__init__(source, operation_target, operation_subtarget, OperationType.WRITE, variable, variable_extension, value)


class StiebelRegisterMessage(StiebelMessage):
    pass
