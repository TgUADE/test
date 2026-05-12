import serial
import serial.tools.list_ports
import threading
import time

BAUDRATE = 115200

def encontrar_puerto_stm32():
    puertos = serial.tools.list_ports.comports()
    for port in puertos:
        if port.vid in (0x0483, 0x10C4):
            return port.device
    return None

puerto = encontrar_puerto_stm32()
print(f"Conectando a {puerto}...")
print("Escribi comandos y presiona Enter. Ctrl+C para salir.\n")

ser = serial.Serial(puerto, BAUDRATE, timeout=0.1)
time.sleep(1)
ser.reset_input_buffer()

def leer():
    while True:
        if ser.in_waiting:
            data = ser.read(ser.in_waiting)
            print(f"\n<< {data.decode('ascii', errors='replace')}", end="", flush=True)
        time.sleep(0.05)

t = threading.Thread(target=leer, daemon=True)
t.start()

try:
    while True:
        cmd = input(">> ")
        ser.write((cmd + "\r\n").encode("ascii"))
except KeyboardInterrupt:
    ser.close()
    print("\nCerrado.")
