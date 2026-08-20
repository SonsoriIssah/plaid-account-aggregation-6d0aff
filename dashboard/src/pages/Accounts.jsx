import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function Accounts() {
  const [accounts, setAccounts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .listAccounts()
      .then((data) => setAccounts(data.accounts))
      .catch((e) => setError(e.message));
  }, []);

  if (error) return <pre className="error">{error}</pre>;

  return (
    <section>
      <h2>Accounts</h2>
      {accounts.length === 0 ? (
        <p>No accounts yet — link an institution and sync.</p>
      ) : (
        <ul>
          {accounts.map((a) => (
            <li key={a.id}>
              {a.institution} · {a.account_name} ····{a.mask} —{" "}
              {a.currency} {a.balance.toFixed(2)}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
