#!/bin/bash

echo "Setting up environment..."
if ! $(python -c "import virtualenv" &> /dev/null); then
    echo "Installing virtualenv via pip (requires sudo password)..."
	sudo pip install virtualenv;
fi
echo "Running installation script generator..."
python install-script-gen.py;
if [ ! -f src/config.json ]; then
    echo "Running configuration generator..."
    python config-gen.py;
fi
echo "Finished!"
