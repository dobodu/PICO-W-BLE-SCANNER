# PICO-W-BLE-SCANNER
Micropython BLE scanner for RP2040 Wireless

A big thank to Damien George helping me to catch BLE name in advertising.

The program is very simple : is scans BLE environnement and gives back information like

[['50:BA:3F:C4:49:03', [UUID(0xfe9f)], 'Unkown', -93], ['AA:BB:CC:12:22:33', [UUID(0xfff0)], 'OBDBLE', -67]]

Thus we have for example a BLE OBD2 dongle named "OBDBLE", with MAC Adress AA:BB:CC:12:22:33, UUID 0XFFF0, signal is -67dB
