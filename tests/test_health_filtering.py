import pytest

from load_balancer import LoadBalancer, RoundRobinStrategy, Request, NoHealthyServersAvailableError, Server, ServerPool
from load_balancer.servers.server import ServerState


def test_unhealthy_servers_filtering():

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, state=ServerState.UNHEALTHY),
        Server(id="s2", host="localhost", port=8002, state=ServerState.HEALTHY),
        Server(id="s3", host="localhost", port=8003, state=ServerState.UNHEALTHY),
        Server(id="s4", host="localhost", port=8004, state=ServerState.HEALTHY)
    ])

    lb = LoadBalancer(server_pool, RoundRobinStrategy())

    selected_servers = [lb.handle_request(Request()).id for _ in range(4)]

    assert selected_servers == ["s2", "s4", "s2", "s4"]


def test_no_healthy_servers_available():

    server_pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, state=ServerState.UNHEALTHY),
        Server(id="s2", host="localhost", port=8002, state=ServerState.UNHEALTHY),
        Server(id="s3", host="localhost", port=8003, state=ServerState.UNHEALTHY),
        Server(id="s4", host="localhost", port=8004, state=ServerState.UNHEALTHY)
    ])

    lb = LoadBalancer(server_pool, RoundRobinStrategy())

    with pytest.raises(NoHealthyServersAvailableError):
        lb.handle_request(Request())