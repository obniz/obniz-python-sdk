# Temperature Sensor - SHT31
温度センサSHT31です。センサで取得した温度を知ることができます。

![](./sht31.jpg)

## wired(obniz,  {vcc , sda, scl, adr, gnd, addressmode} )
Obnizに温度センサをつなぎます。
0,1,2,3,4はそれぞれ温度センサの電源,SDA,SCL,GND,ADDRピンへ接続してください。
5はI2Cアドレスです。アドレスを0x44にする場合は4,0x45にする場合は5を入力してください。
ADDRピンをプルアップしている場合は0x45,プルダウンしている場合は0x44です。
秋月電子のモジュールキット(K-12125)を使用している場合のデフォルトは0x45です。
```Python
# Python Example
sensor = obniz.wired(
    "SHT31",
    {"vcc": 0, "sda": 1, "scl": 2, "adr": 3, "gnd" :4, "addressmode": 5}
)
```
## [await] get_temp_wait()
現在の温度を計測して返します。単位は摂氏(°C)です。

## [await] get_humd_wait()
現在の湿度を計測して返します。単位は%です。
```Python
# Python Example
sensor = obniz.wired(
    "SHT31",
    {"vcc": 0, "sda": 1, "scl": 2, "adr": 3, "gnd" :4, "addressmode": 5}
)
temp = await sensor.get_temp_wait()
humd = await sensor.get_humd_wait()
print('temperature:', temp)
print('humidity:', humd)
```
