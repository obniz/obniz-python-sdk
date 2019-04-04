# DCMotor

Common Brushed DC Motor which moves when connected to +/- and reverse when connected to other side.

![photo of DCMotor](./wired.png)

## wire({forward, back})

connect two wire to an obniz and set io number to forward,back.
If you connect to io 0 and 1, then write a program like a below.

```Python
# Python Example
motor = obniz.wired("DCMotor",  {"forward": 0, "back": 1})
motor.power(50)
motor.forward()
```
## forward()

start moving forward.

```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.forward()
```
## reverse()

start moving to back.

```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.reverse()
```

## stop()

stop a motor.


```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.forward()
await obniz.wait(1000)
motor.stop()
```
## move(bool)

move a motor regard provided value.


```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.move(True) # = motor.forward()
```
## power(float)
set a motor power.

default is 30.

power must be within 0~100.

```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.move(True) # = motor.forward()
```