#!/bin/bash

echo "Welcome to the SearchCLI Install Program!"
echo "Install? (y/n)"
read install

if [[ "$install" = "y" ]]; then
    echo "Installing..."
    
    # Use /usr/local/bin instead of /usr/bin
    mkdir -p /usr/local/bin/.searchcli
    mv searchcli.py /usr/local/bin/.searchcli/

    # Create wrapper script
    echo -e '#!/bin/bash\nexec python3 /usr/local/bin/.searchcli/searchcli.py "$@"' > /usr/local/bin/searchcli
    chmod +x /usr/local/bin/searchcli

    echo "Done!"
    exit 0
else
    echo "Exiting..."
    exit 0
fi           