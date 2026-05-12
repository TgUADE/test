import serial
import serial.tools.list_ports
import time

BAUDRATE = 115200

def encontrar_puerto_stm32():
    puertos = serial.tools.list_ports.comports()
    for port in puertos:
        desc = (port.description or "").upper()
        if port.vid in (0x0483, 0x10C4) or "STM" in desc or "NUCLEO" in desc or "CP210" in desc:
            return port.device
    if len(puertos) == 1:
        return puertos[0].device
    return None

puerto = encontrar_puerto_stm32()
print(f"Escuchando {puerto} a {BAUDRATE} baud... (Ctrl+C para salir)\n")

with serial.Serial(puerto, BAUDRATE, timeout=1) as ser:
    ser.reset_input_buffer()
    while True:
        data = ser.read(256)
        if data:
            try:
                print(data.decode("ascii"), end="", flush=True)
            except:
                print(data.hex(), end=" ", flush=True)
