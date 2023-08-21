# Dev Environment

This is SETUP instruction for AI-employee project.
**Recomemnd following line by line**


## React

```sh
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
<!-- ⬆️ install nvm if not installed -->

nvm install 14.21.3
nvm use 14.21.3
<!-- ⬆️ determine the node version to use -->

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
<!-- ⬆️ add nvm to bash profile -->
<!-- If no bash, sorry, search on google plz -->

npm install -g npm@6.14.8
<!-- ⬆️ install npm -->

git clone https://github.com/orange-fritters/ai-employee path/to/clone
git checkout compact-version
<!-- ⬆️ Use compact version -->

cd path/to/clone/frontend
npm install
<!-- ⬆️ install dependencies -->

npm run build
<!-- ⬆️ build react app -->
```
## Python

```sh
if [[ $PWD != *"server"* ]]; then
    cd path/to/clone/server
fi
<!-- ⬆️ Go inside server folder  -->

python3.8 --version
<!-- ⬆️ This should return: `Python 3.8.10``  -->
<!-- If not, install python 3.8.10 -->

python3 -m venv venv
<!-- Create virtual environment named venv -->

source venv/bin/activate

pip install -r requirements.txt
<!-- ⬆️ install dependencies -->

echo '{"OPENAI_API_KEY": "your-api-key"}' > config.json
<!-- ⬆️ create config.json file with your api key -->
<!-- config.json should be located in server folder EX. server/config.json -->
<!-- Code provide environment variable for python to use openai -->
<!-- EX. `export OPENAI_API_KEY="my_api_key"` -->

bash server.sh
<!-- ⬆️ run server, if Ubuntu, sh file automatically detects IP address and uvicorn -->

<!-- If not Ubuntu, run uvicorn manually -->
uvicorn server:app --reload --host your.ip.address --port port_you_want 
```

## Modifying code

0. Complete the setup
1. Modify react code and `npm run build` inside frontend folder
2. Modify python code and `bash server.sh || uvicorn ...` inside server folder
    - Now you can access the server with the browser
    - Uvicorn inform you the address to access
3. Repeat 1 and 2 until you are satisfied with the result


## [Appendix] w/o comment version
```sh
<!-- frontend -->
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

nvm install 14.21.3
nvm use 14.21.3

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

npm install -g npm@6.14.8

git clone https://github.com/orange-fritters/ai-employee path/to/clone
git checkout compact-version

cd path/to/clone/frontend
npm install

npm run build


<!-- server -->

if [[ $PWD != *"server"* ]]; then
    cd path/to/clone/server
fi

python3.8 --version
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

echo '{"OPENAI_API_KEY": "your-api-key"}' > config.json || export OPENAI_API_KEY="my_api_key"

bash server.sh || uvicorn server:app --reload --host your.ip.address --port port_you_want 

```

