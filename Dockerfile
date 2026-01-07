FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy dependency metadata first to leverage Docker layer caching
COPY pyproject.toml ./

# Install uv and project dependencies from pyproject.toml into the system environment
RUN pip install --upgrade pip \
	&& pip install uv \
	&& uv pip install . --system

# Now copy the rest of the application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
