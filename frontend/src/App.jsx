import { useState } from "react";
import "./App.css";

function App() {
  const [status, setStatus] = useState("Ready to sync");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const syncEmails = async () => {
    setLoading(true);
    setStatus("Syncing...");
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/sync", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      
      if (data.status === "success") {
        setStatus("Completed");
        setResult({
          processed_emails: data.processed_emails,
          timestamp: data.timestamp
        });
      } else {
        setStatus("Error");
      }
    } catch (err) {
      console.error("Sync error:", err);
      setStatus("Error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        {/* Header with Icons */}
        <div className="header-icons">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="icon">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <polyline points="22,6 12,13 2,6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="icon arrow">
            <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="icon">
            <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="2"/>
            <line x1="3" y1="9" x2="21" y2="9" stroke="currentColor" strokeWidth="2"/>
            <line x1="3" y1="15" x2="21" y2="15" stroke="currentColor" strokeWidth="2"/>
            <line x1="9" y1="3" x2="9" y2="21" stroke="currentColor" strokeWidth="2"/>
            <line x1="15" y1="3" x2="15" y2="21" stroke="currentColor" strokeWidth="2"/>
          </svg>
        </div>

        {/* Main Title */}
        <h1 className="title">Gmail → Google Sheets</h1>
        <p className="subtitle">This demo runs using the application owner's Gmail account.</p>

        {/* Email Sync Section */}
        <div className="sync-section">
          <h2 className="section-title">Email Sync</h2>
          <p className="section-desc">Fetch emails and sync them to your Google Sheet</p>
          
          <button 
            className={`sync-btn ${loading ? 'loading' : ''} ${result ? 'completed' : ''}`}
            onClick={syncEmails}
            disabled={loading}
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15" 
                    stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span>{loading ? "Syncing..." : "Sync Emails"}</span>
          </button>
        </div>

        {/* Status Section */}
        <div className="status-section">
          <div className="status-row">
            <span className="status-label">Status</span>
            <span className={`status-badge ${status.toLowerCase()}`}>
              {status === "Completed" && "✓"} {status}
            </span>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="results-section">
            <div className="result-row">
              <span className="result-label">Emails Processed</span>
              <span className="result-value">{result.processed_emails}</span>
            </div>
            <div className="result-row">
              <span className="result-label">Last Sync</span>
              <span className="result-value">
                {new Date(result.timestamp).toLocaleDateString('en-US', { 
                  month: 'short', 
                  day: 'numeric', 
                  year: 'numeric' 
                })} {new Date(result.timestamp).toLocaleTimeString('en-US', { 
                  hour: 'numeric', 
                  minute: '2-digit', 
                  hour12: true 
                })}
              </span>
            </div>

            {/* Success Message */}
            <div className="success-message">
              <svg viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
              </svg>
              <div>
                <strong>Sync completed successfully</strong>
                <p>{result.processed_emails} emails have been synced to your Google Sheet.</p>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <footer className="app-footer">
          <p>Built with React & FastAPI • Portfolio Demo</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
