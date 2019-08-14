# ENC03R_Module

Gyrosensor ENC03R Module.
It detect "Rotation Speed".

![](./enc03r.jpg)


## wired

```python
# Python Example
enc03r = obniz.wired(
    "ENC03R_Module",
    {"gnd": 0, "vcc": 1, "out2": 2, "out1": 3}
)
def onchange(val):
    print(val, "(deg/sec)")
enc03r.onchange1 = onchange
```


## onchange1, onchange2

Set callbacks.
The unit is deg/sec.

```python
# Python Example
enc03r = obniz.wired(
    "ENC03R_Module",
    {"gnd": 0, "vcc": 1, "out2": 2, "out1": 3}
)
def onchange(val):
    print(val, "(deg/sec)")
enc03r.onchange1 = onchange
enc03r.onchange2 = onchange
```

## [await]get1_wait,[await]get2_wait,

Get value once. 
The unit is deg/sec.

```python
# Python Example
enc03r = obniz.wired(
    "ENC03R_Module",
    {"gnd": 0, "vcc": 1, "out2": 2, "out1": 3}
)
val1 = await enc03r.get1_wait()
val2 = await enc03r.get2_wait()

print("1:", val1, "(deg/sec)")
print("2:", val2, "(deg/sec)")

```