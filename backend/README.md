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
OR (GCP style)
```
gunicorn --bind="127.0.0.1:5000" --workers 1 --threads 8 --timeout 0 main:app
```

For manual deploy run `gcloud run deploy`

Known error `AttributeError: 'Response' object has no attribute 'status_code'` is from gunicorn when there are sudden disconnects. It doesn't impact performance and is just kinda weird as it switches from websockets to long polling