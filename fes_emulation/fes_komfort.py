from can.listener import Listener
from can.message import Message


class FESKomfort(Listener):
    roomTemperature = 20.0
    roomHumidity = 50.0
    canBus = None

    def __init__(self, canBus):
        self.canBus = canBus


    def on_message_received(self, msg: Message):
        pass

    def sendTemperature(self):
        