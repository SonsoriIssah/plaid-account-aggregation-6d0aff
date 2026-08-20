# Plaid | Financial Account Aggregation API

An intermediate capstone modeled on Plaid's core problem — aggregating accounts across many financial institutions behind a single API. You design a Postgres schema for users/links/accounts/transactions, build a FastAPI service with a consistent error envelope and auth context, model an institution catalog and link flow, complete an OAuth2 code exchange for a mock bank, fan ingestion out over Kafka to a separate worker that normalizes and idempotently upserts transactions with a sync cursor, add a Redis cache-aside layer, expose unified paginated account/transaction endpoints, instrument logs and metrics, ship a small React dashboard, and harden the whole thing with timeouts, bounded retries, and per-user rate limiting.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- FastAPI
- Postgres
- Redis
- Kafka
- OAuth2
- React
