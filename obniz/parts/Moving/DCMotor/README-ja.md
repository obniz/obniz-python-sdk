# DCMotor
タミヤモーターやマブチモーターのような、<br>電池を繋いで回すような一般的なモーターです。プラスとマイナスはありませんが逆にすると逆に回転します。

![photo of DCMotor](./wired.png)

## wire({forward, back})
モーターから出ている２本の線をObnizにつなぎます。どちらをどこにつないでもOKですが、プログラムで「前」と書いて後ろに動いたらあとで配線を逆にすると良いです。モーターをObnizの0と1番に繋いだ場合は以下のようにします
```Python
# Python Example
motor = obniz.wired("DCMotor",  {"forward": 0, "back": 1})
```
## forward()
モーターを回転させます。


```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.forward()
```
## reverse()
モーターを逆に回転させます。

```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.reverse()
```
## stop()
モーターを停止させます。

```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.forward()
await obniz.wait(1000)
motor.stop()
```
## move(bool)
directionに合わせて指定した方向にモーターを回転させます。rotateとreverseを引数を変えるだけでこの関数１つで扱えます。trueであれば正転。falseであれば逆に回転します。

```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.move(True) # = motor.forward()
```
## power(float)
モーターのパワーを変更します。0~100で指定することが出来ます。

```Python
# Python Example
motor = obniz.wired("DCMotor", {"forward": 0, "back": 1})

motor.move(True) # = motor.forward()
```