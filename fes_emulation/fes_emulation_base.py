import asyncio
#from xknx import XKNX
#from xknx.telegram import Telegram
#from xknx.core import XknxConnectionState
#from xknx.io import ConnectionConfig, ConnectionType

import can
from fes_emulation.stiebel_protocol import StiebelMessage, StiebelWriteMessage, OperationType, Source, OperationTarget



#async def telegram_received_cb(telegram: Telegram):
#    print("Telegram received: {0}".format(telegram), flush=True)


#async def connection_state_changed_cb(state: XknxConnectionState):
#    print("Callback received with state {0}".format(state.name), flush=True)


#connection_config = ConnectionConfig(
#    connection_type=ConnectionType.TUNNELING_TCP,
#    gateway_ip="10.11.2.200",
#    individual_address="1.1.14",
#)

def main():
    #xknx = XKNX(connection_config=connection_config,
    #            telegram_received_cb=telegram_received_cb,
    #            connection_state_changed_cb=connection_state_changed_cb,
    #            daemon_mode=True)
    #await xknx.start()
    #await xknx.stop()

    

    bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=20000)

    stiebelTemperature = StiebelWriteMessage(source=Source.DISPLAY_0,
                                             operation_target=OperationTarget.HEATCIRCLE,
                                             operation_subtarget=1,
                                             variable=0xFA,
                                             variable_extension=0x0011,
                                             value=270)
    try:
        print(stiebelTemperature)
        print(stiebelTemperature.toCanMessage())
        bus.send(stiebelTemperature.toCanMessage())
        print(f"Message sent on {bus.channel_info}")
    except can.CanError:
        print("Message NOT sent")
    
    stiebelFeuchte = StiebelWriteMessage(source=Source.DISPLAY_0,
                                             operation_target=OperationTarget.HEATCIRCLE,
                                             operation_subtarget=1,
                                             variable=0xFA,
                                             variable_extension=0x0075,
                                             value=500)
    try:
        print(stiebelFeuchte)
        print(stiebelFeuchte.toCanMessage())
        bus.send(stiebelFeuchte.toCanMessage())
        print(f"Message sent on {bus.channel_info}")
    except can.CanError:
        print("Message NOT sent")

    i = 0
    while True:
        recv = bus.recv(timeout=None)  # get received msg
        if recv is not None:
            stiebelMsg = StiebelMessage.fromCanMessage(recv)
            if stiebelMsg.operation_type not in [OperationType.REQUEST, OperationType.RESPONSE]:
                print(stiebelMsg)
            #print('[INFO -> Input] {}'.format(recv))
        i = i+1


#asyncio.run(main())


    
