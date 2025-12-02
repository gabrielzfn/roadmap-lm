#!/usr/bin/env python3
import serial
import time
import random

ser = serial.Serial('/tmp/ttyMedidor', 9600, timeout=1)
print("[MEDIDOR] Aguardando comandos...")

while True:
    linha = ser.readline().decode(errors='ignore').strip()
    if not linha:
        continue
    print(f"[MEDIDOR] Recebido: {linha}")

    # Respostas fictícias
    if "LEITURA" in linha.upper():
        temp = round(random.uniform(20.0, 35.0), 2)
        resposta = f"{temp} C;OK\n"
        ser.write(resposta.encode())
        print(f"[MEDIDOR] Enviado: {resposta.strip()}")
