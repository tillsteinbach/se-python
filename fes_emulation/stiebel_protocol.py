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

    def makeStiebelMessage(msg: Message):
        operationType = OperationType(msg.data[0] & 0x0F)
        if operationType == OperationType.REQUEST:
            return StiebelRequestMessage(msg)
        elif operationType == OperationType.RESPONSE:
            return StiebelResponseMessage(msg)
        elif operationType == OperationType.WRITE:
            return StiebelWriteMessage(msg)
        elif operationType == OperationType.REGISTER:
            return StiebelRegisterMessage(msg)
        return None

    def __init__(self, msg: Message):
        self.source = Source(msg.arbitration_id)
        self.operation_target = OperationTarget(msg.data[0] >> 4)
        self.operation_subtarget = msg.data[1]
        self.operation_type = OperationType(msg.data[0] & 0x0F)
        self.variable = msg.data[2]
        self.variable_extension = (msg.data[3] << 8) | msg.data[4]


class StiebelRequestMessage(StiebelMessage):
    def __init__(self, msg: Message):
        super().__init__(msg)

    def __str__(self) -> str:
        return self.operation_type.name+": "+self.source.name+" -> "+self.operation_target.name+" "+str(self.operation_subtarget) \
                +" ("+hex(self.operation_subtarget)+") Variable: "+hex(self.variable)+" Variable extenson: "+hex(self.variable_extension)


class StiebelValueMessage(StiebelMessage):
    def __init__(self, msg: Message):
        super().__init__(msg)
        self.value = (msg.data[5] << 8) | msg.data[6]

    def __str__(self) -> str:
        return self.operation_type.name+": "+self.source.name+" -> "+self.operation_target.name+" "+str(self.operation_subtarget) \
                +" ("+hex(self.operation_subtarget)+") Variable: "+hex(self.variable)+" Variable extenson: "+hex(self.variable_extension)+" Value: "+str(self.value)+" ("+hex(self.value)+")"


class StiebelResponseMessage(StiebelValueMessage):
    def __init__(self, msg: Message):
        super().__init__(msg)


class StiebelWriteMessage(StiebelValueMessage):
    def __init__(self, msg: Message):
        super().__init__(msg)


class StiebelRegisterMessage(StiebelMessage):
    def __init__(self, msg: Message):
        super().__init__(msg)
