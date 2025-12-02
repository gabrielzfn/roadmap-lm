#!/usr/bin/env python3
import serial
import time

# Sender de comandos ABNT - 14522.

ser = serial.Serial("/tmp/ttyHost", 9600, timeout=2)

for i in range(5):
    ser.write(b"LEITURA\n")
    print("[SENDER] Comando LEITURA enviado")
    resposta = ser.readline().decode(errors="ignore").strip()
    print(f"[SENDER] Dados recebidos: {resposta}")
    time.sleep(2)
