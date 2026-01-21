#!/usr/bin/env bash
# Compile com restrições (exemplo para CTF):
gcc -Wall -Wextra -O2 -fstack-protector -o out *.c

# Use capabilities para comandos que precisam de privilégios:
sudo setcap cap_net_raw+ep /usr/bin/nmap

./out
