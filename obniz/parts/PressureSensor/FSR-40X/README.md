# Pressure Sensor - FSR40X

Pressure sensor. It output pressure as a voltage.


## wired(obniz, {pin0, pin1})

Connect two pins to an obniz. pin0 and pin1 is obniz io number.

![](./wired.png)
```Python
# Python Example
pressure = obniz.wired("FSR40X", {"pin0" 0, "pin1": 1})
```

## onchange = callback(press)

callback function will called when pressure changed.

```Python
# Python Example
pressure = obniz.wired("FSR40X", {"pin0" 0, "pin1": 1})
def onchange(press):
    print(press)
pressure.onchange = onchange
```

## [await]get_wait();

Get pressure value once.

```Python
# Python Example
pressure = obniz.wired("FSR40X", {"pin0" 0, "pin1": 1})
press = await pressure.get_wait()
print(press)
```
