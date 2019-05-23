# ArduCAMMini

少ないピン数で利用できるカメラモジュールです。
たくさんの解像度を選べる上に、jpegで画像を取り出すことが出来ます。

同じArduCAMMiniでも種類がありますが、OV2640の2Mピクセルのカメラに対応しています。

![](./image.jpg)


## wired(obniz,  {cs [, mosi, miso, sclk, gnd, vcc, sda, scl, spi, i2c, spi_drive, spi_frequency]} )

つながっているioを指定してオブジェクト化します。

このカメラの電源はobniz以外から供給する方法がおすすめです。
obnizから電源を供給する場合は過電流に気をつける必要があります。
電源は以下のように供給して下さい

- obniz以外の外部電源に接続する
- obnizのJ1ピンに接続する
- vccを2つ以上のobnizのioから供給する

このドキュメントではio11もvcc供給に使用する方法でカメラを動かしています。

![](./wire.jpg)

このモジュールはSPIとI2Cがそれぞれ１つずつ必要です。

name | type | required | default | description
--- | --- | --- | --- | ---
cs | `number(obniz io)` | yes | &nbsp | obniz io. チップ選択
vcc | `number(obniz io)` | no | &nbsp | obniz io. 電源 +5V
gnd | `number(obniz io)` | no | &nbsp | obniz io. 電源 0v
mosi | `number(obniz io)` | no | &nbsp | obniz io. SPI mosi 端子
miso | `number(obniz io)` | no | &nbsp | obniz io. SPI miso 端子
sclk | `number(obniz io)` | no | &nbsp | obniz io. SPI clk 端子
sda | `number(obniz io)` | no | &nbsp | obniz io. I2C sda 端子
scl | `number(obniz io)` | no | &nbsp | obniz io. I2C scl 端子
i2c | `i2c object` | no | &nbsp | configured i2c object
spi | `spi object` | no | &nbsp | configured spi object
spi_frequency | `spi object` | no | 4Mhz | SPI通信がうまくいかない場合に周波数を下げる時に利用します
spi_drive | `spi object` | no | `'3v'` | SPI通信がうまくいかない場合に駆動方法を変更する時に利用します

ピンだけを指定して以下のように設定することが出来ます。
```Python
# Python Example
from obniz import Obniz

obniz = Obniz("OBNIX_ID_HERE")
async def onconnect():
    obniz.io11.output(True)
    cam = obniz.wired("ArduCAMMini", {
        "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
    })
    await cam.startup_wait()
    data = await cam.take_wait('1024x768')
    print("image size = ", len(data), " bytes")
    base64 = cam.array_to_base64(data)

obniz.onconnect = onconnect
```

または、設定済みのi2cやspiオブジェクトがあれば、それを利用することも可能です。


## [await] startup_wait()

カメラを初期化します。撮影する前に一度だけ呼び出す必要があります。
この関数を呼ぶだけで

- SPI通信のテスト
- I2C通信のテスト
- 対応可能なカメラかどうかのチェック
- モードの設定とJpegカメラとしての設定
- 320x240解像度の設定

が完了します。

この初期化をしていればtake_wait()関数で撮影ができます。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
```

startup_wait()を使わないで初期化する場合は以下のような手順となります。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.spi_pingpong_wait()
cam.set_mode('MCU2LCD')
chipid = await cam.get_chip_id_wait()
if chipid != 0x2642:
    raise Exception('unknown chip ' + str(chipid))

cam.init()
```



## [await] take_wait(size)

撮影を行い、jpegのデータを取得します。
撮影の前にはstartup_wait()関数でカメラが初期化されている必要があります。

sizeを指定すると、カメラの解像度設定を変更します。
何も指定されていないか、すでに設定済みの解像度と同じだった場合は何もしません。
sizeで指定できるのはset_size()関数で指定できるものと同じです。

返り値はjpegデータの入ったarrayとなります。
カメラとobnizの間の通信に失敗した場合はエラーとなるか、ずっと応答待ちとなりこの関数から抜けないかのどちらかとなります。


```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
jpeg_data = await cam.take_wait('1024x768')
```

take_wait()を使わずにstart_capture()やFIFO操作などを自分で使って撮影する場合のやり方についてはstart_capture()関数のexampleを御覧ください。

## array_to_base64(list)
listデータをbase64にエンコードします。
これによりjpegのbase64データを取得できます。

```Python
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
jpeg_data = await cam.take_wait('1024x768')
print("image size = ", len(jpeg_data), " bytes")
  
base64 = cam.array_to_base64(jpeg_data)
```

## set_mode(mode)

カメラのモードを設定します。
以下から選択可能です。

この関数はstartup_wait()関数内で使われています。

- 'MCU2LCD'
- 'CAM2LCD'
- 'LCD2MCU'

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
cam.set_mode('MCU2LCD')
```

## [await] spi_pingpong_wait()

obnizとカメラとの間のspi通信をテストします。
カメラの電源が入っているか、配線が正しいかの確認ができます。

この関数はstartup_wait()関数内で使われています。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.spi_pingpong_wait()
```

## [await] get_chip_id_wait()

カメラのチップ番号をI2C通信で取得します。
I2Cに問題があるかや、チップがサポートされているものかどうかを確認するのに使用します。

この関数はstartup_wait()関数内で使われています。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
chipid = await cam.get_chip_id_wait()
if chipid != 0x2642:
  raise Exception('unknown chip ' + str(chipid))
```

## init()

カメラを初期化します。
基本的な設定を行い、jpegモードにして、解像度も320*240で一度設定してしまいます。

この関数はstartupWait()関数内で使われています。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
cam.set_mode('MCU2LCD')
cam.init()
```

## set_size(size)

カメラの解像度を指定します。
選択できるのは

- '160x120'
- '176x144'
- '320x240'
- '352x288'
- '640x480'
- '800x600'
- '1024x768'
- '1280x960'
- '1600x1200'

のうちのいずれかです。

解像度を変更したあとには1秒ほどの待ち時間を設定するのが良いようです。


```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.set_size('1600x1200')
await obniz.wait(1000)
```

## flush_fifo()

FIFO内の内容をクリアします。
start_capture()関数で撮影を開始すときには２度呼ぶ必要があります。

この関数はtake_wait()関数内で使われています。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```

## startCapture()

撮影を開始します。
ただし、すぐに撮影は終わりません。終わったかどうかはis_capture_done_wait()関数で調べます。

この関数はtake_wait()関数内で使われています。


```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```

## [await] is_capture_done_wait()

start_capture()で開始した撮影が、終わってデータを取れる状態になったかを調べます。

この関数はtake_wait()関数内で使われています。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```

## [await] read_fifo_wait()

カメラのFIFOに入っている撮影されたデータを取り出します。

この関数はtake_wait()関数内で使われています。

```Python
# Python Example
obniz.io11.output(True)
cam = obniz.wired("ArduCAMMini", {
    "cs": 0, "mosi": 1, "miso": 2, "sclk": 3, "gnd": 4, "vcc": 5, "sda": 6, "scl": 7
})
await cam.startup_wait()
cam.flush_fifo()
cam.flush_fifo()
cam.start_capture()
while True:
    if await cam.is_capture_done_wait():
        break
jpeg_data = await cam.read_fifo_wait()
```
