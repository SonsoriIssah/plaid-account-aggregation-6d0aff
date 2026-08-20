import { useState } from "react";
import LinkAccount from "./pages/LinkAccount";
import Accounts from "./pages/Accounts";

export default function App() {
  // Linear MVP flow: Link → View Accounts. Minimal client-side state, no router.
  const [tab, setTab] = useState("link");

  return (
    <main>
      <h1>Account Aggregation</h1>
      <nav>
        <button onClick={() => setTab("link")}>Link</button>
        <button onClick={() => setTab("accounts")}>Accounts</button>
      </nav>
      {tab === "link" ? <LinkAccount /> : <Accounts />}
    </main>
  );
}
