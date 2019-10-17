import asyncio
import time
from obniz import Obniz

obniz = Obniz('15696177')


# async def write_data_peripheral(service):
#     time.sleep(10)
#     print(write_data_peripheral)
#
#     service.write(0x64)
#     service.notify()


# def print_temp(temp):
#     print(temp)


async def onconnect(obniz):
    obniz.display.clear()
    obniz.display.print("Hello, World!")

    new_service = obniz.ble.service({
        'uuid': '555a0001-0aaa-467a-9538-01f0652c74e8'
    })
    new_characteristic = obniz.ble.characteristic({
        'uuid': '555a0003-0aaa-467a-9538-01f0652c74e8',
        'properties': ['write', 'read', 'notify'],  # propertiesの設定を追加してください
        'data': [0x00, 0x64],
        'descriptors': [{
            'uuid': '2902',
            'data': [0x00, 0x00],
        }]
    })

    new_service.add_characteristic(new_characteristic)
    obniz.ble.peripheral.add_service(new_service)

    obniz.ble.advertisement.set_adv_data(new_service.adv_data)

    # obniz.ble.advertisement.set_scan_resp_data({
    #     "localName": "obniz BLE",
    # })

    obniz.ble.advertisement.start()

    # new_characteristic.write(data=[0x00, 0x64])
    # new_characteristic.notify()



    # Obniz: {"ble": {"peripheral": {"connection_status": {"address": "61d9f9264655", "status": "connected"}}}}

    # Obniz: {"ad1": 0.61}
    # temperature_sensor = obniz.wired("LM60", {"gnd": 0, "output": 1, "vcc": 2})
    # print(temperature_sensor)

    # while True:
    #     temperature = await temperature_sensor.get_wait()
    #     print(temperature)
    #



    # https://www.autumn-color.com/archives/1591


obniz.debugprint = True
obniz.onconnect = onconnect

# asyncio.get_event_loop().create_task(onconnect(obniz))
asyncio.get_event_loop().run_forever()