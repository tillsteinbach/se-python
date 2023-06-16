from typing import Dict

from can.interface import Bus
from can.listener import Listener
from can.message import Message

from se_python.stiebel_protocol import StiebelMessage, StiebelValueMessage


class SEPython(Listener):
    """Main class used to interact with SE Heatpumps"""
    devices: Dict = {}
    bus:Bus = None

    def __init__(  # noqa: C901 # pylint: disable=too-many-arguments
        self,
        bustype: str='socketcan',
        channel: str='can0',
    ) -> None:
        self.bus = Bus(bustype=bustype, channel=channel, bitrate=20000)

    def on_message_received(self, msg: Message) -> None:
        """This method is called to handle the given message.

        :param msg: the delivered message
        """
        try:
            stiebelMsg = StiebelMessage.fromCanMessage(msg)
            sourceDevice = stiebelMsg.source
            if not sourceDevice in self.devices:
                self.devices[sourceDevice] = {}
            if isinstance(stiebelMsg, StiebelValueMessage):
                self.devices[sourceDevice][stiebelMsg.variable_extension] = {}

            print(stiebelMsg)
        except ValueError:
            print("Message cannot be interpreted")

    def start(self) -> None:
        while True:
            recv = self.bus.recv(timeout=None)  # get received msg
            if recv is not None:
                self.on_message_received(recv)
                #print(self.devices)

