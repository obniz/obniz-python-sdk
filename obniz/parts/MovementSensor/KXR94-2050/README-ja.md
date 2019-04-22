# KXR94-2050

x,y,zの3軸加速度センサ
重力の向きや，どちらの方向に動いているかを知ることができます．

![](./image.jpg)


## obniz.wired(obniz, {x, y, z [, vcc, gnd, enable, self_test]})

部品のピンをobnizに接続し、どこに接続したかなどを設定します。

name | type | required | default | description
--- | --- | --- | --- | ---
x | `number(obniz io)` | yes | &nbsp | X軸の加速度の値が電圧として出力されます。
y | `number(obniz io)` | yes | &nbsp | Y軸の加速度の値が電圧として出力されます。
z | `number(obniz io)` | yes | &nbsp | Z軸の加速度の値が電圧として出力されます。
vcc | `number(obniz io)` | &nbsp | &nbsp | 電源です。5V。
gnd | `number(obniz io)` | &nbsp | &nbsp | 電源です。GND
self_test | `number(obniz io)` | &nbsp | &nbsp | highにするとセルフテストモードになります。
enable | `number(obniz io)` | &nbsp | &nbsp | lowにすると加速度の計測を無効化出来ます。

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

x,y,zいずれかの値が更新された場合に呼び出される関数を指定できます。
xyzはセンサーの出力値を元に計算された重力加速度となります。1であれば9.8m^2です。値の範囲は-2以上+2以下となります。

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

X,Y,Z軸、それぞれの加速度が変わったときにのみ呼び出されます。
ある１つの軸方向の値しかいらない場合に利用すると便利です。

## get()

今の加速度を３つとも取得します。
obnizに問い合わせることなく、obnizから届いた最後の値を取得します。

無限ループで実行する場合はwaitを入れる必要があります。


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

３軸の加速度情報を取得します。
obnizに問い合わせることで最新の値を取得します。

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