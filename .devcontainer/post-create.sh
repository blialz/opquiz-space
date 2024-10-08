#!/bin/bash

set -euo pipefail
set -x

apt-get update -y
apt-get install -y sqlite3

pip install --user -r requirements.txt
