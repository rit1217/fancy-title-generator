import uvicorn

uvicorn.run("api.api:app", host="0.0.0.0", port=3100, log_level="info", reload=True)