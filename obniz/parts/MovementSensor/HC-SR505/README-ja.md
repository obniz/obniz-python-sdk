# HC-SR505

PIR センサーです。人や動物が近くにいるかを検出できます。

![](image.jpg)


## wired(obniz, {signal [,vcc, gnd]})

３つのピンがあります。直接obnizに接続して下さい。

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

何かが変化した時に呼ばれる関数を設定します。
人が近づいてきたときに関数が呼ばれ、値`True`が引数に入っています。
もし、人がいなくなったりすると`False`が引数に入ります。

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

## [await] get_wait()

近くに人がいるかどうかを一度だけ取得します．
`True`なら近くに人がいて，`False`なら近くに人がいない状態です


```Python
# Python Example
sensor = obniz.wired("HC-SR505", {"vcc": 0, "signal": 1, "gnd": 2})
val = await sensor.get_wait()
if val:
    print('Moving Something!')
else:
    print('Nothing moving')
```
