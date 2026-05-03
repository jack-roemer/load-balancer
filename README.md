# Adaptive Load Balancer

Adaptive Load Balancer is a Python project that simulates core load-balancing behavior behind modern distributed systems. It routes incoming requests across backend servers using pluggable algorithms, tracks basic runtime metrics, exposes a FastAPI control plane, and supports simple server state management.

## What the project does

This project provides a small but extensible load balancer framework with:

- multiple routing strategies:
  - round robin
  - least connections
  - weighted round robin
  - consistent hashing
- server pool management
- server states (`healthy`, `draining`, `unhealthy`)
- request metrics
- a FastAPI API for interacting with the load balancer
- automated tests covering the core behaviors

It is designed as a portfolio project that demonstrates clean architecture, testing, and systems-oriented design rather than trying to replace a production reverse proxy.

## Why the project is useful

This project is useful because it demonstrates several backend engineering concepts in one codebase:

- **Pluggable design**: routing algorithms are isolated behind a common strategy interface.
- **Health-aware routing**: only healthy servers are selected for new requests.
- **State management**: servers can be marked healthy, draining, or unhealthy.
- **Observability**: the load balancer tracks total requests, failed requests, and requests per server.
- **API-driven control**: the FastAPI layer makes it easy to inspect and modify the system at runtime.
- **Testability**: the project includes unit tests and API tests to validate current behavior.

### Current feature set

- Strategy-based request routing
- In-memory server registry and state transitions
- Metrics snapshots
- Demo script for local experimentation
- API endpoints for:
  - listing servers
  - retrieving a server by ID
  - creating and deleting servers
  - updating server state
  - handling a request
  - retrieving metrics
  - switching routing strategy

## Project structure

```text
src/
├── api.py
├── main.py
└── load_balancer/
    ├── algos/
    │   ├── consistent_hashing.py
    │   ├── least_connections.py
    │   ├── round_robin.py
    │   ├── routing_strategy.py
    │   └── weighted_round_robin.py
    ├── core/
    │   ├── load_balancer.py
    │   └── request.py
    ├── observability/
    │   └── metrics.py
    └── servers/
        ├── server.py
        └── server_pool.py

tests/
├── test_api.py
├── test_consistent_hashing.py
├── test_health_filtering.py
├── test_least_connections.py
├── test_metrics.py
├── test_round_robin.py
├── test_server_states.py
└── test_weighted_round_robin.py
```

## Architecture overview

### `Server`
Represents a backend server.

Key fields:
- `id`
- `host`
- `port`
- `weight`
- `state`
- `active_connections`
- `avg_response_time`

### `ServerPool`
Stores and manages backend servers.

Responsibilities:
- add/remove servers
- retrieve one or all servers
- filter routable servers
- update server state

### `RoutingStrategy`
Abstract strategy interface used by routing algorithms.

Current implementations:
- `RoundRobinStrategy`
- `LeastConnectionsStrategy`
- `WeightedRoundRobinStrategy`
- `ConsistentHashingStrategy`

### `LoadBalancer`
Core orchestrator that:
- obtains healthy servers from the pool
- delegates selection to the active strategy
- records metrics
- raises an error when no healthy servers are available

### `Metrics`
Tracks basic runtime counters:
- total requests
- failed requests
- requests per server
- healthy server count snapshot

### `FastAPI API`
Provides a simple control plane around the load balancer.

## How users can get started

### Requirements

- Python 3.11+
- `pip`

### Installation

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

### Run the test suite

From the project root:

```bash
PYTHONPATH=src python -m pytest -q
```

At the time of this update, the project test suite passes end to end.

### Run the local demo

```bash
PYTHONPATH=src python src/main.py
```

This runs small examples for:
- round robin
- least connections
- weighted round robin
- consistent hashing

### Start the FastAPI server

```bash
PYTHONPATH=src python -m uvicorn api:app --reload --app-dir src
```

Then open the interactive docs at:

```text
http://127.0.0.1:8000/docs
```

## Usage examples

### Example: route a request in Python

```python
from load_balancer import (
    LoadBalancer,
    Request,
    RoundRobinStrategy,
    Server,
    ServerPool,
)

pool = ServerPool([
    Server(id="s1", host="localhost", port=8001),
    Server(id="s2", host="localhost", port=8002),
])

lb = LoadBalancer(pool, RoundRobinStrategy())
selected = lb.handle_request(Request(client_id="user-1", path="/api/orders"))

print(selected.id)
print(selected.address)
```

### Example: create a server through the API

```bash
curl -X POST http://127.0.0.1:8000/servers \
  -H "Content-Type: application/json" \
  -d '{"id":"s3","host":"localhost","port":8003,"weight":2}'
```

### Example: mark a server as draining

```bash
curl -X PATCH http://127.0.0.1:8000/servers/s1/state \
  -H "Content-Type: application/json" \
  -d '{"state":"draining"}'
```

### Example: switch routing strategy

```bash
curl -X PATCH http://127.0.0.1:8000/strategy \
  -H "Content-Type: application/json" \
  -d '{"strategy":"least_connections"}'
```

### Example: inspect metrics

```bash
curl http://127.0.0.1:8000/metrics
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/servers` | List all servers |
| `GET` | `/servers/{server_id}` | Fetch one server |
| `POST` | `/servers` | Add a new server |
| `DELETE` | `/servers/{server_id}` | Remove a server |
| `PATCH` | `/servers/{server_id}/state` | Update server state |
| `POST` | `/handle_request` | Route a request |
| `GET` | `/metrics` | Return metrics snapshot |
| `PATCH` | `/strategy` | Change routing strategy |

## Testing

The repository includes:
- unit tests for each routing algorithm
- tests for health filtering and server states
- metrics tests
- FastAPI endpoint tests

Run everything with:

```bash
PYTHONPATH=src python -m pytest -q
```

## Current limitations

This is an educational and portfolio-oriented project. It currently uses:
- in-memory state only
- simulated request routing rather than proxying live upstream traffic
- no background health checker yet
- no persistence layer
- no authentication on the API

## Next development focus

The next major improvement is health and failure tracking, including:
- passive failure counting
- automatic transition to unhealthy state after repeated failures
- recovery behavior
- richer metrics around server health events

## License

TODO
