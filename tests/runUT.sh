#!/bin/bash
PATH=$WORKSPACE/testenv/bin:$HOME/.local/bin:$PATH
if [ ! -d "testenv" ]; then
  pip3 install --user virtualenv
  python3 -m venv testenv
fi

source testenv/bin/activate
pip3 install --no-cache-dir -r ./requirements.txt
python3  ./test_flask_app.py
deactivate
exit