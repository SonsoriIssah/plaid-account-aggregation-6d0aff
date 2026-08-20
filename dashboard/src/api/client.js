// One place that knows the backend origin and the auth header.
const BASE = import.meta.env.VITE_BACKEND || "http://localhost:8000";

// MVP auth: a hardcoded user id sent as a header (mirrors the backend's X-User-Id).
const USER_ID = "1";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": USER_ID,
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body?.error?.message || `request failed: ${res.status}`);
  }
  return res.status === 204 ? null : res.json();
}

export const api = {
  listInstitutions: () => request("/institutions"),
  createLink: (institution_slug) =>
    request("/links", { method: "POST", body: JSON.stringify({ institution_slug }) }),
  triggerSync: (linkId) => request(`/links/${linkId}/sync`, { method: "POST" }),
  listAccounts: () => request("/accounts"),
  listTransactions: (accountId, limit = 50) =>
    request(`/accounts/${accountId}/transactions?limit=${limit}`),
};
