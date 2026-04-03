# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
# Benchmark Contract 2 — LLM with strict_eq
# Single LLM call. Validators must return byte-identical JSON.

from genlayer import *
import json

class BenchmarkLLMStrict(gl.Contract):
    last_result: str

    def __init__(self):
        self.last_result = ""

    @gl.public.write
    def classify(self, text: str) -> None:
        def run():
            result = gl.nondet.exec_prompt(
                f'Classify the sentiment of this text as POSITIVE, NEGATIVE, or NEUTRAL. '
                f'Text: "{text}". '
                f'Respond ONLY with valid JSON: {{"sentiment": "<POSITIVE|NEGATIVE|NEUTRAL>"}}',
                response_format="json"
            )
            return json.dumps(result, sort_keys=True)

        raw = gl.eq_principle.strict_eq(run)
        self.last_result = json.loads(raw)["sentiment"]

    @gl.public.view
    def get_result(self) -> str:
        return self.last_result
