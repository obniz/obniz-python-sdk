# Button
Button turn on/off electricity. Just monitor voltage to check button pressed or not.

## wired(obniz, {signal [,gnd]})

Connect two pins to obniz. Many buttons has no pin direction. you can connect each one to signal,gnd.

![photo of wired](./wired.png)

```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})
```

gnd is optional. It can be shared other gnd.

```Python
# Python Example
button = obniz.wired("Button",  {"signal":0})
```



## onchange = function(pressed)
called when button pressed/released.

```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})

def onchange(pressed):
    print("pressed:", pressed)

button.onchange = onchange
```
## [await] is_pressed_wait()
Check current button with waiting result.
```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})

pressed = await button.is_pressed_wait()
print("pressed:", pressed)
```



## [await] state_wait()
Wait until push/release button.
```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})

await button.state_wait(True) 
print("button pushed!")
await button.state_wait(False) 
print("button released")
```