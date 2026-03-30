#工具的注册表
from .amass import AmassRunner
from .dnsx import DnsxRunner
from .subfinder import SubfinderRunner
from .httpx import HttpxRunner


RUNNER_REGISTRY = {
    "amass": AmassRunner,
    "dnsx": DnsxRunner,
    "subfinder": SubfinderRunner,
    "httpx": HttpxRunner
}


def get_supported_runners():
    return sorted(RUNNER_REGISTRY.keys())


def build_runner(tool_name):
    runner_cls = RUNNER_REGISTRY.get(tool_name)
    if not runner_cls:
        raise ValueError(f"不支持的收集器: {tool_name}")
    return runner_cls()
