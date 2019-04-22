# HC-SR04
超音波を利用した距離センサーです。

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
距離を計測します、計測が完了したらcallback関数が呼ばれます。
距離の単位はmmで、unit()関数でinchに変えることも出来ます。
もし、反射してくる超音波を受け取れなかった場合はNoneが返ります。
```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
def callback(distance):
    print("distance", distance, "mm")
hcsr04.measure(callback)
```

## [await] measure_wait()
measure()と同様ですが、こちらはfutureを返す関数です。

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
超音波は温度により進む速度が違います。
デフォルトで15度で計算していますが、変更して正しい値にすることでより精度の高い結果が欲しい場合はtempから調整します。
```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
hcsr04.temp = 36
distance = await hcsr04.measure_wait()
print("distance", distance, "mm")
```

## reset_alltime
一部のHC-SR04では、計測するときに毎回電源のON-OFFが必要なものがあります。
もし、計測がうまくいかない場合はこのプロパティをtrueにすることで
自動的にリセットを行います。
```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
hcsr04.reset_alltime = True
distance = await hcsr04.measure_wait()
print("distance", distance, "mm")
```

## unit(unit)
単位を変更します。

1. "mm"(default)
2. "inch"

が利用可能です。

```Python
# Python Example
hcsr04 = obniz.wired("HC-SR04", {"gnd": 0, "echo": 1, "trigger": 2, "vcc": 3})
hcsr04.unit("inch")
def callback(distance):
    print("distance", distance, "inch")
hcsr04.measure(callback)
```