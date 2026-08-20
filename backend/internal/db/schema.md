# Data model

| entity        | owns                                   | key uniqueness                         |
|---------------|----------------------------------------|----------------------------------------|
| users         | identity                               | email                                  |
| institutions  | seeded connector config                | slug                                   |
| links         | a user↔institution connection + tokens | (user_id, institution_id)              |
| accounts      | a balance under a link                 | (link_id, external_account_id)         |
| transactions  | a posted line item under an account    | (account_id, external_transaction_id)  |

## Why these shapes

- **Money = integer minor units.** `balance_minor` / `amount_minor` are cents.
  Floating point silently loses pennies; integers never do.
- **Multi-tenancy via user_id.** Every read is scoped to the calling user by
  joining back to `links.user_id`. A user can never see another user's data.
- **External ids + composite uniqueness** make ingestion *idempotent*: re-running
  a sync upserts on `(account_id, external_transaction_id)` instead of duplicating.
- **sync_cursor** is the provider's "everything after this" token. We persist it
  per link so the next sync is *incremental*, not a full re-pull.
