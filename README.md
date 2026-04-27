# Adaptive Load Balancer

A portfolio-focused Python load balancer framework that routes requests across backend servers using pluggable algorithms, health-aware filtering, and a modular architecture.

## Current MVP v1 Scope
- Pluggable routing strategy interface
- Backend server model and server pool
- Core load balancer orchestrator
- Round robin routing
- Least connections routing
- Basic healthy/unhealthy filtering
- Unit tests for routing behavior

## Current Repository Layout

```text
src/
  load_balancer/
    __init__.py
    algos/
      routing_strategy.py
      round_robin.py
      least_connections.py
    core/
      load_balancer.py
      request.py
    servers/
      server.py
      server_pool.py
tests/
  test_round_robin.py
  test_least_connections.py
  test_health_filtering.py
```

## Architecture

### Server
Represents a backend target.

Fields today:
- `id`
- `host`
- `port`
- `weight`
- `healthy`
- `active_connections`
- `avg_response_time`

### ServerPool
Responsible for:
- adding and removing servers
- retrieving all servers
- retrieving healthy servers only
- updating server health

### Request
A small request model used by routing algorithms.

Fields:
- `client_id`
- `path`
- `headers`

### RoutingStrategy
Abstract base class for pluggable server-selection strategies.

### LoadBalancer
Coordinates request handling by:
1. asking the pool for healthy servers
2. delegating selection to the active routing strategy
3. returning the selected server

## MVP v1 Plan

### Step 1: Foundation refactor
- Keep strategy-specific state inside each strategy class
- Keep orchestration inside `LoadBalancer`
- Keep server state in `Server`
- Keep server collection logic in `ServerPool`

### Step 2: Stabilize the current code
- fix argument ordering bug in `LoadBalancer.handle_request`
- clean up imports in tests
- align the least-connections test with the implemented behavior
- add packaging so tests run without manual path setup

### Step 3: Expand routing support
- add weighted round robin
- add consistent hashing
- optionally add least response time

### Step 4: Improve usability
- add a small demo in `src/main.py`
- add config support
- add benchmark/simulation scripts

### Step 5: Make it portfolio-ready
- add API endpoints with FastAPI
- add runtime metrics and health views
- add benchmark results and diagrams to the repo

## How to Run Tests

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests from the project root:

```bash
PYTHONPATH=src python -m pytest -q
```

## Recommended Next Steps
1. Fix the current bugs so the MVP baseline is stable.
2. Add weighted round robin as the next strategy.
3. Add consistent hashing for sticky routing.
4. Package the project cleanly with a `pyproject.toml`.
5. Add a runnable demo and benchmark script.
