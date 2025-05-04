# 📌 Project TODO: Stock Poller Enhancements

This TODO list outlines the remaining work required to bring the stock-\* poller repositories to MVP and production quality.

---

## ✅ Core Functionality

- [ ] Ensure poller correctly loads:
  - [ ] Symbols from config
  - [ ] API key from Vault/env
  - [ ] Correct poller type is selected
- [ ] Add health check endpoints or CLI flags
- [ ] Implement dry-run/test mode for poller output verification

---

## 🔐 Vault Integration

- [ ] Automatically initialize Vault for each poller (dev/staging)
- [ ] Create Vault policies per poller type
- [ ] Automate token injection via GitHub Actions/CI
- [ ] Add fallback to environment variables with logging

---

## 📨 Messaging (RabbitMQ / SQS)

- [ ] Unify queue interface (RabbitMQ/SQS abstraction)
- [ ] Graceful retry/backoff strategies
- [ ] Improve test coverage for queue failures
- [ ] Add queue health checks

---

## ⚙️ Configuration

- [ ] Standardize all configuration via `app/config.py`
- [ ] Ensure every poller can:
  - [ ] Use Vault
  - [ ] Use `.env` overrides (optional)
  - [ ] Log missing config values

---

## 🧪 Testing

- [ ] Increase test coverage to >90%
- [ ] Mock APIs cleanly (e.g., Finnhub, AlphaVantage)
- [ ] Add test cases for:
  - [ ] Rate limiting
  - [ ] Timeout behavior
  - [ ] Data validation failures
- [ ] Add integration test runner (`tests/integration/`)

---

## 💬 Slack & Alerting Integration

- [ ] Add support for sending poller status or failures to Slack
- [ ] Allow toggling Slack alerts with an env flag (`ENABLE_SLACK_ALERTS`)
- [ ] Send daily summary or heartbeat if no errors

---

## 🧠 Caching / Optimization

- [ ] Implement symbol result caching to avoid duplicate API calls
- [ ] Consider in-memory cache (e.g. `functools.lru_cache`) for:
  - [ ] Rate limit enforcement
  - [ ] Queue metrics
- [ ] Batch requests where possible (e.g. yfinance allows this)
- [ ] Profile pollers to identify bottlenecks (e.g. queue send time)

---

## 📈 Metrics

- [ ] Send metrics to stdout/Prometheus for:
  - [ ] API response times
  - [ ] Successful vs failed polls
  - [ ] Queue send latency
- [ ] Add `track_polling_metrics()` and `track_request_metrics()` to all pollers

---

## 🔄 CI/CD Integration

- [ ] Ensure GitHub Actions CI runs:
  - [ ] Pre-commit hooks
  - [ ] Linting (ruff, black, mypy)
  - [ ] Tests
- [ ] Publish Docker images or zip bundles (optional)
- [ ] Add version tagging via GitHub releases

---

## 🧹 Cleanup

- [ ] Remove unused imports, redundant code
- [ ] Validate all docstrings and type hints
- [ ] Delete placeholder templates (if any)
- [ ] Ensure consistent directory structure across all repos

---

## 📝 Documentation

- [ ] Add README badges: build, test, coverage
- [ ] Include setup instructions in `README.md`
- [ ] Add `CONTRIBUTING.md` and `LICENSE` if missing
