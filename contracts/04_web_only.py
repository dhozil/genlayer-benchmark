# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# Benchmark Contract 4 — Web access only (no LLM)
# Fetches live data from the web. Uses strict_eq on response body length.

from genlayer import *

class BenchmarkWebOnly(gl.Contract):
    last_result: str

    def __init__(self):
        self.last_result = ""

    @gl.public.write
    def fetch(self, url: str) -> None:
        def run():
            data = gl.nondet.web.get(url)
            return str(len(data.body))

        self.last_result = gl.eq_principle.strict_eq(run)

    @gl.public.view
    def get_result(self) -> str:
        return self.last_result
