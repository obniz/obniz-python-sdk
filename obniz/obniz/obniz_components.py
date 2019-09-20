from .libs.embeds.ble.ble import ObnizBLE
from .libs.embeds.display import Display
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
from .libs.hw.index import HW
from .obniz_connection import ObnizConnection
from .obniz_parts import ObnizParts

import attrdict
import asyncio


class ObnizComponents(ObnizParts):
    def __init__(self, id, options):
        super().__init__(id, options)

        self.pong_observers = []
        self._all_component_keys = []

    def close(self):
        super().close()
        if self.options["reset_obniz_on_ws_disconnection"]:
            self._reset_components()

    def _prepare_components(self):
        hwDefinition = HW.get_definition_for(self.hw)
        if hwDefinition is None:
            raise Exception(f"unknown hw {self.hw}")

        setattr(self, "io", PeripheralIO_(self))

        hw_peripherals = hwDefinition['peripherals']
        hw_embeds = hwDefinition['embeds']

        shared_map = {
            'logicAnalyzer': LogicAnalyzer,
            'measure': ObnizMeasure
        }

        peripheral_map = {
            'io': PeripheralIO,
            'ad': PeripheralAD,
            'uart': PeripheralUART,
            'spi': PeripheralSPI,
            'i2c': PeripheralI2C,
            'pwm': PeripheralPWM
        }

        embeds_map = {
            'display': Display,
            'switch': ObnizSwitch,
            'ble': ObnizBLE
        }

        for key in shared_map:
            classname = shared_map[key]
            setattr(self, key, classname(self))
            self._all_component_keys.append(key)

        for key in peripheral_map:
            if hw_peripherals[key]:
                units = hw_peripherals[key]['units']
                classname = peripheral_map[key]
                for unit_id in units:
                    unit_id = int(unit_id)
                    setattr(self, f"{key}{unit_id}", classname(self, unit_id))
                    self._all_component_keys.append(f"{key}{unit_id}")

        for key in embeds_map:
            if key in hw_embeds:
                classname = embeds_map[key]
                setattr(self, key, classname(self))
                self._all_component_keys.append(key)
        # setattr(self, "util", ObnizUtil(self))

    def _reset_components(self):
        self.print_debug("components state resets")

        for key in self._all_component_keys:
            # ToDo: Clarify why is it deleted?
            if key == 'display':
                continue
            getattr(self, key)._reset()

    def notify_to_module(self, obj):
        super().notify_to_module(obj)

        for key in self._all_component_keys:
            if key == 'logicAnalyzer':
                if 'logic_analyzer' in obj:
                    getattr(self, 'logicAnalyzer').notified(obj['logic_analyzer'])
            if key in obj:
                getattr(self, key).notified(obj[key])

    #   handleSystemCommand(wsObj) {
    #     super.handleSystemCommand(wsObj)
    #     // ping pong
    #     if (wsObj.pong) {
    #       for (callback of self.pongObservers) {
    #         callback(wsObj)
    #       }
    #     }
    #   }
    def handle_system_command(self, ws_obj):
        super().handle_system_command(ws_obj)
        # ping pong
        if ws_obj["pong"]:
            for tpl in self.pong_observers:
                future, callback = tpl
                ret = callback(ws_obj)
                if ret:
                    future.set_result(ret)

    def add_pong_observer(self, future, callback):
        if asyncio.isfuture(future) and callable(callback):
            future.add_done_callback(self.remove_pong_observer)
            self.pong_observers.append((future, callback))

    def remove_pong_observer(self, future):
        for i, tpl in enumerate(self.pong_observers):
            ftr, clb = tpl
            if ftr == future:
                self.pong_observers.pop(i)

    def is_valid_io(self, io):
        return type(io) is int and f'io{io}' in self._all_component_keys

    def set_vcc_gnd(self, vcc, gnd, drive=None):
        if self.is_valid_io(vcc):
            if drive:
                self.get_io(vcc).drive(drive)
            self.get_io(vcc).output(True)
        
        if self.is_valid_io(gnd):
            if drive:
                self.get_io(gnd).drive(drive)
            self.get_io(gnd).output(False)

    def get_io(self, io):
        if not self.is_valid_io(io):
            raise Exception("io " + str(io) + " is not valid io")

        return getattr(self, "io" + str(io))

    def get_ad(self, io):
        if not self.is_valid_io(io):
            raise Exception("ad " + str(io) + " is not valid io")

        return getattr(self, "ad" + str(io))

    def _get_free_peripheral_unit(self, peripheral):
        for key in self._all_component_keys:
            if key.find(peripheral) == 0:
                # "io" for "io0"
                if hasattr(self, key):
                    obj = getattr(self, key)
                    if not obj.is_used():
                        obj.used = True
                        return obj
        raise Exception(f'No More {peripheral} Available.')

    def get_free_pwm(self):
        return self._get_free_peripheral_unit('pwm')

    def get_free_i2c(self):
        return self._get_free_peripheral_unit('i2c')

    def get_i2c_with_config(self, config):
        if type(config) not in [dict, attrdict.default.AttrDefault]:
            raise Exception("get_i2c_with_config need config arg")
        if config.get("i2c"):
            return config.get("i2c")
        i2c = self.get_free_i2c()
        i2c.start(config)
        return i2c

    def get_free_spi(self):
        return self._get_free_peripheral_unit('spi')

    def get_spi_with_config(self, config):
        if type(config) not in [dict, attrdict.default.AttrDefault]:
            raise Exception("get_spi_with_config need config arg")
        if config.get("spi"):
            return config.get("spi")
        spi = self.get_free_spi()
        spi.start(config)
        return spi

    def _call_on_connect(self):
        self._prepare_components()
        super()._call_on_connect()

    def get_free_uart(self):
        return self._get_free_peripheral_unit('uart')
