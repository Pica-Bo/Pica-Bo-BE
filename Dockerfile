FROM python:3.11-slim
WORKDIR /usr/src/app
COPY pyproject.toml /usr/src/app/
RUN pip install --upgrade pip
RUN pip install uv
# Install runtime dependencies
RUN pip install --no-cache-dir fastapi uvicorn jinja2 beanie pymongo python-dotenv pyjwt pydantic passlib[bcrypt]
COPY . /usr/src/app
EXPOSE 8000
CMD ["uv", "run", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
