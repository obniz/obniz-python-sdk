# KXR94-2050

x,y,z 3 dimention accelaration sensor.
This is used for determin direction and angle of a device.

![](./image.jpg)


## obniz.wired(obniz, {x, y, z [, vcc, gnd, enable, self_test]})

Connect pins to an obniz and specify io.

name | type | required | default | description
--- | --- | --- | --- | ---
x | `number(obniz io)` | yes | &nbsp; | value of x
y | `number(obniz io)` | yes | &nbsp; | value of y
z | `number(obniz io)` | yes | &nbsp; | value of z
vcc | `number(obniz io)` | &nbsp; | &nbsp; | Power supply. 5v
gnd | `number(obniz io)` | &nbsp; | &nbsp; | Power supply. gnd
self_test | `number(obniz io)` | &nbsp; | &nbsp; | high for enter test mode
enable | `number(obniz io)` | &nbsp; | &nbsp; | low for disable device.

```Python

# Python Example
sensor = obniz.wired("KXR94-2050", {
    "vcc": 0, "gnd": 1, "x": 2, "y": 3, "z": 4, "enable": 5, "self_test": 6
})
def on_change(values):
      print("x:", values.x)
      print("y:", values.y)
      print("z:", values.z)    
sensor.on_change = on_change
   
```

## on_change = function({x: y: z:})

Specifying a callback function for one of value changes of x,y,z.
The value is regarding gravity. 1 measn 9.8m^2. The value will be -2<= and <= +2.

```Python

# Python Example
sensor = obniz.wired("KXR94-2050", {
    "vcc": 0, "gnd": 1, "x": 2, "y": 3, "z": 4, "enable": 5, "self_test": 6
})
def on_change(values):
      print("x:", values.x)
      print("y:", values.y)
      print("z:", values.z)    
sensor.on_change = on_change
   
```

## on_change_x = function(value)

## on_change_y = function(value)

## on_change_z = function(value)

Specifying a callback function for value change.
This is useful when you only want to watch one of them.

## get()

Getting a current three acceleration value.
This function not contact to an obniz. It return last notified value from an obniz.

Notice: You should insert a wait() in infinity loop.


```Python
# Python Example
sensor = obniz.wired("KXR94-2050", {
    "vcc": 0, "gnd": 1, "x": 2, "y": 3, "z": 4, "enable": 5, "self_test": 6
})
  
while True:
    values = sensor.get()
    print("x:", values.x)
    print("y:", values.y)
    print("z:", values.z)
    await obniz.wait(30)
```


## [await] get_wait()

Getting a current three acceleration value.
This function will contact to an obniz to retrive current value.

```Python
# Python Example
sensor = obniz.wired("KXR94-2050", {
    "vcc": 0, "gnd": 1, "x": 2, "y": 3, "z": 4, "enable": 5, "self_test": 6
})
while True:
    values = await sensor.get_wait()
    print("x:", values.x)
    print("y:", values.y)
    print("z:", values.z)

```