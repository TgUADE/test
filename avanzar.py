import serial
import serial.tools.list_ports
import time

BAUDRATE = 115200
VELOCIDAD = 100  # rango: 0 a 999


def encontrar_puerto_stm32():
    puertos = serial.tools.list_ports.comports()
    for port in puertos:
        desc = (port.description or "").upper()
        # STM32 Nucleo via ST-Link (VID 0x0483) o via CP2102 USB-UART (VID 0x10C4)
        if port.vid in (0x0483, 0x10C4) or "STM" in desc or "NUCLEO" in desc or "CP210" in desc:
            return port.device
    # Si solo hay un puerto disponible, usarlo directamente
    if len(puertos) == 1:
        return puertos[0].device
    return None


def enviar(ser, comando):
    ser.write(comando.encode("ascii"))
    time.sleep(0.05)
    respuesta = ser.read_all().decode("ascii", errors="ignore").strip()
    if respuesta:
        print(f"  placa: {respuesta}")


puerto = encontrar_puerto_stm32()
if puerto is None:
    print("No se encontro el F401RE. Puertos disponibles:")
    for p in serial.tools.list_ports.comports():
        print(f"  {p.device} - {p.description}")
    exit(1)

print(f"Conectando a {puerto} ({BAUDRATE} baud)...")

with serial.Serial(puerto, BAUDRATE, timeout=0.2) as ser:
    time.sleep(1)

    print("Habilitando motor (KL 30)...")
    enviar(ser, "#kl:30;;\r\n")
    time.sleep(0.5)

    print(f"Avanzando a velocidad {VELOCIDAD}...")
    enviar(ser, f"#speed:{VELOCIDAD};;\r\n")

    time.sleep(5)

    print("Frenando...")
    enviar(ser, "#speed:0;;\r\n")
    time.sleep(0.2)
    enviar(ser, "#kl:0;;\r\n")

print("Listo.")
