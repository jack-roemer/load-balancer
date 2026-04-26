from load_balancer import Server, ServerPool, LoadBalancer, RoundRobinStrategy, Request


def test_round_robin_strategy():

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001),
        Server(id="s2", host="localhost", port=8002),
        Server(id="s3", host="localhost", port=8003),
        Server(id="s4", host="localhost", port=8004)
    ])

    lb = LoadBalancer(server_pool, RoundRobinStrategy())

    selected_servers = [lb.handle_request(Request()).id for _ in range(8)]

    assert selected_servers == ["s1", "s2", "s3", "s4", "s1", "s2", "s3", "s4"]