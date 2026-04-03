# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# Benchmark Contract 3 — LLM with prompt_comparative
# Validators agree if outputs are semantically equivalent (not byte-identical).
# Requires an additional LLM call per validator to compare outputs.

from genlayer import *

class BenchmarkLLMComparative(gl.Contract):
    last_result: str

    def __init__(self):
        self.last_result = ""

    @gl.public.write
    def summarize(self, text: str) -> None:
        def run():
            result = gl.nondet.exec_prompt(
                'Summarize this in one sentence: ' + text
            )
            return str(result)

        self.last_result = gl.eq_principle.prompt_comparative(
            run,
            principle="The summaries are equivalent if they convey the same main idea."
        )

    @gl.public.view
    def get_result(self) -> str:
        return self.last_result
