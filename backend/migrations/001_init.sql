-- Core schema for the account-aggregation MVP.
-- Money is stored as integer minor units (cents) to avoid float drift.
-- All timestamps are UTC.

CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email       TEXT        NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE institutions (
    id          BIGSERIAL PRIMARY KEY,
    slug        TEXT        NOT NULL UNIQUE,   -- 'mockbank', 'acme-credit-union'
    name        TEXT        NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- A user's connection to one institution. Tokens are stored encrypted (step 4).
CREATE TABLE links (
    id              BIGSERIAL PRIMARY KEY,
    user_id         BIGINT      NOT NULL REFERENCES users(id),
    institution_id  BIGINT      NOT NULL REFERENCES institutions(id),
    status          TEXT        NOT NULL DEFAULT 'pending',  -- pending | connected | error
    access_token    BYTEA,                                   -- encrypted; null until connected
    refresh_token   BYTEA,
    token_expires_at TIMESTAMPTZ,
    sync_cursor     TEXT,                                    -- provider cursor for incremental sync
    last_error      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, institution_id)
);

CREATE TABLE accounts (
    id                  BIGSERIAL PRIMARY KEY,
    link_id             BIGINT      NOT NULL REFERENCES links(id),
    external_account_id TEXT        NOT NULL,   -- the provider's account id
    name                TEXT        NOT NULL,
    mask                TEXT,                    -- last 4 digits
    currency            TEXT        NOT NULL DEFAULT 'USD',
    balance_minor       BIGINT      NOT NULL DEFAULT 0,
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (link_id, external_account_id)
);

CREATE TABLE transactions (
    id                      BIGSERIAL PRIMARY KEY,
    account_id              BIGINT      NOT NULL REFERENCES accounts(id),
    external_transaction_id TEXT        NOT NULL,
    amount_minor            BIGINT      NOT NULL,   -- signed: negative = debit
    currency                TEXT        NOT NULL DEFAULT 'USD',
    description             TEXT        NOT NULL,
    posted_at               TIMESTAMPTZ NOT NULL,
    UNIQUE (account_id, external_transaction_id)
);

CREATE INDEX idx_links_user      ON links (user_id);
CREATE INDEX idx_accounts_link   ON accounts (link_id);
CREATE INDEX idx_tx_account_time ON transactions (account_id, posted_at DESC);
