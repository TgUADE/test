import serial
import serial.tools.list_ports
import threading
import time

BAUDRATE = 115200
VELOCIDAD = 200  # rango: 0 a 500


def encontrar_puerto_stm32():
    puertos = serial.tools.list_ports.comports()
    for port in puertos:
        if port.vid in (0x0483, 0x10C4):
            return port.device
    if len(puertos) == 1:
        return puertos[0].device
    return None


def leer_respuestas(ser, stop_event):
    buffer = ""
    while not stop_event.is_set():
        if ser.in_waiting:
            buffer += ser.read(ser.in_waiting).decode("ascii", errors="replace")
            while ";;" in buffer:
                msg, buffer = buffer.split(";;", 1)
                if msg.strip():
                    print(f"  << placa: {msg.strip()}")
        time.sleep(0.05)


def enviar(ser, comando):
    print(f"  >> enviado: {comando.strip()}")
    ser.write(comando.encode("ascii"))
    time.sleep(0.3)


puerto = encontrar_puerto_stm32()
if puerto is None:
    print("No se encontro el F401RE. Puertos disponibles:")
    for p in serial.tools.list_ports.comports():
        print(f"  {p.device} - {p.description}")
    exit(1)

print(f"Conectando a {puerto} ({BAUDRATE} baud)...")

with serial.Serial(puerto, BAUDRATE, timeout=0.5) as ser:
    time.sleep(1)
    ser.reset_input_buffer()

    stop_event = threading.Event()
    t = threading.Thread(target=leer_respuestas, args=(ser, stop_event), daemon=True)
    t.start()

    print("\nInicializando bateria...")
    enviar(ser, "#batteryCapacity:6000;;\r\n")
    time.sleep(0.5)

    print("\nHabilitando motor (KL 30)...")
    enviar(ser, "#kl:30;;\r\n")
    time.sleep(0.5)

    print(f"\nAvanzando a velocidad {VELOCIDAD}...")
    enviar(ser, f"#speed:{VELOCIDAD};;\r\n")

    time.sleep(5)

    print("\nFrenando...")
    enviar(ser, "#speed:0;;\r\n")
    time.sleep(0.2)
    enviar(ser, "#kl:0;;\r\n")
    time.sleep(0.5)

    stop_event.set()

print("\nListo.")
