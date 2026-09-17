import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Patient = { patient_id: string };
type Finding = { condition: string; evidence: string[]; confidence: number; rationale: string };
type Result = { request_id: string; patient_id: string; suspects: Finding[] };
const API = "http://localhost:8000";

function App() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [patientId, setPatientId] = useState("SYN-1001");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/v1/patients`).then(r => r.json()).then(setPatients);
  }, []);

  async function analyze() {
    setLoading(true);
    try {
      const response = await fetch(`${API}/api/v1/patients/${patientId}/suspects`, { method: "POST" });
      setResult(await response.json());
    } finally { setLoading(false); }
  }

  return <main className="shell">
    <section className="hero">
      <p className="eyebrow">CLINICAL INTELLIGENCE / SYNTHETIC DEMO</p>
      <h1>Prospective Suspecting Workspace</h1>
      <p>Retrieve synthetic patient context and inspect evidence supporting potential findings.</p>
    </section>
    <section className="panel controls">
      <label htmlFor="patient">Synthetic patient</label>
      <select id="patient" value={patientId} onChange={e => setPatientId(e.target.value)}>
        {patients.map(p => <option key={p.patient_id}>{p.patient_id}</option>)}
      </select>
      <button onClick={analyze} disabled={loading}>{loading ? "Analyzing..." : "Analyze record"}</button>
    </section>
    {result && <section className="results">
      <div className="resultHeader"><h2>Results</h2><span>{result.patient_id}</span></div>
      {result.suspects.length === 0 && <div className="panel">No supported findings identified.</div>}
      {result.suspects.map(item => <article className="panel finding" key={item.condition}>
        <div className="row"><h3>{item.condition}</h3><strong>{Math.round(item.confidence * 100)}%</strong></div>
        <p>{item.rationale}</p><h4>Retrieved evidence</h4>
        {item.evidence.map(text => <blockquote key={text}>{text}</blockquote>)}
      </article>)}
      <p className="request">Request ID: {result.request_id}</p>
    </section>}
    <footer>Portfolio demonstration using synthetic data only. Not for clinical decision-making.</footer>
  </main>;
}

createRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);
