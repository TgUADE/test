import serial
import time

PUERTO = "/dev/ttyUSB0"
BAUDRATES = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

for baud in BAUDRATES:
    try:
        with serial.Serial(PUERTO, baud, timeout=1) as ser:
            ser.reset_input_buffer()
            time.sleep(0.3)
            ser.write(b"#kl:30;;\r\n")
            time.sleep(0.5)
            data = ser.read(100)
            texto = data.decode("ascii", errors="replace").strip()
            print(f"{baud:>7} baud -> {repr(texto[:60])}")
    except Exception as e:
        print(f"{baud:>7} baud -> ERROR: {e}")
