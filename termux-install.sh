#!/bin/bash

TERMUX_INSTALLATION_DIR=/data/data/com.termux/files/usr/bin/.searchcli

echo "Do you want to install SearchCLI for Termux (beta)? (y/n)"
read answer
if [[ $answer = "y"]]; then
    echo "Installing..."
    pkg install python3 lynx -y
    pip install requests beautifulsoup4 --break-system-packages
    mv main.py $TERMUX_INSTALLATION_DIR/main.py
echo -e '#!/bin/bash\nexec python3 $TERMUX_INSTALLATION_DIR/main.py "$@"' > $TERMUX_INSTALLATION_DIR/searchcli
chmod +x $TERMUX_INSTALLATION_DIR/searchcli
else
    echo "Exiting..."
    exit 0
fi
