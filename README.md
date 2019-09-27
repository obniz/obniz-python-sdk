# obniz.py: sdk for python

[![image](https://img.shields.io/pypi/pyversions/obniz.svg)](https://pypi.org/project/obniz/)

[obniz](https://obniz.io/) sdk for python.
You can use [obnizBoard](https://obniz.io/doc/obniz_board_hobby_90/hw_overview) or [obnizOS](https://obniz.io/doc/obnizos/os_overview).

Control obniz from python.

This sdk works with [obniz api](https://obniz.io/doc/about_obniz_api).

Compatible with **Python 3.6+**.

<img src="https://object-storage.tyo1.conoha.io/v1/nc_35a49f4e51c74e35ad3493c52d37f63e/images/obniz-python-readme.gif" width="100%" />

## Usage
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

## Installation

Install obniz via pip
```shell
  pip install obniz
```
and import it on python file.
```python
  from obniz import Obniz
```

## Connect

Details on [doc/connection](https://obniz.io/doc/sdk/doc/connection)

To use obniz, instantiate obniz with obniz id. and set onconnect callback function. It will be called when connected to obniz successfully.
```python
    import asyncio


    async def onconnect(obniz):
        pass


    obniz = Obniz('0000-0000')
    obniz.onconnect = onconnect

    asyncio.get_event_loop().run_forever()
```

You are able to use everything on obniz after connect.
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
Easy to integrate python libraries like TensorFlow.
(need to install `tensorflow` and `opencv-python`)
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

## Documentation
You can find the documentation on [the website](https://obniz.io/doc/).
