# JoyStick

X and Y direction with Push Switch Joystick.
This class accept only analog output.

![](./joystick.jpg)

## wired(obniz, {sw, x, y, vcc, gnd})

connect to an obniz.

1. vcc: power supply
2. gnd: power supply
3. sw: push switch
4. x: X axis analog output
5. Y: T axis analog output

### Attention! pins assing is diffrerent in each product!
There are some joystick and these pin assigns are different.

For example, A joystick commonly used with obniz is below.

![](./joystick_pins.jpg)

But another one has a pinassign like

![photo of wired](./wired.png)


```Python

joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})

# or

joystick = obniz.wired("JoyStick", {"gnd": 0, "sw": 1, "y": 2, "x": 3, "vcc": 4})

# and mores
```

## onchangex = callback(angle)
## onchangey = callback(angle)
callback for on change angle.

angle = -1 to 1

```Python
# Python Example
joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})
def onchangex(val):
    print(val)
joystick.onchangex = onchangex
def onchangey(val):
    print(val)
joystick.onchangey = onchangey
```

## onchangesw = function(pressed)

It's called when button pressed/released.

```Python
# Python Example
joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})
def onchangesw(pressed):
    print(pressed)
joystick.onchangesw = onchangesw
```



## [await] is_pressed_wait()

Get button state once. 

```Python
# Python Example
joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})
is_pressed = await joystick.is_pressed_wait()
if is_pressed:
    print("PRESSED")
    
```


## [await] get_x_wait()
## [await] get_y_wait()

Get X or Y angle once

```Python
# Python Example
joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})
x = await joystick.get_x_wait()
y = await joystick.get_y_wait()
 
print("x:", x, "y:", y)

```