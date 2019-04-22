# ArduCAMMini

ArduCAM Mini works with few pins.
It takes image with many image resolutions and alos jpeg format.

ArduCam Mini has many series of product. This library is only for OV2640 2M pixel ArduCam.

![](./image.jpg)


## wired(obniz,  {cs [, mosi, miso, sclk, gnd, vcc, sda, scl, spi, i2c]} )

Instantiate camera object regarding ios.

We recommend to supply power to an arducam from other power resource.
You should pay attention over current detection when using an obniz as poewr supply.
Supply methods are


- use other power resource
- use J1 on an obniz.
- supply vcc more than two obniz io

This document use io5 and io11 to supply a vcc.

![](./wire.jpg)

Arducam require each SPI and I2C.

name | type | required | default | description
--- | --- | --- | --- | ---
cs | `number(obniz io)` | yes | &nbsp | obniz io. チップ選択
vcc | `number(obniz io)` | no | &nbsp | obniz io. 電源 +5V
gnd | `number(obniz io)` | no | &nbsp | obniz io. 電源 0v
mosi | `number(obniz io)` | no | &nbsp | obniz io. SPI mosi 端子
miso | `number(obniz io)` | no | &nbsp | obniz io. SPI miso 端子
sclk | `number(obniz io)` | no | &nbsp | obniz io. SPI clk 端子
sda | `number(obniz io)` | no | &nbsp | obniz io. I2C sda 端子
scl | `number(obniz io)` | no | &nbsp | obniz io. I2C scl 端子
i2c | `i2c object` | no | &nbsp | configured i2c object
spi | `spi object` | no | &nbsp | configured spi object
spi_frequency | `spi object` | no | 4Mhz | for unstable situation, change frequency of spi
spi_drive | `spi object` | no | `'3v'` | for unstable situation, change drive method of spi

Just specify connected io to configure.

```Python
# Python Example
from obniz import Obniz

obniz = Obniz("OBNIX_ID_HERE")
async def onconnect():
    obniz.io11.output(True)
    cam = obniz.wired("ArduCAMMini", {
        "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
    })
    await cam.startup_wait()
    data = await cam.take_wait('1024x768')
    print("image size = ", len(data), " bytes")
    base64 = cam.array_to_base64(data)

obniz.onconnect = onconnect
```

Or, specify configured i2c and spi object to wired function.


## [await] startup_wait()

Initialize and test a cam.
You should call this function only once before take.

This function does

- SPI communication test
- I2C communication test
- camera suppported check
- mode and jpeg configration
- 320x240 resolution setting

After this startup, take_wait() can be called to take.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
```

Without calling startup_wait(), you can configure manually like below.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.spi_pingpong_wait()
cam.set_mode('MCU2LCD')
chipid = await cam.get_chip_id_wait()
if chipid != 0x2642:
    raise Exception('unknown chip ' + str(chipid))

cam.init()
```


## [await] take_wait(size)

Getting jpeg image data from a cam.
Please call startup_wait() function before take.

Set size to change resolution from default(320*240).
Not specified or specified size is same as before will change nothing.
Size options are same sas set_size() function.

Return value is array(list) of jpeg image.
If it fail, this function throws a error or hang to wait a response form a cam.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
jpeg_data = await cam.take_wait('1024x768')
```

You can take a photo manually without using take_wait(). Please refer start_capture() function.

## array_to_base64(list)
convert list to base64 string.
It is useful when you want to print image to image tag.

```Python
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
jpeg_data = await cam.take_wait('1024x768')
print("image size = ", len(jpeg_data), " bytes")
  
base64 = cam.array_to_base64(jpeg_data)
```

## set_mode(mode)

Configation of  camera mode.
options are below.

This function is used in startup_wait() function.

- 'MCU2LCD'
- 'CAM2LCD'
- 'LCD2MCU'

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
cam.set_mode('MCU2LCD')
```

## [await] spi_pingpong_wait()

Testing a cam and obniz spi communication.
Use this to check cam power supply correction and wiring check.

This function is used in startup_wait() function.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.spi_pingpong_wait()
```

## [await] get_chip_id_wait()

Retriving a chip id by using I2C communication
Use this to check I2C communication and validation of chip id.

This function is used in startup_wait() function.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
chipid = await cam.get_chip_id_wait()
if chipid != 0x2642:
  raise Exception('unknown chip ' + str(chipid))
```

## init()

Initialize a cam.
It does basic initialization. Jpeg mode, and resolution set to 320*240.

This function is used in startup_wait() function.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
cam.set_mode('MCU2LCD')
cam.init()
```

## set_size(size)

Setting a resolution of cam.
Options are

- '160x120'
- '176x144'
- '320x240'
- '352x288'
- '640x480'
- '800x600'
- '1024x768'
- '1280x960'
- '1600x1200'

ArduCam says 1sec waiting is recommended after configrations of size.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.set_size('1600x1200')
await obniz.wait(1000)
```

## flush_fifo()

Clearing FIFO.
You should call twice before calling start_capture().

This function is used in take_wait() function.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```

## start_capture()

Starting a photo taking.
It takes a time. You should wait. Use is_capture_done_wait() function to check it done.

This function is used in take_wait() function.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```

## [await] is_capture_done_wait()

Checking photo taking is done or not.

This function is used in take_wait() function.

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```

## [await] readFIFOWait()

Getting a data in camera FIFO.

This function is used in take_wait() function.


```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```