# BACKEND

To create local virtual environment run `env_config.sh` from `backend/` directory

```
source ./.venv/bin/activate
flask --app backend/main.py --debug run
```
OR 
```
python backend/main.py
```

For manual deploy run `gcloud run deploy`