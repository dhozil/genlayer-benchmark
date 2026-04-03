# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# Benchmark Contract 5 — Web access + LLM combined
# Fetches live price data then passes it to an LLM for analysis.
# Most complex pattern — chains two non-deterministic operations.

from genlayer import *
import json

class BenchmarkWebLLM(gl.Contract):
    last_result: str

    def __init__(self):
        self.last_result = ""

    @gl.public.write
    def analyze(self, ticker: str) -> None:
        def run():
            data = gl.nondet.web.get(
                'https://api.coinbase.com/v2/prices/' + ticker + '-USD/spot'
            )
            price = json.loads(data.body)['data']['amount']
            result = gl.nondet.exec_prompt(
                'The price of ' + ticker + ' is $' + str(price) +
                '. Reply with only one word: HIGH, MEDIUM, or LOW.'
            )
            return str(result).strip().upper()

        self.last_result = gl.eq_principle.strict_eq(run)

    @gl.public.view
    def get_result(self) -> str:
        return self.last_result
