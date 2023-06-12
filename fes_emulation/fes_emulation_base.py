import asyncio
from xknx import XKNX
from xknx.telegram import Telegram
from xknx.core import XknxConnectionState
from xknx.io import ConnectionConfig, ConnectionType

import can



async def telegram_received_cb(telegram: Telegram):
    print("Telegram received: {0}".format(telegram), flush=True)


async def connection_state_changed_cb(state: XknxConnectionState):
    print("Callback received with state {0}".format(state.name), flush=True)


connection_config = ConnectionConfig(
    connection_type=ConnectionType.TUNNELING_TCP,
    gateway_ip="10.11.2.200",
    individual_address="1.1.14",
)

async def main():
    #xknx = XKNX(connection_config=connection_config,
    #            telegram_received_cb=telegram_received_cb,
    #            connection_state_changed_cb=connection_state_changed_cb,
    #            daemon_mode=True)
    #await xknx.start()
    #await xknx.stop()

    bus = can.interface.Bus(bustype='InnoMaker', channel=0, bitrate=20000)
    i = 0
    while i < 10:
        recv = bus.recv(timeout=None)  # get received msg
        if recv is not None:
            print('[INFO -> Input] {}'.format(recv))
        i = i+1


asyncio.run(main())


    
