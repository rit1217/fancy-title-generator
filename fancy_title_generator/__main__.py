import uvicorn

uvicorn.run("fancy_title_generator.api:app", host="0.0.0.0", port=3100, log_level="info")