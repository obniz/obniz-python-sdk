# Pressure Sensor - FSR40X
圧力センサFSR40Xです。センサで取得した圧力を知ることができます。

## wired(obniz, {pin0, pin1})
Obnizに圧力センサをつなぎます。
pin0,pin1を圧力センサへ接続してください。

![](./wired.png)
```Python
# Python Example
pressure = obniz.wired("FSR40X", {"pin0" 0, "pin1": 1})
```

## onchange = callback(press)
圧力センサの値に変化があった場合にcallback関数を呼び出します。

```Python
# Python Example
pressure = obniz.wired("FSR40X", {"pin0" 0, "pin1": 1})
def onchange(press):
    print(press)
pressure.onchange = onchange
```

## [await]get_wait()
圧力センサの値を一度だけ取得します

```Python
# Python Example
pressure = obniz.wired("FSR40X", {"pin0" 0, "pin1": 1})
press = await pressure.get_wait()
print(press)
```
