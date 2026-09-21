import { useState, useEffect } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState(null);

  // Form State
  const [amount, setAmount] = useState("");
  const [category, setCategory] = useState("");
  const [note, setNote] = useState("");
  const [date, setDate] = useState("");

  // Fetch Data on Load
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const expensesRes = await fetch(`${API_BASE_URL}/expenses`);
      const expensesData = await expensesRes.json();
      setExpenses(expensesData);

      const summaryRes = await fetch(`${API_BASE_URL}/summary`);
      const summaryData = await summaryRes.json();
      setSummary(summaryData);
    } catch (error) {
      console.error("Error fetching data. Is the backend running?", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const newExpense = {
      amount: parseFloat(amount),
      category,
      note,
      date,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/expenses`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newExpense),
      });

      if (response.ok) {
        // Clear form and refresh data
        setAmount("");
        setCategory("");
        setNote("");
        setDate("");
        fetchData();
      } else {
        alert("Failed to add expense. Check your inputs.");
      }
    } catch (error) {
      console.error("Error submitting expense:", error);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px", fontFamily: "sans-serif" }}>
      <h1>Spend Tracker</h1>

      <section style={{ marginBottom: "40px" }}>
        <h2>Add Expense</h2>
        <form onSubmit={handleSubmit} style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
          <input type="number" step="0.01" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} required />
          <input type="text" placeholder="Category (e.g. Food)" value={category} onChange={(e) => setCategory(e.target.value)} required />
          <input type="text" placeholder="Note (optional)" value={note} onChange={(e) => setNote(e.target.value)} />
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
          <button type="submit">Add Expense</button>
        </form>
      </section>

      {summary && (
        <section style={{ marginBottom: "40px", padding: "15px", backgroundColor: "#f4f4f4", borderRadius: "8px" }}>
          <h2>Summary</h2>
          <p><strong>Total Spend:</strong> ${summary.total_spend.toFixed(2)}</p>
          <p>
            <strong>MoM Change:</strong> {summary.mom_change_percentage > 0 ? "+" : ""}
            {summary.mom_change_percentage}%
            {summary.mom_change_percentage > 20 && " ⚠️ (Category spend increased by more than 20%!)"}
          </p>
          
          <h3>By Category</h3>
          <ul>
            {Object.entries(summary.spend_by_category).map(([cat, total]) => (
              <li key={cat}>{cat}: ${total.toFixed(2)}</li>
            ))}
          </ul>
        </section>
      )}

      <section>
        <h2>Expense History</h2>
        <table style={{ width: "100%", textAlign: "left", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #ccc" }}>
              <th>Date</th>
              <th>Category</th>
              <th>Note</th>
              <th>Amount</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((exp) => (
              <tr key={exp.id} style={{ borderBottom: "1px solid #eee" }}>
                <td>{exp.date}</td>
                <td>{exp.category}</td>
                <td>{exp.note || "-"}</td>
                <td>${exp.amount.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;