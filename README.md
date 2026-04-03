# GenLayer Intelligent Contract — Execution Performance Benchmark

> How long does it actually take for different types of Intelligent Contracts to finalize on GenLayer?

This repo documents a performance benchmark measuring execution time across 5 contract categories on the GenLayer Studio testnet. All contracts, raw data, and methodology are included.

---

## Results Summary

| Contract Type | Run 1 | Run 2 | Run 3 | Average | vs Baseline |
|---|---|---|---|---|---|
| Pure Python (baseline) | 30s | 40s | 45s | **~38s** | — |
| Web only | 45s | 45s | 40s | **~43s** | +5s |
| LLM strict_eq | 40s | 48s | 45s | **~44s** | +6s |
| LLM prompt_comparative | 45s | 55s | 49s | **~50s** | +12s |
| Web + LLM combined | 60s | 65s | 60s | **~62s** | +24s |

---

## Test Environment

- **Network:** GenLayer Studio hosted testnet (`studio.genlayer.com`)
- **Chain ID:** 61999
- **Total validators:** 115 active
- **LLM models running simultaneously:** 8 different models across 2 providers

| Model | Provider | Validators |
|---|---|---|
| GPT-5.2 | openrouter | 12 |
| GPT-5-mini | openrouter | 5 |
| Claude Sonnet 4.5 | openrouter | 13 |
| Gemini 3 Flash Preview | openrouter | 15 |
| Nvidia Llama 3.1 Nemotron Ultra 253B | openrouter | 17 |
| Qwen3 235B | openrouter | 12 |
| DeepSeek V3.2 | openrouter + ionet | 26 |
| Llama 4 Maverick | openrouter + ionet | 14 |

---

## Contracts Tested

### 1. Pure Python (baseline)
**File:** `contracts/01_pure_python.py`

Basic computation with no external calls — sorts a list and stores the result. Used to isolate the consensus overhead from any LLM or web latency.

### 2. LLM with strict_eq
**File:** `contracts/02_llm_strict_eq.py`

Single LLM call for sentiment classification. Uses `gl.eq_principle.strict_eq` — all validators must return byte-identical JSON. Prompt is tightly constrained to three possible values.

### 3. LLM with prompt_comparative
**File:** `contracts/03_llm_prompt_comparative.py`

Open-ended text summarization. Uses `gl.eq_principle.prompt_comparative` — validators agree if outputs are semantically equivalent. Requires an additional LLM call per validator to evaluate equivalence.

### 4. Web access only
**File:** `contracts/04_web_only.py`

HTTP fetch with no LLM. Fetches live data from Coinbase API and stores response body length. Uses `strict_eq` since the numeric result should be identical across validators if fetched close in time.

### 5. Web + LLM combined
**File:** `contracts/05_web_llm_combined.py`

Fetches live crypto price from Coinbase API, then passes it to an LLM for a HIGH/MEDIUM/LOW assessment. Chains two non-deterministic operations in a single transaction.

---

## Key Findings

### 1. Consensus is the bottleneck, not computation
Even pure Python with trivial logic takes ~38 seconds. That's the consensus process — 115 validators independently executing and agreeing — not the code itself. Optimizing contract logic has minimal impact on user-perceived latency.

### 2. LLM calls add surprisingly little overhead
Adding a single LLM call with `strict_eq` only added ~6 seconds over baseline. LLM inference happens in parallel across validators and gets partially absorbed into the consensus window.

### 3. Web access and LLM strict_eq are roughly equivalent
Web-only (~43s) and LLM strict_eq (~44s) came in nearly identical. Both operations have similar latency profiles because the bottleneck is the same — waiting for all validators to complete independently.

### 4. prompt_comparative costs more than strict_eq
The ~6 second gap between `strict_eq` and `prompt_comparative` reflects the additional LLM call validators make to evaluate semantic equivalence. If your output can be constrained to a fixed schema, `strict_eq` is faster.

### 5. Chaining web + LLM compounds latency
Web + LLM combined (~62s) is more than the sum of web alone (+5s) and LLM alone (+6s) — suggesting compounding effects when two non-deterministic operations need to converge across 115 validators.

---

## Methodology

- Each contract was deployed once and executed 3 times
- Time measured manually from transaction submission to `FINALIZED` status
- All transactions used default validator selection (no custom configuration)
- Tests run on GenLayer Studio hosted environment in March 2026

Raw data: [`data/raw_results.csv`](data/raw_results.csv)
Environment details: [`data/environment.json`](data/environment.json)

---

## Recommendations for Developers

1. **Use `strict_eq` by default** — if output can be constrained to fixed JSON schema, saves ~6s vs `prompt_comparative`
2. **Avoid chaining web + LLM** — separate into two transactions if latency matters
3. **Design for the ~38s floor** — that's consensus overhead, no amount of code optimization gets below it
4. **Account for variance** — individual runs varied 5-15s within the same contract type

---

## Limitations

- 3 runs per contract is a small sample
- Results specific to Studio environment (115 validators, 8 models)
- Local setup or Testnet Bradbury may show different numbers
- Network conditions and validator load affect results

---

*Tested on GenLayer Studio testnet, March 2026. Part of the GenLayer community research initiative.*
