from load_balancer import *


def demo_round_robin() -> None:

    print("\nRound Robin Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
        Server(id="s3", host="localhost", port=8003),
        Server(id="s4", host="localhost", port=8004)
    ])

    lb = LoadBalancer(pool, RoundRobinStrategy())

    for i in range(6):
        server = lb.handle_request(Request(path=f"/rr/{i}"))
        print(f"Request {i} -> {server.id}")


def demo_least_connections() -> None:

    print("\nLeast Connections Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, active_connections=5),
        Server(id="s2", host="localhost", port=8002, active_connections=2),
        Server(id="s3", host="localhost", port=8003, active_connections=7),
        Server(id="s4", host="localhost", port=8004, active_connections=3)
    ])

    lb = LoadBalancer(pool, LeastConnectionsStrategy())

    server = lb.handle_request(Request(path="/least"))
    print(f"Selected server -> {server.id}")


def demo_weighted_round_robin() -> None:

    print("\nWeighted Round Robin Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, weight=1),
        Server(id="s2", host="localhost", port=8002, weight=2),
        Server(id="s3", host="localhost", port=8003, weight=3),
        Server(id="s4", host="localhost", port=8004, weight=4)
    ])

    lb = LoadBalancer(pool, WeightedRoundRobinStrategy())

    for i in range(10):
        server = lb.handle_request(Request(path=f"/wrr/{i}"))
        print(f"Request {i} -> {server.id}")


def demo_consistent_hash() -> None:

    print("\nConsistent Hash Demo")

    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
        Server(id="s3", host="localhost", port=8003),
        Server(id="s4", host="localhost", port=8004),
    ])

    lb = LoadBalancer(pool, ConsistentHashingStrategy())

    users = ["alice", "bob", "alice", "charlie", "bob"]

    for user in users:
        server = lb.handle_request(Request(client_id=user, path="/profile"))
        print(f"Client {user} -> {server.id}")


if __name__ == "__main__":
    demo_round_robin()
    demo_least_connections()
    demo_weighted_round_robin()
    demo_consistent_hash()