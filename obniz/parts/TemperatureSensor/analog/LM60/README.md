# Temperature Sensor - LM60
Temperature sensor LM60BIZ/LM60CIM



![photo of AnalogTempratureSensor](./wired.png)




## wired(obniz, {vcc, gnd, output})
```Python
# Python Example
tempsens = obniz.wired("LM60",  {"gnd": 0 , "output": 1, "vcc" 2})
```

## onchange
callback function for temperature change.
Unit of temp is Celsius

```Python
# Python Example
tempsens = obniz.wired("LM60",  {"gnd": 0 , "output": 1, "vcc" 2})

def print_temp(temp):
    print(temp)
tempsens.onchange = print_temp
```

## [await]get_wait
get temperature change.
Unit of temp is Celsius

```Python
# Python Example
tempsens = obniz.wired("LM60",  {"gnd": 0 , "output": 1, "vcc" 2})

temp = await tempsens.get_wait()
print(temp)
```
