import pytest

from load_balancer import LoadBalancer, RoundRobinStrategy, Request, NoHealthyServersAvailableError, Server, ServerPool


def test_unhealthy_servers_filtering():

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, healthy=False),
        Server(id="s2", host="localhost", port=8002, healthy=True),
        Server(id="s3", host="localhost", port=8003, healthy=False),
        Server(id="s4", host="localhost", port=8004, healthy=True)
    ])

    lb = LoadBalancer(server_pool, RoundRobinStrategy())

    selected_servers = [lb.handle_request(Request()).id for _ in range(4)]

    assert selected_servers == ["s2", "s4", "s2", "s4"]


def test_no_healthy_servers_available():

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, healthy=False),
        Server(id="s2", host="localhost", port=8002, healthy=False),
        Server(id="s3", host="localhost", port=8003, healthy=False),
        Server(id="s4", host="localhost", port=8004, healthy=False)
    ])

    lb = LoadBalancer(server_pool, RoundRobinStrategy())

    with pytest.raises(NoHealthyServersAvailableError):
        lb.handle_request(Request())