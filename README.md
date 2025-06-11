# Stock Analysis Engine

This repository processes raw market data and produces actionable insights or
computed indicators using technical, quantitative, or alternative methods.

## Features

- Supports multiple analysis strategies (technical, factor-based, alt-data)
- Pluggable processor functions per indicator type
- Queue-driven or database-driven architecture
- Structured output schema for downstream consumption
- Fully containerized with support for Kubernetes
- Structured logging and metric-ready instrumentation

## Project Structure

```
src/
├── app/
│   ├── config.py
│   ├── main.py
│   ├── queue_handler.py        # Consumes messages and dispatches to processor
│   ├── processor.py            # Core analysis logic
│   ├── output_handler.py       # Writes to queue or database
│   └── utils/
```

## Usage

```bash
make install
make run
```

## Environment Variables

| Variable      | Description                        |
| ------------- | ---------------------------------- |
| `QUEUE_TYPE`  | Input source: `rabbitmq` or `sqs`  |
| `OUTPUT_TYPE` | Output mode: `db`, `queue`, `rest` |
| `VAULT_ADDR`  | Vault server address               |
| `VAULT_TOKEN` | Vault token or AppRole auth config |

## Development

```bash
make lint
make test
make build
```

## License

Apache License 2.0
