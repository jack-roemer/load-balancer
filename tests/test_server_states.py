from load_balancer import (
    LoadBalancer,
    NoHealthyServersAvailableError,
    Request,
    RoundRobinStrategy,
    Server,
    ServerPool,
    ServerState,
)


def test_draining_servers_are_not_routable():
    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, state=ServerState.DRAINING),
        Server(id="s2", host="localhost", port=8002, state=ServerState.HEALTHY),
    ])

    lb = LoadBalancer(pool, RoundRobinStrategy())
    selected = lb.handle_request(Request())

    assert selected.id == "s2"


def test_unhealthy_servers_are_not_routable():
    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, state=ServerState.UNHEALTHY),
        Server(id="s2", host="localhost", port=8002, state=ServerState.HEALTHY),
    ])

    lb = LoadBalancer(pool, RoundRobinStrategy())
    selected = lb.handle_request(Request())

    assert selected.id == "s2"


def test_no_routable_servers_raises_error():
    pool = ServerPool([
        Server(id="s1", host="localhost", port=8001, state=ServerState.DRAINING),
        Server(id="s2", host="localhost", port=8002, state=ServerState.UNHEALTHY),
    ])

    lb = LoadBalancer(pool, RoundRobinStrategy())

    try:
        lb.handle_request(Request())
        assert False, "Expected NoHealthyServersAvailableError"
    except NoHealthyServersAvailableError:
        assert True