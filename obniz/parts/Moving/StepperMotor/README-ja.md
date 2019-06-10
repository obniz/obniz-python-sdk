# StepperMotor

ステッピングモーター(またはパルスモーター)はDCモーターのように中にあるコイルをとにかく回すというものとは違い、
ある角度ずつ正確に回転させることができるモーターです。ステップごとに動かすのでそのような名前になっています。
ステッピングモーターを使えば正確に回転させたり、移動させたり、または動かないように位置をキープしたりといったことが簡単にできます。逆に高速にパワフルに回転させる用途には向きません。

このライブラリではバイポーラ・ユニポーラのステッピングモーターを駆動できます。obnizから直接つないで動かすため5vで動くものを想定しています。

![](./wire.jpg)

![](./image.jpg)


## wired(obniz, {a, b, aa, bb [, common]})

部品と接続したioを指定します。

バイポーラ・ユニポーラ、それぞれでこのように接続します。

![](./wire.png)

ライブラリはcommonの有無でバイポーラかユニポーラかを判断します。

name | type | required | default | description
--- | --- | --- | --- | ---
a | `int(obniz io)` | no |  &nbsp; | つないだobnizのioを指定してください。
b | `int(obniz io)` | no |  &nbsp; | つないだobnizのioを指定してください。
aa | `int(obniz io)` | no |  &nbsp; | つないだobnizのioを指定してください。aの逆相を指定します。
bb | `int(obniz io)` | no |  &nbsp; | つないだobnizのioを指定してください。bの逆相を指定します。
common | `int(obniz io)` | no |  &nbsp; | ユニポーラの場合に指定します。


```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_wait(200)
print(motor.current_step) # => 300
```

### step_type(type: string)

励磁方法を変更します。デフォルトで2となっています。

name | type | required | default | description
--- | --- | --- | --- | ---
type | `string` | yes | `'2'` | 下に詳細を記す

指定できるのは以下です。

keyname | type | description
--- | --- | ---
`'1'` | 1相励磁 | どれか１つのコイルのみを動作する方法。消費電力が少ないが、パワーは弱い
`'2'` | 2相励磁 | 必ず２つのコイルを動作する方法。最も一般的
`'1-2'` | 1-2相励磁 | 上記２つを組み合わせた方式で半分のステップで駆動できるのが特徴

`'1-2'`のみステップあたりの移動量が変わるので注意が必要です。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
morot.step_type("1")
await motor.step_wait(100)
await motor.step_wait(200)
print(motor.current_step) # => 300
```

### speed(frequency: int)

速度をHzで指定します。100は1秒間に100ステップとなります。

name | type | required | default | description
--- | --- | --- | --- | ---
frequency | `int` | yes | `100` | ステップ移動の周波数

指定できる最大値はモーターとモーターの負荷によって異なります。大きいほどスリップの可能性(動かしたはずなのに実際は動いていない)が上がります

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.speed(1000)
await motor.step_wait(100)
```

### [await] step_wait(step: int)

指定したステップだけ移動します。speedとstepTypeに従ってモーターを駆動します。

name | type | required | default | description
--- | --- | --- | --- | ---
step | `int` | yes | - | 動かしたいステップ数

小数が与えられた場合は四捨五入されます。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_wait(-100)
# now returned to start position.
```

### [await] step_to_wait(destination: int)

目的となるステップ数の場所まで移動します。speedとstepTypeに従ってモーターを駆動します。

name | type | required | default | description
--- | --- | --- | --- | ---
destination | `int` | yes | - | 目的となるステップ数。


```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_to_wait(-150); # it move -250 steps
print(motor.current_step) # => -150
```

### [await] hold_wait()

今のステップ位置で電流を流し、維持した状態にします。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.hold_wait()
```

### [await] free_wait()

全てのコイルへの電流を停止し、モーターを自由な状態にします。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.free_wait()
```


### current_step

現在の位置をステップで表します。初期値は0です。
100ステップ動かし-50動かしたなら50となっています。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
await motor.step_wait(100)
await motor.step_to_wait(-150); # it move -250 steps
print(motor.current_step) # => -150
```

### [await] rotate_wait(rotation: int)

指定した角度だけ回転させます。
rotation_step_count変数に従い動かすので、先に設定する必要があります。

name | type | required | default | description
--- | --- | --- | --- | ---
rotation | `int` | yes | - | 回転させたい角度(度)

360を指定すれば1回転することになり、-360で逆向きに１回転します。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.rotation_step_count = 100
await motor.rotate_wait(360 * 2)
print(motor.current_rotation()); # => 720
print(motor.current_angle()); # => 0
```

### [await] rotate_to_wait(rotation: int)

始めの角度を0度として指定した角度になるように回転させます。
また、最も少ない移動数でその角度に移動します。
rotation_step_count変数に従い動かすので、先に設定する必要があります。

name | type | required | default | description
--- | --- | --- | --- | ---
angle | `int` | yes | - | 目標となる角度(0 to 360)

355度に移動したあと0を指定すると355度ではなく5度の移動となります。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.rotation_step_count = 100
await motor.rotate_to_wait(90)
```

### rotation_step_count

1回転するのに何ステップ必要かを指定します。この値はモーターによって異なります。デフォルトで100となっています。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.rotation_step_count = 100
await motor.rotate_to_wait(90)
```

### [await] move_wait(distance: int)

指定した距離(mm)だけ移動します。
milli_meter_step_count変数に従い動かすので、先に設定する必要があります。

name | type | required | default | description
--- | --- | --- | --- | ---
distance | `int` | yes | - | 移動距離(mm)


```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.milli_meter_step_count = 10
await motor.move_wait(100)
await motor.move_wait(-10)
print(motor.current_distance()); # => 90
```

### [await] move_to_wait(destination: int)

はじめを0として、指定した位置(mm)に移動します。
milli_meter_step_count変数に従い動かすので、先に設定する必要があります。

name | type | required | default | description
--- | --- | --- | --- | ---
destination | `int` | yes | - | 目標位置(mm)


```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.milli_meter_step_count = 10
await motor.move_wait(100)
await motor.move_to_wait(-10)
print(motor.current_distance()); # => -10
```

### milli_meter_step_count

1ミリ移動するのに何ステップ必要なのかを指定します。デフォルトで1となっています。

```Python
# Python Example
motor = obniz.wired("StepperMotor", {"a": 0, "aa": 1, "b": 2, "bb": 3})
motor.milli_meter_step_count = 10
await motor.move_wait(100)
await motor.move_to_wait(-10)
print(motor.current_distance()); # => -10
```