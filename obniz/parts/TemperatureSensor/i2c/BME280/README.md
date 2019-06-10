# Temperature Sensor - BME280
Temperature / Humidity / Air pressure sensor.
Very low energy consumption and high accuracy.

![](./image.jpg)

## wired(obniz,  {[vio, vcore, gnd, csb, sdi, sck, sdo, address, i2c]} )

Connect a sensor to an obniz.
obniz has internal pull up. But for communication stability, please add pull-up resistor to both SCK and SDI.

![](./image2.jpg)

##### Not recommended direct connecting.

![](./image3.jpg)

name | type | required | default | description
--- | --- | --- | --- | ---
vio | `number(obniz io)` | no | &nbsp; | connected obniz io. power supply for interface
vcore | `number(obniz io)` | no | &nbsp; | connected obniz io. power supply for core
gnd | `number(obniz io)` | no | &nbsp; | connected obniz io. power supply
csb | `number(obniz io)` | no | &nbsp; | connected obniz io. I2C/SPI selection.
sdi | `number(obniz io)` | no | &nbsp; | connected obniz io. data port
sck | `number(obniz io)` | no | &nbsp; | connected obniz io. clock
sdo | `number(obniz io)` | no | &nbsp; | connected obniz io. data port or address selection
i2c | `i2c object` | no | &nbsp; | configured i2c object
address | `number` | no | 0x76  | 0x76 or 0x77

This library use I2C to communicate.

```Python
# Python Example
# Please pullup sdi and sck.
bme280 = obniz.wired(
    "BME280",
    {"vio": 0, "vcore": 1, "gnd": 2, "csb" 3, "sdi": 4, "sck": 5, "sdo":6}
)
await bme280.apply_calibration()
val = await bme280.get_all_wait()
print(val)
```

vio and vcore can be connected.
csb can be connected to high simply, and sdo can be connected to low.
So, minimum connection and configration is.

```Python
# Python Example

# vcore connected to vio
# csb connected to vio
# sdo connected to gnd

bme280 = obniz.wired("BME280", {"vio": 0, "gnd": 1, "sdi": 2, "sck": 3})
await bme280.apply_calibration()
val = await bme280.get_all_wait()
print(val)
```

Or you can use i2c object

```Python
# Python Example

i2c = obniz.get_free_i2c()
i2c.start({"mode": "master", "sda": 2, "scl": 3, "clock" 100000}) 

bme280 = obniz.wired("BME280", {"vio": 0, "gnd": 1, "i2c": i2c})
```

If you configured a chip to use address 0x77 (by pull-up sdo)

```Python
# Python Example

bme280 = obniz.wired(
    "BME280",
    {"vio": 0, "gnd": 1, "sdi": 2, "sck": 3, "address": 0x77}
)
```

## [await] apply_calibration()

Retrive factory stored calibration data from connected chip.
You can use BME280 without calling this, But You should do for better accuracy.

```Python
# Python Example
# Please pullup sdi and sck.
bme280 = obniz.wired(
    "BME280",
    {"vio": 0, "vcore": 1, "gnd": 2, "csb" 3, "sdi": 4, "sck": 5, "sdo":6}
)
await bme280.apply_calibration()
```

## [await] set_iir_strength()

configure of internal IIR filter. 0 to 4.

0 for disable IIR filter.(default)

IIR filter makes more stable and accurate result.
But you should wait for get more accurate result.


```Python
# Python Example
# Please pullup sdi and sck.
bme280 = obniz.wired(
    "BME280",
    {"vio": 0, "vcore": 1, "gnd": 2, "csb" 3, "sdi": 4, "sck": 5, "sdo":6}
)
await bme280.apply_calibration()
await bme280.set_iir_strength(1) # start using minimum IIR 
```

## [await] get_all_wait()

get all values.

- temperature: celcius
- humidity: %
- pressure: hPa

```Python
# Python Example
# Please pullup sdi and sck.
bme280 = obniz.wired(
    "BME280",
    {"vio": 0, "vcore": 1, "gnd": 2, "csb" 3, "sdi": 4, "sck": 5, "sdo":6}
)
await bme280.apply_calibration()
obj = await bme280.get_all_wait()
print('temp:', obj["temperature"], 'degree')
print('humidity:', obj["humidity"], '%')
print('pressure:', obj["pressure"], 'hPa')
```

## calc_altitude(pressure, sea_pressure)

Utility function for calcurate accuracy using air pressure.
Unit is m.

```Python
# Python Example
# Please pullup sdi and sck.
bme280 = obniz.wired(
    "BME280",
    {"vio": 0, "vcore": 1, "gnd": 2, "csb" 3, "sdi": 4, "sck": 5, "sdo":6}
)
await bme280.apply_calibration()
obj = await bme280.get_all_wait()
air_pressure = obj.pressure
hight_in_m = bme280.calc_altitude(air_pressure)
print('altitude:', hight_in_m, 'm')
```