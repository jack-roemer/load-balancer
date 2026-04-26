from load_balancer import Server, ServerPool, LoadBalancer, LeastConnectionsStrategy, Request


def test_least_connections_strategy():

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, active_connections=5),
        Server(id="s2", host="localhost", port=8002, active_connections=3),
        Server(id="s3", host="localhost", port=8003, active_connections=7),
        Server(id="s4", host="localhost", port=8004, active_connections=2)
    ])

    lb = LoadBalancer(server_pool, LeastConnectionsStrategy())

    selected_server = lb.handle_request(Request())

    assert selected_server.id == "s4"
