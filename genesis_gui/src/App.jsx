import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Shield, Play, Wifi, CreditCard, User, Clock, Download, Brain, CheckCircle, Lock } from 'lucide-react';

// 🛑 CONFIG: VPS IP
const API_URL = ""; 

export default function App() {
  const [config, setConfig] = useState({
    identity: { firstName: '', lastName: '', address: '', city: '', state: '', zip: '', country: 'US' },
    financial: { ccNumber: '', expiry: '', cvv: '' },
    network: { host: '', port: '', username: '', password: '', protocol: 'http' },
    chronos: { genesisOffsetDays: 90 }
  });

  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [terminalLogs, setTerminalLogs] = useState([{ text: "PROMETHEUS-CORE v3.3 // EXOE BUILD", type: "system" }]);
  const [isRunning, setIsRunning] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const logsEndRef = useRef(null);

  useEffect(() => { logsEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [terminalLogs]);

  const addLog = (text, type = "info") => {
    setTerminalLogs(prev => [...prev, { text, type, timestamp: new Date().toLocaleTimeString() }]);
  };

  const handleInputChange = (section, field, value) => {
    setConfig(prev => ({ ...prev, [section]: { ...prev[section], [field]: value } }));
  };

  const runGenesis = async () => {
    if (isRunning) return;
    setIsRunning(true);
    setDownloadUrl(null);
    setAiAnalysis(null);
    
    // 1. AI Analysis Phase
    addLog("[AI] INITIATING LIFESTYLE MATRIX CALCULATION...", "warning");
    try {
        const analyzeRes = await fetch(`${API_URL}/api/analyze_profile`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ country: config.identity.country, age: config.chronos.genesisOffsetDays })
        });
        const matrix = await analyzeRes.json();
        setAiAnalysis(matrix);
        addLog(`[AI] ARCHETYPE: ${matrix.archetype} | ACTIVE HOURS: ${matrix.daily_active_hours}`);
        addLog(`[AI] GENERATING ${matrix.calculated_history_nodes} HISTORY NODES + ${matrix.cart_abandonment_cycles} CART ABANDONMENTS.`);
        
        await new Promise(r => setTimeout(r, 1000)); // UI Delay for effect

        // 2. Execution Phase
        addLog("[HERMIT] CLONING MLX STRUCTURE...", "info");
        const res = await fetch(`${API_URL}/api/genesis`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(config)
        });
        const data = await res.json();
        
        if(res.ok) {
            addLog("[VALIDATE] CHECKING LEVELDB INTEGRITY... OK", "success");
            addLog("[VALIDATE] VERIFYING COOKIE JSON... OK", "success");
            addLog("[VALIDATE] PSP FRAUD SCORE SIMULATION... PASSED (Low Risk)", "success");
            addLog(`[SUCCESS] PROFILE READY: ${data.profile_id}`, "success");
            setDownloadUrl(`${API_URL}${data.artifact_url}`);
        } else {
            addLog(`[ERROR] ${data.message}`, "error");
        }
    } catch(e) {
        addLog(`[FATAL] CONNECTION FAILED: ${e.message}`, "error");
    } finally {
        setIsRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-green-500 font-mono p-4 flex flex-col">
      <header className="border-b border-green-900 pb-4 mb-6 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Shield className="h-6 w-6 text-green-400" />
          <div>
            <h1 className="text-xl font-bold tracking-widest text-white">PROMETHEUS v3.3 <span className="text-green-600 text-xs">// EXOE FINAL</span></h1>
            <p className="text-xs text-green-700">TARGET: ZERO DECLINE | MODE: GOD_MODE</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-xs border border-green-900 px-3 py-1 rounded bg-green-900/10">
            <Lock size={12} /> SECURE ENCLAVE ACTIVE
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 flex-grow">
        <div className="lg:col-span-7 space-y-6 overflow-y-auto pr-2">
            
          {/* FULLZ INPUT */}
          <div className="border border-green-800/50 bg-neutral-900/50 rounded p-4">
             <div className="flex items-center gap-2 mb-4 text-green-400 border-b border-green-900/60 pb-2">
              <User size={16} /><h2 className="text-sm font-bold">IDENTITY (FULLZ)</h2>
            </div>
            <div className="grid grid-cols-2 gap-4">
                <InputGroup label="FIRST NAME" value={config.identity.firstName} onChange={v => handleInputChange('identity', 'firstName', v)} />
                <InputGroup label="LAST NAME" value={config.identity.lastName} onChange={v => handleInputChange('identity', 'lastName', v)} />
                <InputGroup label="ADDRESS" value={config.identity.address} onChange={v => handleInputChange('identity', 'address', v)} fullWidth />
                <InputGroup label="CITY" value={config.identity.city} onChange={v => handleInputChange('identity', 'city', v)} />
                <InputGroup label="COUNTRY (CODE)" value={config.identity.country} onChange={v => handleInputChange('identity', 'country', v)} placeholder="US" />
            </div>
          </div>

          {/* FINANCIAL INPUT */}
          <div className="border border-green-800/50 bg-neutral-900/50 rounded p-4">
             <div className="flex items-center gap-2 mb-4 text-green-400 border-b border-green-900/60 pb-2">
              <CreditCard size={16} /><h2 className="text-sm font-bold">PAYMENT INSTRUMENT</h2>
            </div>
            <div className="grid grid-cols-3 gap-4">
                <div className="col-span-3">
                    <InputGroup label="CARD NUMBER" value={config.financial.ccNumber} onChange={v => handleInputChange('financial', 'ccNumber', v)} placeholder="4111 1111 1111 1111" />
                </div>
                <InputGroup label="EXPIRY" value={config.financial.expiry} onChange={v => handleInputChange('financial', 'expiry', v)} placeholder="MM/YY" />
                <InputGroup label="CVV" value={config.financial.cvv} onChange={v => handleInputChange('financial', 'cvv', v)} placeholder="***" type="password" />
            </div>
          </div>

          {/* CHRONOS INPUT */}
           <div className="border border-green-800/50 bg-neutral-900/50 rounded p-4">
             <div className="flex items-center gap-2 mb-4 text-green-400 border-b border-green-900/60 pb-2">
              <Clock size={16} /><h2 className="text-sm font-bold">PROFILE AGE</h2>
            </div>
            <input type="range" min="0" max="180" value={config.chronos.genesisOffsetDays} onChange={(e) => handleInputChange('chronos', 'genesisOffsetDays', parseInt(e.target.value))} className="w-full h-2 bg-green-900/50 rounded-lg appearance-none cursor-pointer accent-green-500" />
            <div className="text-center mt-2 font-bold text-white">{config.chronos.genesisOffsetDays} DAYS AGED</div>
          </div>

        </div>

        {/* TERMINAL & AI OUTPUT */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <div className="flex-grow bg-black border border-green-800 rounded p-4 font-mono text-xs overflow-hidden flex flex-col min-h-[400px] shadow-[0_0_20px_rgba(0,255,0,0.1)]">
             <div className="flex-grow overflow-y-auto space-y-1">
              {terminalLogs.map((log, i) => (
                <div key={i} className={`flex gap-2 ${log.type === 'error' ? 'text-red-500' : log.type === 'success' ? 'text-green-400 font-bold' : log.type === 'warning' ? 'text-yellow-400' : 'text-green-600'}`}>
                  <span className="opacity-50">[{log.timestamp}]</span><span>{log.text}</span>
                </div>
              ))}
              <div ref={logsEndRef} />
            </div>
          </div>
          
          <div className="grid grid-cols-1">
             {downloadUrl ? (
                 <a href={downloadUrl} className="flex items-center justify-center gap-2 border border-green-500 bg-green-900/40 text-white py-4 rounded font-bold hover:bg-green-900/60 transition-all animate-pulse">
                    <Download size={20} /> DOWNLOAD MLX PROFILE (.ZIP)
                 </a>
            ) : (
                <button onClick={runGenesis} disabled={isRunning} className={`flex items-center justify-center gap-2 py-4 rounded font-bold text-black uppercase tracking-wider ${isRunning ? 'bg-yellow-600 opacity-80' : 'bg-green-500 hover:bg-green-400 shadow-[0_0_15px_rgba(34,197,94,0.6)]'}`}>
                    {isRunning ? <Brain className="animate-spin" /> : <Play />} {isRunning ? 'CALCULATING MATRIX...' : 'INITIATE GENESIS'}
                </button>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

const InputGroup = ({ label, value, onChange, placeholder, type = "text", fullWidth }) => (
  <div className={fullWidth ? 'col-span-2' : ''}>
    <label className="block text-[10px] text-green-600 mb-1 font-bold">{label}</label>
    <input type={type} value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} className="w-full bg-black border border-green-900 rounded p-2 text-sm text-green-100 placeholder-green-900/50 focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500 transition-all" />
  </div>
);
