#!/usr/bin/env bash

set -euo pipefail

die() {
  echo -e "[ERRO]" | tee -a "logfile.txt"
}

check() {
  command -v cppcheck
  cppcheck --force .
  #cppcheck --force . | grep DEBUG
}

debug() {
  cppcheck --force . | rg DEBUG
}

check
debug
