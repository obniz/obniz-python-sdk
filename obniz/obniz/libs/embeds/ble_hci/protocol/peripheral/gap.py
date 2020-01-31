from pyee import EventEmitter

class Gap:
    ee = EventEmitter()
    def __init__(self, hci):
        self._hci = hci

        self._advertiseState = None

        # @self._hci.ee.on('error')
        # def onHciError():
        #     self.onHciError()
        # @self._hci.ee.on('leAdvertisingParametersSet')
        # def onHciLeAdvertisingParametersSet():
        #     self.onHciLeAdvertisingParametersSet()
        # @self._hci.ee.on('leAdvertisingDataSet')
        # def onHciLeAdvertisingDataSet():
        #     self.onHciLeAdvertisingDataSet()
        # @self._hci.ee.on('leScanResponseDataSet')
        # def onHciLeScanResponseDataSet():
        #     self.onHciLeScanResponseDataSet()
        # @self._hci.ee.on('leAdvertiseEnableSet')
        # def onHciLeAdvertiseEnableSet():
        #     self.onHciLeAdvertiseEnableSet()

    # def onHciError(self, error):
    #     pass