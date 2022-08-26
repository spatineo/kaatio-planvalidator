import uvicorn

from kaatio_plan_validator.main import app  # noqa

if __name__ == "__main__":
    uvicorn.run("kaatio_plan_validator", host="0.0.0.0", port=8000, reload=True)
