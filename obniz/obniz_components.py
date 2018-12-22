from .libs.embeds.ble.ble import ObnizBLE
from .libs.embeds.switch import ObnizSwitch
from .libs.io_peripherals.ad import PeripheralAD
from .libs.io_peripherals.i2c import PeripheralI2C
from .libs.io_peripherals.io import PeripheralIO
from .libs.io_peripherals.io_ import PeripheralIO_
from .libs.io_peripherals.pwm import PeripheralPWM
from .libs.io_peripherals.spi import PeripheralSPI
from .libs.io_peripherals.uart import PeripheralUART
from .libs.measurements.logicanalyzer import LogicAnalyzer
from .libs.measurements.measure import ObnizMeasure
from .obniz_connection import ObnizConnection


class ObnizComponents(ObnizConnection):
    def __init__(self, id, options):
        super().__init__(id, options)

        self.pong_observers = []

    def close(self):
        super().close()
        if self.options["reset_obniz_on_ws_disconnection"]:
            self._reset_components()

    def _prepare_components(self):
        setattr(self, "io", PeripheralIO_(self))

        for i in range(0, 12):
            setattr(self, "io" + str(i), PeripheralIO(self, i))

        for i in range(0, 12):
            setattr(self, "ad" + str(i), PeripheralAD(self, i))

        for i in range(0, 2):
            setattr(self, "uart" + str(i), PeripheralUART(self, i))

        for i in range(0, 2):
            setattr(self, "spi" + str(i), PeripheralSPI(self, i))

        for i in range(0, 1):
            setattr(self, "i2c" + str(i), PeripheralI2C(self, i))

        for i in range(0, 6):
            setattr(self, "pwm" + str(i), PeripheralPWM(self, i))

        # setattr(self, "display", Display(self))
        setattr(self, "switch", ObnizSwitch(self))
        setattr(self, "logicAnalyzer", LogicAnalyzer(self))
        setattr(self, "ble", ObnizBLE(self))
        setattr(self, "measure", ObnizMeasure(self))

        # setattr(self, "util", ObnizUtil(self))

    def _reset_components(self):
        self.print_debug("components state resets")
        for i in range(0, 12):
            getattr(self, "io" + str(i))._reset()

        for i in range(0, 12):
            getattr(self, "ad" + str(i))._reset()

        for i in range(0, 2):
            getattr(self, "uart" + str(i))._reset()

        for i in range(0, 2):
            getattr(self, "spi" + str(i))._reset()

        for i in range(0, 1):
            getattr(self, "i2c" + str(i))._reset()

        for i in range(0, 6):
            getattr(self, "pwm" + str(i))._reset()

        # self.display._reset()
        self.switch._reset()
        self.logicAnalyzer._reset()
        self.ble._reset()
        self.measure._reset()

    def notify_to_module(self, obj):
        super().notify_to_module(obj)
        notify_handlers = ["io", "uart", "spi", "i2c", "ad"]
        for peripheral in notify_handlers:
            i = 0
            while hasattr(self, peripheral + str(i)):
                module_value = obj.get(peripheral + str(i))
                if module_value is not None:
                    getattr(self, peripheral + str(i)).notified(module_value)
                i += 1

        names = ["switch", "ble", "measure"]
        for name in names:
            if name in obj:
                getattr(self, name).notified(obj[name])

        if "logic_analyzer" in obj:
            self.logicAnalyzer.notified(obj["logic_analyzer"])

    #   handleSystemCommand(wsObj) {
    #     super.handleSystemCommand(wsObj)
    #     // ping pong
    #     if (wsObj.pong) {
    #       for (callback of self.pongObservers) {
    #         callback(wsObj)
    #       }
    #     }
    #   }

    def add_pong_observer(self, callback):
        if callback:
            self.pong_observers.append(callback)

    #   removePongObserver(callback) {
    #     if (self.pongObservers.includes(callback)) {
    #       index = self.pongObservers.indexOf(callback)
    #       self.pongObservers.splice(index, 1)
    #     }
    #   }

    def is_valid_io(self, io):
        return type(io) is int and io >= 0 and io < 12

    #   setVccGnd(vcc, gnd, drive) {
    #     if (self.isValidIO(vcc)) {
    #       if (drive) {
    #         self.getIO(vcc).drive(drive)
    #       }
    #       self.getIO(vcc).output(true)
    #     }

    #     if (self.isValidIO(gnd)) {
    #       if (drive) {
    #         self.getIO(gnd).drive(drive)
    #       }
    #       self.getIO(gnd).output(false)
    #     }
    #   }

    def get_io(self, io):
        if not self.is_valid_io(io):
            raise Exception("io " + str(io) + " is not valid io")

        return getattr(self, "io" + str(io))

    def get_ad(self, io):
        if not self.is_valid_io(io):
            raise Exception("ad " + str(io) + " is not valid io")

        return getattr(self, "ad" + str(io))

    def get_free_pwm(self):
        i = 0
        for i in range(0, 6):
            pwm = getattr(self, "pwm" + str(i))
            if not pwm:
                break

            if not pwm.is_used():
                pwm.used = True
                return pwm

        raise Exception("No More PWM Available. max = " + i)


#   getFreeI2C() {
#     i = 0
#     for (i = 0 i < 1 i++) {
#       i2c = self['i2c' + i]
#       if (!i2c) {
#         break
#       }
#       if (!i2c.isUsed()) {
#         i2c.used = true
#         return i2c
#       }
#     }
#     throw new Error('No More I2C Available. max = ' + i)
#   }

#   getI2CWithConfig(config) {
#     if (typeof config !== 'object') {
#       throw new Error('getI2CWithConfig need config arg')
#     }
#     if (config.i2c) {
#       return config.i2c
#     }
#     i2c = self.getFreeI2C()
#     i2c.start(config)
#     return i2c
#   }

#   getFreeSpi() {
#     i = 0
#     for (i = 0 i < 2 i++) {
#       spi = self['spi' + i]
#       if (!spi) {
#         break
#       }
#       if (!spi.isUsed()) {
#         spi.used = true
#         return spi
#       }
#     }
#     throw new Error('No More SPI Available. max = ' + i)
#   }

#   getSpiWithConfig(config) {
#     if (typeof config !== 'object') {
#       throw new Error('getSpiWithConfig need config arg')
#     }
#     if (config.spi) {
#       return config.spi
#     }
#     spi = self.getFreeSpi()
#     spi.start(config)
#     return spi
#   }

#   getFreeUart() {
#     i = 0
#     for (i = 0 i < 2 i++) {
#       uart = self['uart' + i]
#       if (!uart) {
#         break
#       }
#       if (!uart.isUsed()) {
#         uart.used = true
#         return uart
#       }
#     }
#     throw new Error('No More uart Available. max = ' + i)
#   }
# }
