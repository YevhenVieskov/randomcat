#!/bin/bash
PATH=$WORKSPACE/venv/bin:$HOME/.local/bin:$PATH
if [ ! -d "venv" ] then;
	pip3 install virtualenv --user
	virtualenv venv
fi
source venv/bin/activate
pip3 install --no-cache-dir -r ./requirements.txt
python3  ./test_flask_app.py"

