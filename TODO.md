# TODO — Stock Analysis Engine

## 🧩 Missing Features

- [ ] Add new analysis models (momentum, mean reversion, ML-based)
- [ ] Enable hybrid models using combined signal weighting
- [ ] Support windowed multi-frame analysis (e.g., 5m + 1h + 1d)
- [ ] Dynamic rule-based output routing (e.g., signal only on threshold)

## 🛠️ Infrastructure Enhancements

- [ ] Retry logic in queue and output handlers
- [ ] Full output schema validation using Pydantic
- [ ] Prometheus metrics integration (processing latency, error rate)
- [ ] Output to InfluxDB/PostgreSQL with async support (future)

## 📈 Monitoring & Logging

- [ ] Use JSON logs with field-level detail
- [ ] Add structured error tracking for processor exceptions
- [ ] Implement message trace ID propagation

## ✅ Security & Compliance

- [ ] Bandit + Safety CI enforcement
- [ ] Cosign image signing & SBOM
- [ ] Add REUSE headers & license validation
- [ ] Add Semgrep rules for static analysis

## 🧪 Testing & CI

- [ ] Full test coverage of processor modules
- [ ] Test queue parsing edge cases
- [ ] Enforce pre-commit consistency with CI

## 🧹 Code Hygiene

- [ ] Remove unused imports and legacy code
- [ ] Verify typing coverage (`pyright`, `mypy`)
- [ ] Regenerate missing docstrings with `pyment`

## 🪄 Optional Enhancements

- [ ] Add CLI runner for local batch analysis
- [ ] Stream results to WebSocket or dashboard frontend
