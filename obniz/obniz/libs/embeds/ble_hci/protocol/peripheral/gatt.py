ATT_OP_ERROR = 0x01
ATT_OP_MTU_REQ = 0x02
ATT_OP_MTU_RESP = 0x03
ATT_OP_FIND_INFO_REQ = 0x04
ATT_OP_FIND_INFO_RESP = 0x05
ATT_OP_FIND_BY_TYPE_REQ = 0x06
ATT_OP_FIND_BY_TYPE_RESP = 0x07
ATT_OP_READ_BY_TYPE_REQ = 0x08
ATT_OP_READ_BY_TYPE_RESP = 0x09
ATT_OP_READ_REQ = 0x0a
ATT_OP_READ_RESP = 0x0b
ATT_OP_READ_BLOB_REQ = 0x0c
ATT_OP_READ_BLOB_RESP = 0x0d
ATT_OP_READ_MULTI_REQ = 0x0e
ATT_OP_READ_MULTI_RESP = 0x0f
ATT_OP_READ_BY_GROUP_REQ = 0x10
ATT_OP_READ_BY_GROUP_RESP = 0x11
ATT_OP_WRITE_REQ = 0x12
ATT_OP_WRITE_RESP = 0x13
ATT_OP_WRITE_CMD = 0x52
ATT_OP_PREP_WRITE_REQ = 0x16
ATT_OP_PREP_WRITE_RESP = 0x17
ATT_OP_EXEC_WRITE_REQ = 0x18
ATT_OP_EXEC_WRITE_RESP = 0x19
ATT_OP_HANDLE_NOTIFY = 0x1b
ATT_OP_HANDLE_IND = 0x1d
ATT_OP_HANDLE_CNF = 0x1e
ATT_OP_SIGNED_WRITE_CMD = 0xd2

GATT_PRIM_SVC_UUID = 0x2800
GATT_INCLUDE_UUID = 0x2802
GATT_CHARAC_UUID = 0x2803

GATT_CLIENT_CHARAC_CFG_UUID = 0x2902
GATT_SERVER_CHARAC_CFG_UUID = 0x2903

ATT_ECODE_SUCCESS = 0x00
ATT_ECODE_INVALID_HANDLE = 0x01
ATT_ECODE_READ_NOT_PERM = 0x02
ATT_ECODE_WRITE_NOT_PERM = 0x03
ATT_ECODE_INVALID_PDU = 0x04
ATT_ECODE_AUTHENTICATION = 0x05
ATT_ECODE_REQ_NOT_SUPP = 0x06
ATT_ECODE_INVALID_OFFSET = 0x07
ATT_ECODE_AUTHORIZATION = 0x08
ATT_ECODE_PREP_QUEUE_FULL = 0x09
ATT_ECODE_ATTR_NOT_FOUND = 0x0a
ATT_ECODE_ATTR_NOT_LONG = 0x0b
ATT_ECODE_INSUFF_ENCR_KEY_SIZE = 0x0c
ATT_ECODE_INVAL_ATTR_VALUE_LEN = 0x0d
ATT_ECODE_UNLIKELY = 0x0e
ATT_ECODE_INSUFF_ENC = 0x0f
ATT_ECODE_UNSUPP_GRP_TYPE = 0x10
ATT_ECODE_INSUFF_RESOURCES = 0x11

ATT_CID = 0x0004

class Gatt:
    def __init__(self, hci):
        self.max_mtu = 256
        self._mtu = 23
        self._prepare_write_request = None

        self.set_services([])

        # self.on_acl_stream_data_binded = self.on_acl_stream_data(self)
        # self.on_acl_stream_end_binded = self.on_acl_stream_end(self)

    def set_services(self, services):
        print("wip")
        all_services = []
        all_services.append(services)

        self._handles = []

        handle = 0

        for service in all_services:
            print(service)
            handle += 1
            service_handle = handle

            self._handles[service_handle] = {
                'type': 'service',
                'uuid': service.uuid,
                'attribute': service,
                'startHandle': service_handle
            }

            for characteristic in service.characteristics:
                properties = 0
                secure = 0

                if "read" in characteristic.properties:
                    properties |= 0x02

                    if "read" in characteristic.secure:
                        secure |= 0x02

                if "writeWithoutResoinse" in characteristic.properties:
                    properties |= 0x04

                    if "writeWithoutResoinse" in characteristic.secure:
                        secure |= 0x04

                if "write" in characteristic.properties:
                    properties |= 0x08

                    if "write" in characteristic.secure:
                        secure |= 0x08

                if "notify" in characteristic.properties:
                    properties |= 0x10

                    if "notify" in characteristic.secure:
                        secure |= 0x10

                if "nindicate" in characteristic.properties:
                    properties |= 0x20

                    if "nindicate" in characteristic.secure:
                        secure |= 0x20

                handle += 1
                characteristic_handle = handle

                handle += 1
                characteristic_value_handle = handle

                self._handles[characteristic_handle] = {
                    'type': 'characteristic',
                    'uuid': characteristic.uuid,
                    'properties': properties,
                    'secure': secure,
                    'attribute': characteristic,
                    'startHandle': characteristic_handle,
                    'valueHandle': characteristic_value_handle,
                }

                self._handles[characteristic_value_handle] = {
                    'type': 'characteristicValue',
                    'handle': characteristic_value_handle,
                    'value': characteristic.value,
                }
