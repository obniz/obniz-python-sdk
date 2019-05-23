# Temperature Sensor - SHT31
Temperature and Humidity sensor SHT31

![](./sht31.jpg)

## wired(obniz,  {vcc , sda, scl, adr, gnd, addressmode} )
the address of SHT31 can be choosed from 0x44,0x45.
Please provide 4 for 0x44. 5 for 0x45 to addressmode.
(SHT31 read ADDR value to define it's address. 0 is 0x45.)
```Python
# Python Example
sensor = obniz.wired(
    "SHT31",
    {"vcc": 0, "sda": 1, "scl": 2, "adr": 3, "gnd" :4, "addressmode": 5}
)
```
## [await] get_temp_wait()
Get a temperature. Unit is Celsius.

## [await] get_humd_wait()
Get a Humidity. Unit is Ratio(%).
```Python
# Python Example
sensor = obniz.wired(
    "SHT31",
    {"vcc": 0, "sda": 1, "scl": 2, "adr": 3, "gnd" :4, "addressmode": 5}
)
temp = await sensor.get_temp_wait()
humd = await sensor.get_humd_wait()
print('temperature:', temp)
print('humidity:', humd)
```
