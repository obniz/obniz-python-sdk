# Temperature Sensor - LM60
温度センサLM60BIZ/LM60CIMです。センサで取得した温度を知ることができます。






![photo of AnalogTempratureSensor](./wired.png)



## wired(obniz, {vcc, output, gnd})
Obnizに温度センサをつなぎます。
```Python
# Python Example
tempsens = obniz.wired("LM60",  {"gnd": 0 , "output": 1, "vcc" 2})
```

## onchange
温度センサの値に変化があった場合にcallback関数を呼び出します。
温度は摂氏で返されます。
```Python
# Python Example
tempsens = obniz.wired("LM60",  {"gnd": 0 , "output": 1, "vcc" 2})

def print_temp(temp):
    print(temp)
tempsens.onchange = print_temp
```


## [await]get_wait

温度センサの値を一度だけ取得します
温度は摂氏で返されます。

```Python
# Python Example
tempsens = obniz.wired("LM60",  {"gnd": 0 , "output": 1, "vcc" 2})

temp = await tempsens.get_wait()
print(temp)
```
 