from load_balancer import Server, ServerPool, LoadBalancer, WeightedRoundRobinStrategy, Request


def test_weighted_round_robin_strategy():   

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, weight=1),
        Server(id="s2", host="localhost", port=8002, weight=2),
        Server(id="s3", host="localhost", port=8003, weight=3),
        Server(id="s4", host="localhost", port=8004, weight=4) 
    ])

    lb = LoadBalancer(server_pool, WeightedRoundRobinStrategy())

    selected = [lb.handle_request(Request()).id for _ in range(10)]

    assert selected == ["s1", "s2", "s2", "s3", "s3", "s3", "s4", "s4", "s4", "s4"]