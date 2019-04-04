# GP2Y0A21YK0F
Infrared Distance Measurement Unit.
This unit output voltage regarding measured distance.

![photo of wired](./image.gif)

## wired(obniz, {vcc, gnd, signal})

![photo of wired](./image.jpg)

![photo of wired](./wired.png)

```Python
# Python Example
sensor = obniz.wired("GP2Y0A21YK0F", {"vcc": 0, "gnd": 1, "signal": 2})
def print_distance(distance):
    print("distance:", distance, "mm")
sensor.start(print_distance)
```

## start(callback(distance))
measure distance continurously.
Callback will be called when distance changed.
default return unit is "mm". change by calling .unit()
```Python
# Python Example
sensor = obniz.wired("GP2Y0A21YK0F", {"vcc": 0, "gnd": 1, "signal": 2})

def print_distance(distance):
    print("distance:", distance, "mm")
sensor.start(print_distance)
})
```

## [await] get_wait()

Measure distance once.

```Python
# Python Example
sensor = obniz.wired("GP2Y0A21YK0F", {"vcc": 0, "gnd": 1, "signal": 2})

while True:
    val = await sensor.get_wait()
    print("distance", val)
    await obniz.wait(1000)
```
    
## unit(unit)
change unit

1. "mm"(default)
2. "inch"

are available

```Python
# Python Example
sensor = obniz.wired("GP2Y0A21YK0F", {"vcc": 0, "gnd": 1, "signal": 2})

sensor.unit("inch")
def print_distance(distance):
    print("distance:", distance, "mm")
sensor.start(print_distance)
```