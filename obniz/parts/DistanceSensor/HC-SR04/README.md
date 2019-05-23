# HC-SR04
Ultrasonic Distance Measurement Unit.


## wired(obniz, {vcc, trigger, echo, gnd})

![photo of wired](./wired.png)
```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
def callback(distance):
    print("distance", distance, "mm")
hcsr04.measure(callback)
```

## measure(callback(distance))
measure distance.
default return unit is "mm". change by calling unit().
```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
def callback(distance):
    print("distance", distance, "mm")
hcsr04.measure(callback)
```

## [await] measure_wait()
This is async/await version of measure()

```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
while True:
    avg = 0
    count = 0
    for i in range(i): # measure three time. and calculate average
        val = await hcsr04.measure_wait()
        if val:
            count += 1
            avg += val
    if count > 1:
        avg /= count
    print(avg)
    await obniz.wait(100)
```


## temp
The speed of ultrasonic depends on temperature.
By default calculation temp is 15 degree(Celsius). Change this to get more accurate result.
```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
hcsr04.temp = 36
distance = await hcsr04.measure_wait()
print("distance", distance, "mm")
```

## reset_alltime
Some HC-SR04 needs power reset after measure.
set true to this property to automatic power reset after each measurement.
```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
hcsr04.reset_alltime = True
distance = await hcsr04.measure_wait()
print("distance", distance, "mm")
```

## unit(unit)
change unit

1. "mm"(default)
2. "inch"

are available

```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
hcsr04.unit("inch")
def callback(distance):
    print("distance", distance, "inch")
hcsr04.measure(callback)
```