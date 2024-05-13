# LBS Workshop

### Local environment

- Have python 3.9+ installed
- Install requirements `pip install -r requirements.txt`
- Have a `dev.env` file locally created with AWS connection strings:

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

### Run FastAPI

Simply execute in your terminal: `uvicorn main:app --reload`

To test your application, open your browser at `localhost:8000` (http://127.0.0.1 in Windows)