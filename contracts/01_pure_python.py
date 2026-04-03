# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# Benchmark Contract 1 — Pure Python (baseline)
# No LLM calls, no web access. Used to measure consensus overhead alone.

from genlayer import *

class BenchmarkBaseline(gl.Contract):
    counter: u256
    last_result: str

    def __init__(self):
        self.counter = u256(0)
        self.last_result = ""

    @gl.public.write
    def compute(self, n: u256) -> None:
        # Simple computation: sort a list and join as string
        data = [int(n) - i for i in range(10)]
        data.sort()
        self.last_result = ",".join(str(x) for x in data)
        self.counter += u256(1)

    @gl.public.view
    def get_result(self) -> str:
        return self.last_result

    @gl.public.view
    def get_counter(self) -> u256:
        return self.counter
