import struct
import re
from pyee import EventEmitter

class Gap:
    ee = EventEmitter()
    def __init__(self, hci):
        self._hci = hci

        self._scan_state = None
        self._scan_filter_duplicates = None
        self._discoveries = {}

        # @self._hci.ee.on('error')
        # def on_hci_error():
        #     self.on_hci_error()
        
        @self._hci.ee.on('le_scan_parameters_set')
        def on_hci_le_scan_parameters_set():
            self.on_hci_le_scan_parameters_set()
        @self._hci.ee.on('le_scan_enable_set')
        def on_hci_le_scan_enable_set(status):
            self.on_hci_le_scan_enable_set(status)
        @self._hci.ee.on('le_advertising_report')
        def on_hci_le_advertising_report(status, typ, address, address_type, eir, rssi):
            self.on_hci_le_advertising_report(status, typ, address, address_type, eir, rssi)
        @self._hci.ee.on('le_scan_enable_set_cmd')
        def on_le_scan_enable_set_cmd():
            self.on_le_scan_enable_set_cmd()
        @self._hci.ee.on('le_advertising_parameters_set')
        def on_hci_le_advertising_parameters_set():
            self.on_hci_le_advertising_parameters_set()
        @self._hci.ee.on('le_advertising_data_set')
        def on_hci_le_advertising_data_set():
            self.on_hci_le_advertising_data_set()
        @self._hci.ee.on('le_scan_response_data_set')
        def on_hci_le_scan_response_data_set():
            self.on_hci_le_scan_response_data_set()
        @self._hci.ee.on('le_advertise_enable_set')
        def on_hci_le_advertise_enable_set():
            self.on_hci_le_advertise_enable_set()

    def start_scanning(self, allow_duplicates):
        self._scan_state = 'starting'
        self._scan_filter_duplicates = not allow_duplicates

        # Always set scan parameters before scanning
        # https://www.bluetooth.org/docman/handlers/downloaddoc.ashx?doc_id=229737
        # p106 - p107
        self._hci.set_scan_enabled(False, True)
        self._hci.set_scan_parameters()
        self._hci.set_scan_enabled(True, self._scan_filter_duplicates)

    def stop_scanning(self):
        self._scan_state = 'stopping'

        self._hci.set_scan_enabled(False, True)

    def on_hci_error(self, error):
        pass

    def on_hci_le_scan_parameters_set(self):
        pass

    def on_hci_le_scan_enable_set(self, status):
        if not status == 0:
            return
        if self._scan_state == 'starting':
            self._scan_state = 'started'
        
            self.ee.emit('scan_start', self._scan_filter_duplicates) # -> central.binding
        elif self._scan_state == 'stopping':
            self._scan_state = 'stopped'

            self.ee.emit('scan_stop')  # -> central.binding

    def on_le_scan_enable_set_cmd(self, enable, filter_duplicates):
        print('wip: on_le_scan_enable_set_cmd')

    def on_hci_le_advertising_report(self, status, typ, address, address_type, eir, rssi):
        previously_discovered = address in self._discoveries # !!this._discoveries[address];
        if previously_discovered:
            advertisement = self._discoveries[address]["advertisement"] if "advertisement" in self._discoveries[address] else None
            discovery_count = self._discoveries[address]["count"] if "count" in self._discoveries[address] else None
            has_scan_response = self._discoveries[address]["hasScanResponse"] if "hasScanResponse" in self._discoveries[address] else None
        else:
            advertisement = {
                "localName": None,
                "txPowerLevel": None,
                "manufacturerData": None,
                "serviceData": [],
                "serviceUuids": [],
                "solicitationServiceUuids": [],
                "advertisementRaw": [],
                "scanResponseRaw": [],
                "raw": [],
            }
            discovery_count = 0
            has_scan_response = False


        if typ == 0x04:
            has_scan_response = True

            if len(eir) > 0:
                advertisement["scanResponseRaw"] = eir

        else:
            # # reset service data every non-scan response event
            advertisement["serviceData"] = []
            advertisement["serviceUuids"] = []
            advertisement["serviceSolicitationUuids"] = []

            if len(eir) > 0:
                advertisement["advertisementRaw"] = eir

        discovery_count += 1

        i = 0
        j = 0
        service_uuid = None
        service_solicitation_uuid = None

        while i + 1 < len(eir):
            length = eir[i]

            if length < 1:
                break

            # https://www.bluetooth.org/en-us/specification/assigned-numbers/generic-access-profile
            eir_type = eir[i + 1]

            if i + length + 1 > len(eir):
                break

            byts = eir[i + 2 : i +length + 1]

            # incomplete list of 16-bit service class u_u_i_d / complete list of 16-bit service class u_u_i_ds
            if eir_type == 0x02 or eir_type == 0x03:
                for j in range(len(byts) // 2):
                    j *= 2
                    service_uuid = format(struct.unpack("<h", bytearray(byts[j:j+2]))[0], 'x')
                    if service_uuid in advertisement["serviceUuids"]:
                        advertisement["serviceUuids"].append(service_uuid)
                break

            # incomplete list of 128-bit service class u_u_i_ds / complete list of 128-bit service class u_u_i_ds
            if eir_type == 0x06 or eir_type == 0x07:
                for j in range(len(byts)//16):
                    j *= 16
                    service_uuid = "".join(
                        reversed([re.match('.{1,2}', str(format(x, '02x'))).group() for x in byts[j:j+16]]))
                    if service_uuid in advertisement["serviceUuids"]:
                        advertisement["serviceUuids"].append(service_uuid)
                break

            # shortened local name / complete local name
            if eir_type == 0x08 or eir_type == 0x09:
                advertisement["local_name"] = "".join([chr(b) for b in byts])
                break

            if eir_type == 0x0a:
                # txPowerLevel
                advertisement["txPowerLevel"] = byts[0]
                break

            if eir_type == 0x14:
                print("wip: eir_type =", eir_type)
                # # list of 16 bit solicitation u_u_i_ds
                # for j=0; j < bytes.length; j += 2:
                #     service_solicitation_uuid=bytes.read_u_int16_l_e(j).to_string(16)
                # if advertisement.service_solicitation_uuids.index_of(service_solicitation_uuid) is -1:
                #     advertisement.service_solicitation_uuids.append(
                #         service_solicitation_uuid
                #     )
                break

            if eir_type == 0x15:
                print("wip: eir_type =", eir_type)
                # # list of 128 bit solicitation u_u_i_ds
                # for j=0; j < bytes.length; j += 16:
                #     service_solicitation_uuid=bytes
                #     .slice(j, j + 16)
                #     .to_string('hex')
                #     .match(/.{1, 2}/g)
                #     .reverse()
                #     .join('')
                #     if
                #     advertisement.service_solicitation_uuids.index_of(
                #         service_solicitation_uuid
                #     ) is -1:
                #     advertisement.service_solicitation_uuids.append(
                #         service_solicitation_uuid
                #     )
                break
            
            if eir_type == 0x16:
                print("wip: eir_type =", eir_type)
                # # 16-bit service data, there can be multiple occurences
                # let service_data_uuid=bytes
                # .slice(0, 2)
                # .to_string('hex')
                # .match(/.{1, 2}/g)
                # .reverse()
                # .join('')
                # let service_data=bytes.slice(2, bytes.length)

                # advertisement.service_data.append({
                #     uuid: service_data_uuid,
                #     data: service_data,
                # })
                break
            
            if eir_type == 0x20:
                print("wip: eir_type =", eir_type)
                # # 32-bit service data, there can be multiple occurences
                # let service_data32_uuid=bytes
                # .slice(0, 4)
                # .to_string('hex')
                # .match(/.{1, 2}/g)
                # .reverse()
                # .join('')
                # let service_data32=bytes.slice(4, bytes.length)

                # advertisement.service_data.append({
                #     uuid: service_data32_uuid,
                #     data: service_data32,
                # })
                break
            
            if eir_type == 0x21:
                print("wip: eir_type =", eir_type)
                # # 128-bit service data, there can be multiple occurences

                # let service_data128_uuid=bytes
                # .slice(0, 16)
                # .to_string('hex')
                # .match(/.{1, 2}/g)
                # .reverse()
                # .join('')
                # let service_data128=bytes.slice(16, bytes.length)

                # advertisement.service_data.append({
                #     uuid: service_data128_uuid,
                #     data: service_data128,
                # })
                break
            
            if eir_type == 0x1f:  # list of 32 bit solicitation u_u_i_ds
                print("wip: eir_type =", eir_type)
                # for j=0; j < bytes.length; j += 4:
                # service_solicitation_uuid=bytes.read_u_int32_l_e(j).to_string(16)
                # if advertisement.service_solicitation_uuids.index_of(service_solicitation_uuid) is -1:
                # advertisement.service_solicitation_uuids.append(
                #     service_solicitation_uuid
                # )
                break

            if eir_type == 0xff:  # manufacturer specific data
                advertisement["manufacturerData"] = byts
                break

            i += length + 1
            
        if typ == 0x04 and previously_discovered:
            connectable = self._discoveries[address]["connectable"] if "connectable" in self._discoveries[address] else None
        else:
            connectable = not typ == 0x03

        self._discoveries[address] = {
            "address": address,
            "addressType": address_type,
            "connectable": connectable,
            "advertisement": advertisement,
            "rssi": rssi,
            "count": discovery_count,
            "hasScanResponse": has_scan_response,
        }

        # only report after a scan response event or if non-connectable or more than one discovery without a scan response, so more data can be collected
        if typ == 0x04 or not connectable or (discovery_count > 1 and not has_scan_response): # or process.env.NOBLE_REPORT_ALL_HCI_EVENTS:
            self.ee.emit('discover', status, address, address_type, connectable, advertisement, rssi)


    # # def...

    def on_hci_le_advertising_parameters_set(self):
        pass

    def on_hci_le_advertising_data_set(self):
        pass
    def on_hci_le_scan_response_data_set(self):
        pass

    def on_hci_le_advertise_enable_set(self):
        print('wip: on_hci_le_advertise_enable_set')
