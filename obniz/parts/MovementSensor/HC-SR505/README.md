# HC-SR505

It is used for detects humans/animals.

![](image.jpg)


## wired(obniz, {signal [,vcc, gnd]})

It has three pins. Connect them to an obniz directly.

```Python
# Python Example
sensor = obniz.wired("HC-SR505", {"vcc": 0, "signal": 1, "gnd": 2})
def onchange(val):
    if val:
        print('Moving Something!')
    else:
        print('Nothing moving')
sensor.onchange = onchange
```

## onchange = function(value)

It called when something changed.
It humans is closing to a sensor, this function will called with value `True`.
If a humans leaves or if a human stops moving, this function will called with value `False`.
It's fileter works. So called with False after soon called with True.

```Python
# Python Example
sensor = obniz.wired("HC-SR505", {"vcc": 0, "signal": 1, "gnd": 2})
def onchange(val):
    if val:
        print('Moving Something!')
    else:
        print('Nothing moving')
sensor.onchange = onchange
```

## [await] getWait()

Get sensor value once.

```Python
# Python Example
sensor = obniz.wired("HC-SR505", {"vcc": 0, "signal": 1, "gnd": 2})
val = await sensor.get_wait()
if val:
    print('Moving Something!')
else:
    print('Nothing moving')
```
