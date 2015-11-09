#!/bin/sh
rm -rf ./Project-UNCH
git clone https://github.com/EdricY/Project-UNCH.git
cd ./Project-UNCH/src
echo "Starting Project-UNCH!"
python main.py
echo "Project-UNCH has quit."
cd ../
