# Project Net Zero

A CLI tool that optimizes your Python code for lower CO2 emissions. Send your code to an optimization backend, get an optimized version back, and run it — without ever modifying your original file.

## Installation

```bash
pip install projectnetzero
```

Or install from source:

```bash
git clone https://github.com/your-org/project-net-zero-public-api.git
cd project-net-zero-public-api
pip install .
```

## Quick Start

```bash
projectnetzero run your_script.py
```

This will:

1. Read `your_script.py`
2. Send the source code to the optimization API
3. Receive the optimized version
4. Run the optimized code locally

Your original file is **never modified**.

## Configuration

### API URL

By default, the CLI connects to `https://web-production-4e0ee.up.railway.app`. No configuration needed.

To use a different API server:

```bash
# Using the --api-url flag
projectnetzero run your_script.py --api-url https://your-api.example.com

# Or using an environment variable
export PROJECTNETZERO_API_URL=https://your-api.example.com
projectnetzero run your_script.py
```

## CLI Reference

```
projectnetzero --version          # Show version
projectnetzero --help             # Show help
projectnetzero run <file>         # Optimize and run a Python file
projectnetzero run <file> --api-url <url>  # Use a custom API URL
```

---

## Building an Optimizer Backend

Want to build your own optimization backend that works with this CLI? Your API just needs to implement a single endpoint.

### API Specification

#### `POST /optimize`

Receives Python source code and returns an optimized version.

**Request:**

```json
{
  "source_code": "def hello():\n    x = 1\n    y = 2\n    print(x + y)\n\nhello()"
}
```

| Field         | Type   | Description                            |
| ------------- | ------ | -------------------------------------- |
| `source_code` | string | The raw Python source code to optimize |

**Response (200 OK):**

```json
{
  "optimized_code": "def hello():\n    print(3)\n\nhello()"
}
```

| Field            | Type   | Description                      |
| ---------------- | ------ | -------------------------------- |
| `optimized_code` | string | The optimized Python source code |

**Error Response (non-200):**

Return any non-200 status code with an error message in the response body. The CLI will display it to the user.

### Minimal Backend Example (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class OptimizeRequest(BaseModel):
    source_code: str


class OptimizeResponse(BaseModel):
    optimized_code: str


@app.post("/optimize")
def optimize(request: OptimizeRequest) -> OptimizeResponse:
    # Your optimization logic here
    optimized = your_optimizer(request.source_code)
    return OptimizeResponse(optimized_code=optimized)
```

Run it with:

```bash
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Minimal Backend Example (Flask)

```python
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.post("/optimize")
def optimize():
    data = request.get_json()
    source_code = data["source_code"]

    # Your optimization logic here
    optimized = your_optimizer(source_code)

    return jsonify({"optimized_code": optimized})
```

Run it with:

```bash
pip install flask
flask run --host 0.0.0.0 --port 8000
```

### Requirements for Your Backend

- Must accept `POST /optimize` with a JSON body containing `source_code`
- Must return JSON with `optimized_code`
- Must return status `200` on success
- The returned `optimized_code` must be valid, executable Python
- Timeout is set to 120 seconds — optimizations must complete within that window

## Requirements

- Python >= 3.10

## License

MIT
