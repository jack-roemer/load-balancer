# Design Notes

## Project Description
A modular Python load balancer framework that routes requests using pluggable algorithms, health-aware filtering, and scalability-oriented design.

## MVP v1 Goals
- create a clean separation between orchestration, routing logic, and backend state
- support multiple routing strategies without changing the core load balancer
- filter unhealthy servers automatically before routing
- keep the code small, testable, and easy to extend

## Current Components

### `Server`
Represents one backend server.

Current responsibilities:
- store endpoint identity
- track health state
- track active connections
- expose a computed network address

### `ServerPool`
Maintains the collection of servers and provides filtered views.

Current responsibilities:
- add/remove servers
- retrieve servers by id
- return healthy servers only
- update server health

### `RoutingStrategy`
An abstract interface for server-selection algorithms.

Current implementations:
- `RoundRobinStrategy`
- `LeastConnectionsStrategy`

### `LoadBalancer`
Coordinates request handling and delegates server selection.

## Review Findings

### Good choices
- clear separation between strategies, core logic, and server storage
- `RoutingStrategy` abstraction is the right direction
- `ServerPool` already provides healthy-server filtering
- test files show good intent around behavior-driven development

## Recommended Build Sequence
1. stabilize the current MVP foundation
2. add weighted round robin
3. add consistent hashing
4. add a demo entry point
5. add packaging and CI
6. add observability and an API layer

## Testing Notes
Run tests with the source directory on the Python path:

```bash
PYTHONPATH=src python -m pytest -q
```

Once packaging is added, this can become a simpler `pytest` invocation.
