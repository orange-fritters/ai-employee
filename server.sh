#!/bin/bash

# (1) server and venv

if [[ $PWD != *"server"* ]]; then
    cd server
fi

source venv/bin/activate

# (2) Parse environment variables and run uvicorn
while IFS="=" read -r key value; do
    # Removing double quotes from the key and value
    key=$(echo $key | tr -d '"')
    value=$(echo $value | tr -d '"')

    # Exporting the key-value pair as an environment variable
    export $key=$value
    echo "Exported: $key=$value"
done < <(jq -r 'to_entries[] | "\(.key)=\(.value)"' config.json)

# (3) Run uvicorn
uvicorn server:app --reload --host $(ip addr | grep 'inet ' | grep -v '127.0.0.1' | grep -v 'docker0' | awk '{print $2}' | cut -d'/' -f1) 