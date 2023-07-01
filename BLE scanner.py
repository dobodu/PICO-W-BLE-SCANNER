import time, bluetooth, struct

devices = []      

# Advertising byte type

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_SHORTNAME = const(0x08)
_ADV_TYPE_UUID16_COMPLETE = const(0x03)
_ADV_TYPE_UUID32_COMPLETE = const(0x05)
_ADV_TYPE_UUID128_COMPLETE = const(0x07)
_ADV_TYPE_UUID16_MORE = const(0x02)
_ADV_TYPE_UUID32_MORE = const(0x04)
_ADV_TYPE_UUID128_MORE = const(0x06)
_ADV_TYPE_TX_LEVEL = const(0x0A)
_ADV_TYPE_CLASS_DEVICE = const(0x0D)
_ADV_TYPE_SIMPLE_PAIRING_HASH = const(0x0E)
_ADV_TYPE_SIMPLE_PAIRING_RANDOM = const(0x0F)
_ADV_TYPE_APPEARANCE = const(0x19)

#Bluetooth IRQ SCAN RESULT ADV TYPE
_ADV_IND = 0x00
_ADV_DIRECT_IND = 0x01
_ADV_SCAN_IND = 0x02
_ADV_NONCONN_IND = 0x03
_ADV_SCAN_RESP = 0x04

def decode_services(payload):
    services = []
    for u in decode_field(payload, _ADV_TYPE_UUID16_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<h", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID32_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack("<d", u)[0]))
    for u in decode_field(payload, _ADV_TYPE_UUID128_COMPLETE):
        services.append(bluetooth.UUID(u))
    return services

def decode_field(payload, adv_type):
    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2 : i + payload[i] + 1])
        i += 1 + payload[i]
    return result

def decode_name(payload):
    n = decode_field(payload, _ADV_TYPE_NAME)
    return str(n[0], "utf-8") if n else "Unkown"

def decode_mac(payload):
    return payload[-6:].hex(":").upper()

def irq_handler(irq_ble, data_ble):
    if irq_ble == 5:
        add_type,  addr, adv_type, signal, data = data_ble
        mac = decode_mac(addr)
        existing_dev = [index for index, row in enumerate(devices) if mac in row]
        if adv_type in (_ADV_IND, _ADV_DIRECT_IND): 
            if existing_dev == []:
                devices.append([mac, decode_services(data), "", signal])
        elif adv_type == _ADV_SCAN_RESP:
            if existing_dev != []:
                devices[existing_dev[0]][2] = decode_name(data)

ble = bluetooth.BLE()
ble.irq(irq_handler)
ble.active(True)
ble.gap_scan(1000, 6250, 6250, True)
time.sleep_ms(2000)
print(devices)
