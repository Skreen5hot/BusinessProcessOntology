"""APQC PCF -> BFO 2020 / CCO transform toolchain.

Two-layer architecture per ADR-001:
  - catalog layer (deterministic, total)  -> catalog.py
  - reality layer (selective, LLM-built)  -> agent_runner.py / daemon.py
Validation: validate.py (Gates A-D).
"""

__version__ = "0.1.0"
