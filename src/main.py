from load_balancer import *


def demo_round_robin() -> None:

    print("\nRound Robin Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
        Server(id="s3", host="localhost", port=8003),
        Server(id="s4", host="localhost", port=8004)
    ])

    metrics = Metrics()
    
    lb = LoadBalancer(pool, RoundRobinStrategy(), metrics=metrics)

    for i in range(6):
        server = lb.handle_request(Request(path=f"/rr/{i}"))
        print(f"Request {i} -> {server.id}")

    print("metrics snapshot:", lb.get_metrics())


def demo_least_connections() -> None:

    print("\nLeast Connections Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, active_connections=5),
        Server(id="s2", host="localhost", port=8002, active_connections=2),
        Server(id="s3", host="localhost", port=8003, active_connections=7),
        Server(id="s4", host="localhost", port=8004, active_connections=3)
    ])

    metrics = Metrics()
    lb = LoadBalancer(pool, LeastConnectionsStrategy(), metrics=metrics)

    server = lb.handle_request(Request(path="/least"))
    print(f"Selected server -> {server.id}")
    print("metrics snapshot:", lb.get_metrics())


def demo_weighted_round_robin() -> None:

    print("\nWeighted Round Robin Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, weight=1),
        Server(id="s2", host="localhost", port=8002, weight=2),
        Server(id="s3", host="localhost", port=8003, weight=3),
        Server(id="s4", host="localhost", port=8004, weight=4)
    ])

    metrics = Metrics()
    lb = LoadBalancer(pool, WeightedRoundRobinStrategy(), metrics=metrics)

    for i in range(10):
        server = lb.handle_request(Request(path=f"/wrr/{i}"))
        print(f"Request {i} -> {server.id}")
    print("metrics snapshot:", lb.get_metrics())


def demo_consistent_hash() -> None:

    print("\nConsistent Hash Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
        Server(id="s3", host="localhost", port=8003),
        Server(id="s4", host="localhost", port=8004),
    ])

    metrics = Metrics()
    lb = LoadBalancer(pool, ConsistentHashingStrategy(), metrics=metrics)

    users = ["alice", "bob", "alice", "charlie", "bob"]

    for user in users:
        server = lb.handle_request(Request(client_id=user, path="/profile"))
        print(f"Client {user} -> {server.id}")
    print("metrics snapshot:", lb.get_metrics())


if __name__ == "__main__":
    demo_round_robin()
    demo_least_connections()
    demo_weighted_round_robin()
    demo_consistent_hash()