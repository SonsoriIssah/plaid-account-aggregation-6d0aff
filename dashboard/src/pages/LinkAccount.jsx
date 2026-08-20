import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function LinkAccount() {
  const [institutions, setInstitutions] = useState([]);
  const [status, setStatus] = useState("");

  useEffect(() => {
    api.listInstitutions().then((d) => setInstitutions(d.institutions));
  }, []);

  async function link(slug) {
    setStatus("linking…");
    const { link_id } = await api.createLink(slug);
    // In a real OAuth flow the backend returns an authorize_url to redirect to;
    // the mock connector completes server-side, so we go straight to syncing.
    await api.triggerSync(link_id);
    setStatus(`sync requested for link ${link_id}`);
  }

  return (
    <section>
      <h2>Link an institution</h2>
      <ul>
        {institutions.map((i) => (
          <li key={i.slug}>
            {i.name} <button onClick={() => link(i.slug)}>Link</button>
          </li>
        ))}
      </ul>
      <p>{status}</p>
    </section>
  );
}
