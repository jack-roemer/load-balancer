from load_balancer import Server, ServerPool, LoadBalancer, ConsistentHashingStrategy, Request


def test_same_client_id_routes_to_same_server():

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
        Server(id="s3", host="localhost", port=8003),
        Server(id="s4", host="localhost", port=8004)
    ])

    lb = LoadBalancer(server_pool, ConsistentHashingStrategy())

    request = Request(client_id="user-123")

    results = [lb.handle_request(request).id for _ in range(4)]

    assert len(set(results)) == 1


def test_different_clients_are_distributed():
    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
        Server(id="s3", host="localhost", port=8003),
        Server(id="s4", host="localhost", port=8004)
    ])

    lb = LoadBalancer(server_pool, ConsistentHashingStrategy())

    client_ids = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    results = [lb.handle_request(Request(client_id=client_id)).id for client_id in client_ids]

    assert len(set(results)) >= 2