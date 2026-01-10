socat -d -d pty,raw,echo=0,link=/tmp/ttyMedidor pty,raw,echo=0,link=/tmp/ttyHost
#&& python3 medidor_simulado.py && python3 sender.py
