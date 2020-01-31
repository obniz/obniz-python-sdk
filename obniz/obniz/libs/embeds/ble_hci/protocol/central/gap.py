from pyee import EventEmitter

class Gap:
    ee = EventEmitter()
    def __init__(self, hci):
        self._hci = hci

        self._scanState = None
        self._scanFilterDuplicates = None
        self._discoveries = {}

        # @self._hci.ee.on('error')
        # def onHciError():
        #     self.onHciError()
        
        @self._hci.ee.on('leScanParametersSet')
        def onHciLeScanParametersSet():
            self.onHciLeScanParametersSet()
        @self._hci.ee.on('leScanEnableSet')
        def onHciLeScanEnableSet(status):
            self.onHciLeScanEnableSet(status)
        # @self._hci.ee.on('leAdvertisingReport')
        # def onHciLeAdvertisingReport():
        #     self.onHciLeAdvertisingReport()
        # @self._hci.ee.on('leScanEnableSetCmd')
        # def onLeScanEnableSetCmd():
        #     self.onLeScanEnableSetCmd()
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

    def onHciLeScanParametersSet(self):
        pass

    def onHciLeScanEnableSet(self, status):
        if not status == 0:
            return
        if self._scanState == 'starting':
            self._scanState = 'started'
        
            self.ee.emit('scanStart', self._scanFilterDuplicates) # -> central.binding
        elif self._scanState == 'stopping':
            self._scanState = 'stopped'

            self.ee.emit('scanStop')  # -> central.binding
