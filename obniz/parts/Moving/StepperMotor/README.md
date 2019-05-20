# StepperMotor

Stepper Motor is different from just rotating things like DC motors.
It rotate by following electrical pulse. So, It can rotate correctly by step.
So It is very useful when you want to move/rotate things correctly, and hold something at current state. In the other hands, Stepper Motor is not good for high-speed/high-power usages.

This library can drive both bipolar/unipolar stepper motors. This cabale to drive directy from obniz io. So 5v stepper motor is best.

![](./wire.jpg)

![](./image.jpg)


## wired(obniz, {a, b, aa, bb [, common]})

It recognize connected io.

See below image to connect.

![](./wire.png)

This function recognize motor bipolar/unipolar by specifying common.


name | type | required | default | description
--- | --- | --- | --- | ---
a | `int(obniz io)` | no |  &nbsp; | Specify obniz io
b | `int(obniz io)` | no |  &nbsp; | Specify obniz io
aa | `int(obniz io)` | no |  &nbsp; | Specify obniz io. This is other side of a.
bb | `int(obniz io)` | no |  &nbsp; | Specify obniz io. This is other side of b.
common | `int(obniz io)` | no |  &nbsp; | Specify only when unipolar.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_wait(200)
print(motor.current_step) # => 300
```

### step_type(type: string)

It change stepping method. By default, it is 2


name | type | required | default | description
--- | --- | --- | --- | ---
type | `string` | yes | `'2'` | See below options



keyname | type | description
--- | --- | ---
`'1'` | 1 phase ecitation | Only one coil is driven. Low power consumption. But not strong
`'2'` | 2 phase ecitation | Two coil is always driven. Very common.
`'1-2'` | 1-2 phase ecitation | Combination of above two method. Step is 1/2.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
morot.step_type("1")
await motor.step_wait(100)
await motor.step_wait(200)
print(motor.current_step) # => 300
```

### speed(frequency: int)

It specify speed in hz. 100 means 100 step per sec.

name | type | required | default | description
--- | --- | --- | --- | ---
frequency | `int` | yes | `100` | frequency of steps

Limit of frequency is depends on motor which you are using. High frequency has risks of slips.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.speed(1000)
await motor.step_wait(100)
```

### [await] step_wait(step: int)

It rotate a motor by specified steps.
Also it follow speed and stepType.

name | type | required | default | description
--- | --- | --- | --- | ---
step | `int` | yes | - | Steps wants to move

If decimal int was provided, then the int will be rounded.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_wait(-100)
# now returned to start position.
```

### [await] step_to_wait(destination: int)

It rotate a motor to specified destionation step.
Also it follow speed and step_type.

name | type | required | default | description
--- | --- | --- | --- | ---
destination | `int` | yes | - | Destionation step


```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_to_wait(-150); # it move -250 steps
print(motor.current_step) # => -150
```

### [await] hold_wait()

Drain current to keep position.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.hold_wait()
```


### [await] free_wait()

Stop drain current and make free a motor.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.free_wait()
```


### current_step

It is current step count int. Initially 0.
When you move +100 then -50, It is 50

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_to_wait(-150); # it move -250 steps
print(motor.current_step) # => -150
```


### [await] rotate_wait(rotation: int)

It rotate by specified angle.
It also follow rotation_step_count variable. Please set correct int first.

name | type | required | default | description
--- | --- | --- | --- | ---
rotation | `int` | yes | - | angle to move in degree

360 means one rotate.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.rotation_step_count = 100
await motor.rotate_wait(360 * 2)
print(motor.current_rotation()); # => 720
print(motor.current_angle()); # => 0
```

### [await] rotate_to_wait(rotation: int)

It rotate to specified angle. (Initial angle is recognized as 0).
It rotate at minimum rotation.
It also follow rotation_step_count variable. Please set correct int first.

name | type | required | default | description
--- | --- | --- | --- | ---
angle | `int` | yes | - | Destination angle in degree

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.rotation_step_count = 100
await motor.rotate_to_wait(90)
```

### rotation_step_count

It is configration of needed step count to one rotation.
It depends on your motor. It initially 100.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.rotation_step_count = 100
await motor.rotate_to_wait(90)
```

### [await] move_wait(distance: int)

It rotate specified distance in mm.
It also follow milli_meter_step_count variable. Please set correct int first.

name | type | required | default | description
--- | --- | --- | --- | ---
distance | `int` | yes | - | distance to be moved


```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.milli_meter_step_count = 10
await motor.move_wait(100)
await motor.move_wait(-10)
print(motor.current_distance()); # => 90
```

### [await] move_to_wait(destination: int)

It rotate to specified distance in mm. Initial position is recognized as 0.
It also follow milli_meter_step_count variable. Please set correct int first.

name | type | required | default | description
--- | --- | --- | --- | ---
destination | `int` | yes | - | destination distance in mm


```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.milli_meter_step_count = 10
await motor.move_wait(100)
await motor.move_to_wait(-10)
print(motor.current_distance()); # => -10
```

### milli_meter_step_count

It is configration of needed step count to move 1 mm.
It depends on your motor. It initially 1.

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.milli_meter_step_count = 10
await motor.move_wait(100)
await motor.move_to_wait(-10)
print(motor.current_distance()); # => -10
```