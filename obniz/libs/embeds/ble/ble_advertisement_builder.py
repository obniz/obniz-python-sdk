# from .bleHelper import BleHelper


class BleAdvertisementBuilder:
    def __init__(self, obniz, json):
        self.obniz = obniz
        self.rows = {}

        if json:
            if "localName" in json:
                self.set_complete_local_name(json["localName"])

            if (
                "manufacturerData" in json
                and "companyCode" in json["manufacturerData"]
                and "data" in json["manufacturerData"]
            ):
                self.set_manufacturer_specific_data(
                    json["manufacturerData"]["companyCode"],
                    json["manufacturerData"]["data"],
                )

            if "serviceUuids" in json:
                for uuid in json["serviceUuids"]:
                    self.setUuid(uuid)

        if self.extend_eval_json:
            self.extend_eval_json(json)

    def set_row(self, type, data):
        self.rows[type] = data

    def get_row(self, type):
        return self.rows.get(type, [])

    def build(self):
        data = []
        for key in sorted(self.rows.keys()):
            if len(self.rows[key]) == 0:
                continue

            data.append(len(self.rows[key]) + 1)
            data.append(int(key))
            data.extend(self.rows[key])

        if len(data) > 31:
            self.obniz.error(
                "Too large data. Advertise/ScanResponse data are must be less than 32 byte."
            )

        return data

    def set_string_data(self, type, string):
        data = []

        for c in string:
            data.append(ord(c))

        self.set_row(type, data)

    #     setShortenedLocalName(name) {
    #         self.setStringData(0x08, name)
    #     }

    def set_complete_local_name(self, name):
        self.set_string_data(0x09, name)

    def set_manufacturer_specific_data(self, company_code, data):
        row = []
        row.append(company_code & 0xFF)
        row.append((company_code >> 8) & 0xFF)
        row.extend(data)
        self.set_row(0xFF, row)

    #     setUuid(uuid) {
    #         uuidData = self.convertUuid(uuid)
    #         type = { 16: 0x06, 4: 0x04, 2: 0x02 }[uuidData.length]
    #         self.set_row(type, uuidData)
    #     }

    # 　　 convertUuid(uuid) {
    #         uuidNumeric = BleHelper.uuidFilter(uuid)
    #         if (
    #             uuidNumeric.length !== 32 and
    #             uuidNumeric.length !== 8 and
    #             uuidNumeric.length !== 4
    #         ) {
    #             self.obniz.error(
    #                 'BLE uuid must be 16/32/128 bit . '
    #                 + '(example: c28f0ad5-a7fd-48be-9fd0-eae9ffd3a8bb for 128bit)'
    #             )
    #         }

    #         data = []
    #         for (i = uuidNumeric.length i > 1 i -= 2) {
    #             data.append(parseInt(uuidNumeric[i - 2] + uuidNumeric[i - 1], 16))
    #         }
    #         return data
    #     }

    #     setIbeaconData(uuid, major, minor, txPower) {
    #         data = []
    #         data.append(0x02, 0x15) // fixed data

    #         uuidData = self.convertUuid(uuid)
    #         Array.prototype.append.apply(data, uuidData)

    #         data.append((major >> 8) & 0xff)
    #         data.append((major >> 0) & 0xff)
    #         data.append((minor >> 8) & 0xff)
    #         data.append((minor >> 0) & 0xff)
    #         data.append((txPower >> 0) & 0xff)

    #         self.setManufacturerSpecificData(0x004c, data)
    #         return
    #     }

    def extend_eval_json(self, json):
        if json:
            if "flags" in json:
                if "limited_discoverable_mode" in json["flags"]:
                    self.set_le_limited_discoverable_mode_flag()
                if "general_discoverable_mode" in json["flags"]:
                    self.set_le_general_discoverable_mode_flag()
                if "br_edr_not_supported" in json["flags"]:
                    self.set_br_edr_not_supported_flag()
                if "le_br_edr_controller" in json["flags"]:
                    self.set_le_br_edr_controller_flag()
                if "le_br_edr_host" in json["flags"]:
                    self.set_le_br_edr_host_flag()

    def set_flags(self, flag):
        data = self.get_row(0x01)
        if len(data):
            data[0] = data[0] | flag
        else:
            data.append(flag)
        self.set_row(0x01, data)

    def set_le_limited_discoverable_mode_flag(self):
        self.set_flags(0x01)

    def set_le_general_discoverable_mode_flag(self):
        self.set_flags(0x02)

    def set_br_edr_not_supported_flag(self):
        self.set_flags(0x04)

    def set_le_br_edr_controller_flag(self):
        self.set_flags(0x08)

    def set_le_br_edr_host_flag(self):
        self.set_flags(0x10)
