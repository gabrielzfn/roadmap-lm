#!/usr/bin/env python3.11

from plyer import notification
import time
from datetime import datetime


# Função para notificar o horário do
def notificar_ponto():
    notification.notify(title=title, message=message, timeout=duration)


def marcarPonto():
    # Horas inicio
    hi = int(input("Digite a hora que tu bateu o ponto: "))
    mi = int(input("Digite os minutos: "))

    # Horas final
    hf = int(input("Digite a hora final: "))
    mf = int(input("Digite os minutos da hora final: "))
    # Cálculo das horas trabalhadas no dia
    hora_inicio = datetime(2025, 9, 16, hi, mi)
    hora_fim = datetime(2025, 9, 16, hf, mf)

    diferenca = hora_fim - hora_inicio

    total_segundos = diferenca.total_seconds()
    horas = int(total_segundos // 3600) - 1
    minutos = int(total_segundos % 3600) // 60
    segundos = int(total_segundos % 60)

    print("\f")
    print("\n")
    print(diferenca)

    if horas >= 8 and minutos >= 48:
        print("\f" + "Vaza pra casa rapaiz!")
        print(f"Horas de hoje = {horas}h {minutos}m {segundos}s")
    else:
        print(f"Horas de hoje = {horas}h {minutos}m {segundos}s")


if __name__ == "__main__":
    marcarPonto()
