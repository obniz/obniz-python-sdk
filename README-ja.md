# obniz.py: sdk for python

[![image](https://img.shields.io/pypi/pyversions/obniz.svg)](https://pypi.org/project/obniz/)

[obniz](https://obniz.io/)をpythonから操作するためのsdkです。
[obnizBoard](https://obniz.io/ja/doc/obniz_board_hobby_90/hw_overview)と[obnizOS](https://obniz.io/ja/doc/obnizos/os_overview)に対応しています

**Python 3.6以上**で動作します。

<img src="https://object-storage.tyo1.conoha.io/v1/nc_35a49f4e51c74e35ad3493c52d37f63e/images/obniz-python-readme.gif" width="100%" />

## 使い方
```py
    import asyncio

    from obniz import Obniz


    async def onconnect(obniz):
        obniz.io0.drive("5v")
        obniz.io0.output(True)
        obniz.io1.pull("3v")
        obniz.io1.drive("open-drain")
        obniz.io1.output(False)
        obniz.io2.drive("3v")
        obniz.io2.output(True)

        def callback(voltage):
            print("change to {} v".format(voltage))

        obniz.ad3.start(callback)

        pwm = obniz.get_free_pwm()
        pwm.start({"io": 4})
        pwm.freq(1000)
        pwm.duty(50)

        uart = obniz.getFreeUart()
        uart.start({"tx": 5, "rx": 6, "baud": 9600})

        def onreceive(data, text):
            print(data)

        uart.onreceive = onreceive

        uart.send("Hello")


    obniz = Obniz('0000-0000')
    obniz.onconnect = onconnect

    asyncio.get_event_loop().run_forever()
```

## インストール

pipでインストールします。
```shell
  pip install obniz
```
そしてpythonの中でimportして下さい。
```python
  from obniz import Obniz
```

## 接続

[詳細](https://obniz.io/doc/sdk/doc/connection)

obnizをobniz idを使ってインスタンス化します。 そして接続が完了した時に呼ばれる関数をセットします。
```python
    import asyncio


    async def onconnect(obniz):
        pass


    obniz = Obniz('0000-0000')
    obniz.onconnect = onconnect

    asyncio.get_event_loop().run_forever()
```

接続完了後にobnizやobnizにつながれた部品を扱えます。
```python
    async def onconnect(obniz):
        obniz.io0.drive("5v")
        obniz.io0.output(True)
        obniz.io1.pull("3v")
        obniz.io1.drive("open-drain")
        obniz.io1.output(False)
        obniz.io2.drive("3v")
        obniz.io2.output(True)

        def callback(voltage):
            print("change to {} v".format(voltage))

        obniz.ad3.start(callback)

        pwm = obniz.get_free_pwm()
        pwm.start({"io": 4})
        pwm.freq(1000)
        pwm.duty(50)

        uart = obniz.getFreeUart()
        uart.start({"tx": 5, "rx": 6, "baud": 9600})

        def onreceive(data, text):
            print(data)

        uart.onreceive = onreceive

        uart.send("Hello")
```

## Example
TensorFlowなどのpythonライブラリもとても簡単に行なえます。
(`tensorflow` と `opencv-python` のインストールが必要です)
```py
    import asyncio

    from obniz import Obniz

    import cv2
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    fashion_mnist = keras.datasets.fashion_mnist

    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    train_images = train_images / 255.0

    test_images = test_images / 255.0

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    model.compile(optimizer=tf.train.AdamOptimizer(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    model.fit(train_images, train_labels, epochs=5)

    test_loss, test_acc = model.evaluate(test_images, test_labels)

    print('Test accuracy:', test_acc)

    def set_angle(pwm, angle):
        max = 2.4
        min = 0.5
        val = ((max - min) * angle) / 180.0 + min
        pwm.pulse(val)


    async def onconnect(obniz):
        obniz.io0.output(False)
        obniz.io1.output(True)

        pwm = obniz.get_free_pwm()
        pwm.start({"io": 2})
        pwm.freq(50)

        cap = cv2.VideoCapture(0)

        prev = None

        while True:
            ret, frame = cap.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)

            height, width = frame.shape
            x = height if height < width else width
            y = height if height < width else width
            square= np.zeros((x, y), np.uint8)

            x1 = int((width-x)/2)
            x2 = int(width-(width-x)/2)
            y1 = int((height-y)/2)
            y2 = int(height-(height-y)/2)
            square = frame[y1:y2, x1:x2]

            cv2.imshow("frame", square)

            img = cv2.resize(square, (28, 28), interpolation = cv2.INTER_AREA)

            img = (np.expand_dims(img / 255.0, 0))

            predictions_single = model.predict(img)

            answer = np.argmax(predictions_single[0])

            if prev != answer:
                print("answer: {}".format(class_names[answer]))
                set_angle(pwm, answer / 9 * 180)

            prev = answer

            if cv2.waitKey(1) & 0xFF == ord('q'):
                asyncio.get_event_loop().stop()
                break

            await asyncio.sleep(0.1)

        cap.release()
        cv2.destroyAllWindows()

    obniz = Obniz('0000-0000')
    obniz.debugprint = True
    obniz.onconnect = onconnect

    asyncio.get_event_loop().run_forever()
```

## ドキュメント
[公式サイト](https://obniz.io/doc/)
