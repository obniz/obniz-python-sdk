from pyee import EventEmitter

class Gap:
    ee = EventEmitter()
    def __init__(self, hci):
        self._hci = hci

        self._advertiseState = None

        # @self._hci.ee.on('error')
        # def on_hci_error():
        #     self.on_hci_error()
        # @self._hci.ee.on('le_advertising_parameters_set')
        # def on_hci_le_advertising_parameters_set():
        #     self.on_hci_le_advertising_parameters_set()
        # @self._hci.ee.on('le_advertising_data_set')
        # def on_hci_le_advertising_data_set():
        #     self.on_hci_le_advertising_data_set()
        # @self._hci.ee.on('le_scan_response_data_set')
        # def on_hci_le_scan_response_data_set():
        #     self.on_hci_le_scan_response_data_set()
        # @self._hci.ee.on('le_advertise_enable_set')
        # def on_hci_le_advertise_enable_set():
        #     self.on_hci_le_advertise_enable_set()

    # def on_hci_error(self, error):
    #     pass