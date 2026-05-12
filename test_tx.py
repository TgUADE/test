import serial
import serial.tools.list_ports
import time

BAUDRATE = 115200

def encontrar_puerto():
    for p in serial.tools.list_ports.comports():
        if p.vid == 0x0483:
            return p.device
    return None

puerto = encontrar_puerto()
print(f"Conectando a {puerto}...")

with serial.Serial(puerto, BAUDRATE, timeout=5) as ser:
    time.sleep(0.5)
    ser.reset_input_buffer()

    # pide los limites del servo - deberia responder sin necesitar KL30
    print("Enviando steerLimits...")
    ser.write(b"#steerLimits:0;;\r\n")

    print("Esperando 5 segundos cualquier dato del STM32...")
    inicio = time.time()
    recibido = b""
    while time.time() - inicio < 5:
        if ser.in_waiting:
            recibido += ser.read(ser.in_waiting)
            print(f"  DATOS: {recibido}")
        time.sleep(0.05)

    if not recibido:
        print("\nNada recibido - el TX del STM32 no llega a la PC.")
        print("Posible causa: puente SB14 abierto en la placa Nucleo.")
    else:
        print("\nOK - la placa SI transmite.")
