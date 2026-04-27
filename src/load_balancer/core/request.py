from dataclasses import dataclass, field


@dataclass
class Request:

    client_id: str | None = None
    path: str = "/"
    headers: dict[str, str] = field(default_factory=dict)