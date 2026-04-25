#!/bin/bash
set -eou pipefail

# Check if pip is installed
if ! command -v pip &> /dev/null; then
  echo -e "Pip is not installed. Kindly install pip before proceeding.\n"
  exit 1
fi

# Upgrade pip
pip install --upgrade pip
pip install uv

# Sync uv packages
uv sync
    
# Make the secrets folders
if [ ! -d "./secrets" ]; then
  echo "Creating 'secrets' folder."
  mkdir -p secrets
  echo "your-api-key" > "./secrets/api_key.txt"
  echo "your-server-secret" > "./secrets/server_secret.txt"
fi

# Make self signed certificates
if [ ! -d "./certs" ]; then
  echo "Generating self-signed certificate"
  mkdir -p certs
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/local.key -out certs/local.crt \
    -subj "/CN=*.docker.localhost"
fi

# Generate password
read -n 1 -p "Would you like to generate the dashboard credentials? (y/n)" yn
case $yn in
  [Yy]* ) 

    while true 
    do
      echo
      read -e -s -p "Enter password: " pw
      read -e -s -p "Confirm password: " confirm_pw
    
      if [ -z "$pw" ]; then
        echo "Password cannot be empty. Try again."
        continue
      fi

      if [ "$pw" == "$confirm_pw" ]; then
        break
      fi

      echo -e "Password mismatch. Try again."
    done

    echo -e "Generating dashboard credentials...\n"
    htpasswd -nb admin $pw | sed -e 's/\$/\$\$/g'
    echo -e "Copy the password above and change the default password of the traefik dashboard."
    ;;

  [Nn]* )
    echo -e "Done."
    exit 0
    ;;

  * )
    echo -e "Done."
    exit 0
    ;;
esac
