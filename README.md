# BATTLESHIP

## Frontend Start

Create generic VueJS project
`npm init vue@latest`

Add Quasar https://quasar.dev/start/vite-plugin
```
npm install quasar @quasar/extras
npm install -D @quasar/vite-plugin sass@1.32.12
```

Setting up from repo
```
npm install
npm run lint
npm run dev
```

### IDEAS
* Create a websocket object in the pina store and use that to send and receive events so each vue component
doesn't have to initialize a websocket client

* Game state will be entirely managed in Pina store

## BACKEND

To create local virtual environment run `env_config.sh` from `backend/` directory

```
source ./.venv/bin/activate
flask --app backend/app.py --debug run
```
OR 
```
python backend/app.py
```