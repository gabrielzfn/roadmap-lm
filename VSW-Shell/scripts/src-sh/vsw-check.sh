#!/usr/bin/env bash

set -euo pipefail

die() {
  echo -e "[ERRO]" | tee -a "logfile.txt"
}

check() {
  #command -v cppcheck
  cppcheck --force . 
  #| rg DEBUG
  #cppcheck --force . | grep DEBUG
}

check
