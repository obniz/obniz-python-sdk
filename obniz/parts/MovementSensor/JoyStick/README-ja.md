# JoyStick
X軸Y軸とプッシュスイッチをもつジョイスティックです。出力がアナログ値の一般的なものに対して利用できます。

![](./joystick.jpg)

## wired(obniz, {sw, x, y, vcc, gnd})
obnizと接続します。vccはジョイスティックの5v入力へ。gndはマイナスへ接続します。  
sw: スイッチ  
x: x軸のアナログ値出力  
y: y軸のアナログ値出力  
へ接続して下さい

### 注意！いろいろな製品があります！
ジョイスティックは製品によってピン配置が違うので注意して下さい。
例えば、obnizでよく使われるのはこのピンアサインのものですが
![](./joystick_pins.jpg)

他にもこのようなピンアサインのものもあります。

![photo of wired](./wired.png)


```Python

joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})

# or

joystick = obniz.wired("JoyStick", {"gnd": 0, "sw": 1, "y": 2, "x": 3, "vcc": 4})

# and mores
```
## onchangex = callback(angle)
## onchangey = callback(angle)
それぞれX軸，Y軸方向へ動いた場合に呼ばれる関数を指定できます。
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

## onchangesw = callback(pressed)
ボタンが押されたり離された時に呼ばれます。
```Python
# Python Example
joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})
def onchangesw(pressed):
    print(pressed)
joystick.onchangesw = onchangesw
```


## [await] is_pressed_wait()
ボタンが押されているかどうかを一度だけ取得します

```Python
# Python Example
joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})
is_pressed = await joystick.is_pressed_wait()
if is_pressed:
    print("PRESSED")
    
```


## [await] get_x_wait()
## [await] get_y_wait()

X,Yそれぞれの傾きを一度だけ取得します

```Python
# Python Example
joystick = obniz.wired("JoyStick", {"gnd": 4, "sw": 0, "y": 1, "x" 2, "vcc": 3})
x = await joystick.get_x_wait()
y = await joystick.get_y_wait()
 
print("x:", x, "y:", y)

```