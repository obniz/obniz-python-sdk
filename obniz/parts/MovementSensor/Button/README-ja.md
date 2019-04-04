# Button
押すことで電流を流したり止めたり出来る部品です。これをつなぎ電流が流れているかを見ることでボタンが押されているかをチェックできます。このモジュールではボタンの形によらず、とにかく押せば電流が流れるボタンを扱うことができます。

## wired(obniz, {signal [,gnd]})

ボタンにある２つのピンをObnizにつなぎます。プラスとマイナスはありません。例えば片方をObnizの0番に。もう片方を1番につないだ場合は以下のようにプログラム上でwireします

![photo of wired](./wired.png)

```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})
```

gndはオプショナルです。他のGNDに繋いだ場合は、指定しなくても大丈夫です。

```Python
# Python Example
button = obniz.wired("Button",  {"signal":0})
```

## onchange = function(pressed)
ボタンが押された時、離された時にcallback関数を呼び出します。

```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})

def onchange(pressed):
    print("pressed:", pressed)

button.onchange = onchange
```

## [await] is_pressed_wait()
ボタンが押されているかを確認します。
```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})

pressed = await button.is_pressed_wait()
print("pressed:", pressed)
```


## [await] state_wait()
ボタンが押される／離されるまで待ちます
```Python
# Python Example
button = obniz.wired("Button",  {"signal": 0, "gnd": 1})

await button.state_wait(True) 
print("button pushed!")
await button.state_wait(False) 
print("button released")
```