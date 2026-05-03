# Design Notes

## Design goals

The project is built around four goals:

1. keep the core load balancer easy to reason about
2. isolate routing algorithms behind a common interface
3. model backend state explicitly rather than hiding it in routing logic
4. keep the code small enough to test and extend quickly

## Current design

### Core domain model

#### `Server`
`Server` models one backend target. It stores identity, address information, weight, runtime connection count, and routing state.

Current state model:
- `healthy`: routable
- `draining`: present in the pool but not eligible for new traffic
- `unhealthy`: excluded from routing

This state model is intentionally simple but mirrors real operational concepts used in load balancers.

#### `ServerPool`
`ServerPool` owns the server collection and acts as the single place where servers are added, removed, retrieved, and filtered.

Design choice:
- the pool returns a concrete list from `get_servers()` instead of a live dictionary view so callers receive a stable snapshot.

#### `Request`
`Request` is intentionally lightweight. It carries only the information routing strategies currently need:
- `client_id`
- `path`
- `headers`

This keeps the core decoupled from any specific web framework.

### Routing architecture

#### `RoutingStrategy`
The routing strategy abstraction keeps algorithm-specific logic out of `LoadBalancer`.

Benefits:
- strategies can be added without rewriting the load balancer
- algorithm state stays local to the algorithm implementation
- each strategy is easier to test independently

#### Implemented strategies

- **Round robin**: simple fair rotation across healthy servers
- **Least connections**: prefers the server with the smallest active connection count
- **Weighted round robin**: biases routing toward higher-weight servers
- **Consistent hashing**: maps similar requests to the same backend for sticky routing behavior

### Load balancer orchestration

`LoadBalancer` does only a small set of jobs:
- fetch the current healthy servers from the pool
- fail fast when none are available
- delegate server selection to the active strategy
- record metrics about successes and failures

This narrow responsibility is intentional. It keeps orchestration stable while allowing strategies, server state logic, and observability to evolve independently.

## Observability design

`Metrics` currently captures a compact snapshot of runtime behavior:
- total routed requests
- failed requests
- requests per server
- healthy server count at snapshot time

This is enough for MVP observability without overcomplicating the system.

The next logical extension is to track:
- per-server failure counts
- state transition counts
- last failure timestamps
- request latency metrics

## API design

The FastAPI layer is a thin control plane over the core library.

Current goals:
- inspect current state
- mutate server membership and server state
- submit simulated requests
- change routing strategy at runtime
- inspect metrics

Design choice:
- request and response validation uses Pydantic models because FastAPI integrates with them for validation and docs generation.

### Current API limitation

The app currently keeps runtime state in memory. That is fine for local testing and portfolio demos, but it means:
- state resets when the process restarts
- multiple workers would not share the same pool or metrics
- tests must be careful about shared mutable state unless the app is re-created per test

A future refinement would move the runtime objects onto `app.state` or dependency injection helpers for cleaner lifecycle management.

## Testing strategy

The current test suite is intentionally layered:

- algorithm tests validate routing behavior
- server-state tests validate routing eligibility
- metrics tests validate observability behavior
- API tests validate the control plane interface

This gives good coverage without needing complex infrastructure.

## Key tradeoffs

### Why not build a real reverse proxy?
That would add networking, concurrency, socket management, upstream retries, and significantly more operational complexity. The current project focuses on decision-making and control-plane behavior instead.

### Why keep fields public on `Server`?
For this Python project, a dataclass with small helper methods is clearer than a Java-style getter/setter design. Explicit methods are used only where they add meaning or validation.

### Why return lists from pool methods?
Returning lists creates predictable snapshots and simpler test behavior.

## Recommended next step

The next feature should be health and failure tracking.

A good implementation path is:

1. add passive failure counters per server
2. define a failure threshold
3. mark a server unhealthy after repeated failures
4. add recovery/reset behavior
5. expose failure information through metrics and the API

This will make the project feel much closer to a real load balancer while preserving the current clean architecture.
