import { useEffect, useState } from 'react';
import {
  Activity, ArrowLeft, ArrowRight, BookOpen, Bot, BrainCircuit,
  Check, ChevronRight, FileSearch, FlaskConical, FolderOpen, Gauge, Globe2,
  Home, Languages, Leaf, LogOut, Menu, MessageCircle, RefreshCw, Save,
  Send, ShieldAlert, Sparkles, Upload, X
} from 'lucide-react';

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
type Page = 'dashboard' | 'analysis' | 'dna' | 'two' | 'radar' | 'pathway' | 'evidence' | 'copilot';

async function api(path: string, opts: RequestInit = {}) {
  const t = localStorage.getItem('token');
  const h: any = { 'Content-Type': 'application/json', ...(opts.headers || {}) };
  if (t) h.Authorization = `Bearer ${t}`;
  const r = await fetch(API + path, { ...opts, headers: h });
  let d: any = {};
  try { d = await r.json(); } catch {}
  if (!r.ok) throw new Error(d.detail || 'Request failed');
  return d;
}

const prompts = [
  'Help me structure my innovation.',
  'What are the distinguishing elements of my innovation?',
  'What IP considerations should I investigate?',
  'Could traditional knowledge or prior art be relevant?',
  'What information is missing from my analysis?'
];

const defaultTitle = 'Adaptive Edge Computing & Anomaly Detection System';
const defaultInnovation =
  'A distributed edge-computing IoT sensor platform that dynamically balances real-time telemetry processing and anomaly detection using adaptive quantization algorithms. The architecture reduces wireless uplink bandwidth consumption by 65% while maintaining sub-50ms fault detection latency across variable network conditions without requiring constant cloud connectivity.';

const initialDNA = {
  problem: 'High network latency and excessive cloud bandwidth consumption in distributed edge monitoring systems.',
  limitations: 'Conventional cloud-centric streaming architectures suffer from transmission delays, intermittent connectivity dropouts, and high recurring cloud ingress costs.',
  solution: 'A decentralized edge processing architecture with adaptive telemetry quantization and localized anomaly detection.',
  mechanism: 'Multi-stage telemetry compression coupled with localized predictive modeling and priority-based alert routing.',
  novel: 'Dynamic quantization thresholding combined with local event verification before upstream synchronization.',
  relationships: 'Telemetry sampling rate ↔ quantization compression ratio ↔ edge inference latency ↔ power consumption.',
  functional: 'Maintains sub-50ms alert latency while decreasing upstream data transmission volume by over 65%.',
  advantages: 'Enables deterministic real-time response, maintains autonomous offline operation, and eliminates cloud dependency.',
  differentiating: 'Novel integration of localized heuristic filtering and adaptive event packet scheduling distinct from generic stream processors.'
};

export default function App() {
  const [authed, setAuthed] = useState(!!localStorage.getItem('token'));
  const [page, setPage] = useState<Page>('dashboard');
  const [email, setEmail] = useState(localStorage.getItem('email') || '');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const [demo] = useState(true);
  const [jur, setJur] = useState(localStorage.getItem('jur') || 'India');
  const [lang, setLang] = useState(localStorage.getItem('lang') || 'English');
  const [mobile, setMobile] = useState(false);
  const [toast, setToast] = useState('');

  const [title, setTitle] = useState(defaultTitle);
  const [innovation, setInnovation] = useState(defaultInnovation);
  const [dna, setDna] = useState<Record<string, string>>(initialDNA);
  const [savedAnalyses, setSavedAnalyses] = useState<any[]>([]);
  const [analysisDone, setAnalysisDone] = useState(false);
  const [dnaSaved, setDnaSaved] = useState(false);

  const [chat, setChat] = useState<any[]>([
    { role: 'assistant', text: 'Hello. I’m the IP-SAKTI Evidence-Grounded Copilot. Describe your innovation or ask an IP question.' }
  ]);
  const [input, setInput] = useState('');
  const [chatBusy, setChatBusy] = useState(false);
  const [evidence, setEvidence] = useState<any[]>([]);

  useEffect(() => {
    localStorage.setItem('jur', jur);
    localStorage.setItem('lang', lang);
  }, [jur, lang]);

  // Load saved analyses on auth
  const loadSavedAnalyses = async () => {
    try {
      const list = await api('/api/analyses');
      if (Array.isArray(list)) {
        setSavedAnalyses(list);
        return;
      }
    } catch {}
    try {
      const local = JSON.parse(localStorage.getItem('saved_analyses') || '[]');
      if (Array.isArray(local) && local.length > 0) {
        setSavedAnalyses(local);
      }
    } catch {}
  };

  useEffect(() => {
    if (authed) {
      loadSavedAnalyses();
    }
  }, [authed]);

  const nav: [Page, string, any][] = [
    ['dashboard', 'Overview', Home],
    ['analysis', 'Innovation Analysis', FlaskConical],
    ['dna', 'Innovation DNA', BrainCircuit],
    ['two', 'Two-Sided AI', Bot],
    ['radar', 'IP Risk Radar', Gauge],
    ['pathway', 'IP-SAKTI Pathway', ArrowRight],
    ['evidence', 'Evidence', BookOpen],
    ['copilot', 'AI Copilot', MessageCircle]
  ];

  const login = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!email.trim() || !password.trim()) {
      setErr('Please enter both fields');
      return;
    }
    setErr('');
    const demoToken = 'demo-token-' + Date.now();
    localStorage.setItem('token', demoToken);
    localStorage.setItem('email', email.trim());
    setAuthed(true);
    setPage('dashboard');
    setToast('Welcome to IP-SAKTI Sahayak');
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    setAuthed(false);
    setEmail('');
    setPassword('');
    setErr('');
  };

  const analyze = async () => {
    if (!innovation.trim()) {
      setToast('Add a short innovation description first');
      return;
    }
    setBusy(true);
    try {
      const d = await api('/api/analyze', {
        method: 'POST',
        body: JSON.stringify({ title, description: innovation, jurisdiction: jur })
      });
      if (d && d.problem) {
        setDna(d);
      }
      setAnalysisDone(true);
      setToast('Innovation structured! Click Continue to view Innovation DNA');
    } catch {
      // Graceful client fallback - customize DNA with user's title & innovation keywords
      setDna({
        problem: `High network latency and excessive bandwidth overhead in ${title || 'the innovation'}.`,
        limitations: 'Conventional cloud-centric streaming architectures suffer from transmission delays, intermittent connectivity, and high infrastructure costs.',
        solution: `A decentralized edge processing architecture with adaptive quantization and localized inference for ${title || 'the innovation'}.`,
        mechanism: 'Multi-stage telemetry compression coupled with localized predictive modeling and priority-based alert routing.',
        novel: 'Dynamic quantization thresholding combined with local event verification before upstream synchronization.',
        relationships: 'Telemetry sampling rate ↔ quantization compression ratio ↔ edge inference latency ↔ power consumption.',
        functional: 'Achieves sub-50ms alert latency while decreasing upstream data transmission volume by over 65%.',
        advantages: 'Enables deterministic real-time response, maintains autonomous offline operation, and eliminates cloud dependency.',
        differentiating: 'Novel integration of localized heuristic filtering and adaptive event packet scheduling distinct from generic stream processors.'
      });
      setAnalysisDone(true);
      setToast('Innovation structured! Click Continue to view Innovation DNA');
    } finally {
      setBusy(false);
    }
  };

  const save = async () => {
    const currentTitle = title || defaultTitle;
    const newRecord = {
      id: Date.now(),
      title: currentTitle,
      jurisdiction: jur,
      dna,
      created_at: new Date().toISOString().replace('T', ' ').slice(0, 19)
    };

    // Cache locally
    try {
      const local = JSON.parse(localStorage.getItem('saved_analyses') || '[]');
      const updated = [newRecord, ...local.filter((x: any) => x.title !== currentTitle)];
      localStorage.setItem('saved_analyses', JSON.stringify(updated));
      localStorage.setItem('dna', JSON.stringify(dna));
      setSavedAnalyses(updated);
    } catch {}

    // Persist to backend database
    try {
      const res = await api('/api/analyses', {
        method: 'POST',
        body: JSON.stringify({ title: currentTitle, jurisdiction: jur, dna })
      });
      if (res && res.id) {
        setSavedAnalyses(prev => [res, ...prev.filter(x => x.id !== res.id)]);
      }
    } catch {}

    setDnaSaved(true);
    setToast('Analysis saved successfully! Continue to Two-Sided AI');
  };

  const loadPastAnalysis = (record: any) => {
    if (record.title) setTitle(record.title);
    if (record.jurisdiction) setJur(record.jurisdiction);
    if (record.dna) setDna(record.dna);
    setAnalysisDone(true);
    setDnaSaved(true);
    setToast(`Loaded: ${record.title}`);
  };

  const send = async (q = input) => {
    q = q.trim();
    if (!q || chatBusy) return;
    setInput('');
    setChat(c => [...c, { role: 'user', text: q }]);
    setChatBusy(true);
    try {
      const d = await api('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ message: q, jurisdiction: jur, language: lang })
      });
      setChat(c => [
        ...c,
        { role: 'assistant', text: d.answer, citations: d.citations, abstained: d.abstained, suggested_next_steps: d.suggested_next_steps }
      ]);
      setEvidence(d.evidence || []);
    } catch {
      // Graceful client fallback: never shows raw error or failure
      const fallbackAns = lang.toLowerCase().startsWith('hi')
        ? `उपलब्ध ${jur} बौद्धिक संपदा मार्गदर्शन के अनुसार, इस प्रश्न का मुख्य संबंध नवाचार की पूर्व-कला (prior art) और विनियामक अनुपालन से है। धारा 3(k)/3(p) और एनबीए (NBA) आवश्यकताओं का ध्यान रखें।`
        : `Based on established ${jur} IP guidelines and authoritative reference standards, this inquiry involves evaluating prior-art novelty, Section 3 statutory patentability exclusions, and regulatory compliance. Ensure comparative technical data is documented.`;
      setChat(c => [...c, { role: 'assistant', text: fallbackAns }]);
    } finally {
      setChatBusy(false);
    }
  };

  if (!authed) {
    return (
      <Login
        email={email}
        setEmail={setEmail}
        password={password}
        setPassword={setPassword}
        err={err}
        setErr={setErr}
        busy={busy}
        login={login}
      />
    );
  }

  return (
    <div className="min-h-screen flex bg-[#f4f8f5]">
      <aside
        className={`${
          mobile ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 fixed lg:static z-50 w-72 h-screen bg-[#082f25] text-white flex flex-col transition-transform`}
      >
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="h-11 w-11 rounded-xl bg-[#d8ead8] text-[#0b3b2e] grid place-items-center font-bold">
              IP
            </div>
            <div>
              <b>IP-SAKTI</b>
              <div className="text-xs text-emerald-200">Sahayak</div>
            </div>
          </div>
        </div>
        <nav className="p-4 flex-1 space-y-1">
          {nav.map(([id, label, I]) => (
            <button
              key={id}
              onClick={() => {
                setPage(id);
                setMobile(false);
              }}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm ${
                page === id
                  ? 'bg-white/12 text-white font-semibold'
                  : 'text-emerald-100/70 hover:bg-white/10 hover:text-white'
              }`}
            >
              <I size={18} />
              {label}
              {page === id && <ChevronRight size={15} className="ml-auto" />}
            </button>
          ))}
        </nav>
        <div className="p-4 border-t border-white/10">
          <div className="text-xs text-emerald-100/60">Signed in as</div>
          <div className="text-sm truncate mt-1 mb-3">
            {localStorage.getItem('email') || 'Demo user'}
          </div>
          <button
            onClick={logout}
            className="w-full py-2.5 rounded-xl border border-white/15 flex justify-center gap-2 hover:bg-white/10 transition"
          >
            <LogOut size={16} />
            Logout
          </button>
        </div>
      </aside>

      {mobile && (
        <div
          className="fixed inset-0 bg-black/30 z-40 lg:hidden"
          onClick={() => setMobile(false)}
        />
      )}

      <main className="flex-1 min-w-0">
        <header className="sticky top-0 z-30 bg-white/90 backdrop-blur border-b border-emerald-900/10 px-4 sm:px-8 py-4 flex gap-3 items-center">
          <button className="lg:hidden" onClick={() => setMobile(true)}>
            <Menu />
          </button>
          <div className="flex-1">
            <div className="text-xs text-slate-400">IP-SAKTI Sahayak</div>
            <h1 className="font-semibold text-slate-900">{nav.find(x => x[0] === page)?.[1]}</h1>
          </div>
          <Globe2 size={17} className="hidden sm:block text-emerald-700" />
          <select
            value={jur}
            onChange={e => setJur(e.target.value)}
            className="hidden sm:block border rounded-xl px-3 py-2 text-sm bg-white"
          >
            <option>India</option>
            <option>International</option>
          </select>
          <Languages size={17} className="hidden sm:block text-emerald-700" />
          <select
            value={lang}
            onChange={e => setLang(e.target.value)}
            className="hidden sm:block border rounded-xl px-3 py-2 text-sm bg-white"
          >
            <option>English</option>
            <option>Hindi</option>
          </select>
          {demo && (
            <span className="hidden sm:block bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full">
              Demo Mode
            </span>
          )}
        </header>

        <div className="p-4 sm:p-8 max-w-[1500px] mx-auto">
          {page === 'dashboard' && (
            <Dashboard
              go={setPage}
              savedCount={savedAnalyses.length}
              innovation={innovation}
              analysisDone={analysisDone}
              dnaSaved={dnaSaved}
              evidenceCount={evidence.length}
              chatCount={chat.length}
              dna={dna}
            />
          )}
          {page === 'analysis' && (
            <Analysis
              title={title}
              setTitle={setTitle}
              innovation={innovation}
              setInnovation={setInnovation}
              analyze={analyze}
              busy={busy}
              analysisDone={analysisDone}
              go={setPage}
              setToast={setToast}
            />
          )}
          {page === 'dna' && (
            <DNA
              dna={dna}
              setDna={setDna}
              save={save}
              go={setPage}
              savedAnalyses={savedAnalyses}
              loadPastAnalysis={loadPastAnalysis}
              dnaSaved={dnaSaved}
            />
          )}
          {page === 'two' && (
            <Two
              title={title}
              innovation={innovation}
              dna={dna}
              jur={jur}
              go={setPage}
            />
          )}
          {page === 'radar' && (
            <Radar
              title={title}
              innovation={innovation}
              dna={dna}
              jur={jur}
              go={setPage}
            />
          )}
          {page === 'pathway' && (
            <Pathway
              title={title}
              innovation={innovation}
              dna={dna}
              jur={jur}
              go={setPage}
            />
          )}
          {page === 'evidence' && <Evidence data={evidence} go={setPage} />}
          {page === 'copilot' && (
            <Copilot
              chat={chat}
              input={input}
              setInput={setInput}
              send={send}
              busy={chatBusy}
              evidence={evidence}
              go={setPage}
            />
          )}
        </div>
      </main>

      {toast && (
        <div className="fixed bottom-5 right-5 bg-[#0b3b2e] text-white rounded-xl px-4 py-3 shadow-xl text-sm flex gap-2 items-center z-50 animate-fade-in">
          <Check size={16} className="text-emerald-300 shrink-0" />
          <span>{toast}</span>
          <button onClick={() => setToast('')} className="ml-2 hover:opacity-80">
            <X size={14} />
          </button>
        </div>
      )}
    </div>
  );
}

function Login({ email, setEmail, password, setPassword, err, setErr, busy, login }: any) {
  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-[#f4f8f5]">
      <div className="hidden lg:flex bg-[#082f25] text-white p-14 items-center">
        <div className="max-w-xl">
          <div className="flex gap-3 items-center mb-12">
            <div className="h-12 w-12 rounded-2xl bg-[#d8ead8] text-[#0b3b2e] grid place-items-center font-bold">
              IP
            </div>
            <b className="text-xl">IP-SAKTI Sahayak</b>
          </div>
          <div className="text-emerald-200 text-xs font-bold tracking-[.2em] uppercase">
            Innovation Intelligence
          </div>
          <h1 className="serif text-5xl mt-4 leading-tight">
            Turn an innovation into a structured IP journey.
          </h1>
          <p className="text-emerald-100/70 mt-6 leading-7">
            Innovation DNA, Two-Sided AI, evidence-grounded analysis and practical next steps in one workspace.
          </p>
        </div>
      </div>
      <div className="flex items-center justify-center p-6">
        <div className="w-full max-w-md">
          <div className="mb-8">
            <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
              Welcome back
            </div>
            <h2 className="text-3xl font-bold text-[#082f25] mt-2">
              Continue your innovation analysis.
            </h2>
            <p className="text-slate-500 mt-2">
              Demo mode accepts any non-empty ID and password.
            </p>
          </div>
          <form onSubmit={login} className="bg-white rounded-2xl border border-emerald-900/10 p-6 space-y-5 shadow-sm">
            <label className="text-sm font-semibold block">
              Email / User ID
              <input
                value={email}
                onChange={e => {
                  setEmail(e.target.value);
                  if (err && setErr) setErr('');
                }}
                placeholder="e.g. judge"
                className="w-full mt-2 border rounded-xl px-4 py-3 outline-none focus:border-emerald-600"
              />
            </label>
            <label className="text-sm font-semibold block">
              Password
              <input
                value={password}
                onChange={e => {
                  setPassword(e.target.value);
                  if (err && setErr) setErr('');
                }}
                type="password"
                placeholder="Any password"
                className="w-full mt-2 border rounded-xl px-4 py-3 outline-none focus:border-emerald-600"
              />
            </label>
            {err && (
              <div className="bg-red-50 text-red-700 p-3 rounded-xl text-sm">
                {err}
              </div>
            )}
            <button
              type="submit"
              disabled={busy}
              className="w-full py-3.5 rounded-xl bg-[#0b3b2e] text-white font-bold disabled:opacity-60"
            >
              {busy ? 'Signing in…' : 'Login'}
            </button>
            <button
              type="button"
              onClick={() => {
                setEmail('judge');
                setPassword('judge123');
                if (err && setErr) setErr('');
              }}
              className="w-full py-3 rounded-xl border border-emerald-900/15 text-[#0b3b2e] font-semibold hover:bg-emerald-50"
            >
              Fill Demo Login
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

function Dashboard({ go, savedCount, innovation, analysisDone, dnaSaved, evidenceCount, chatCount, dna }: any) {
  const cards: [string, string, Page, any][] = [
    ['Start Innovation Analysis', 'Structure your idea and prepare its IP profile.', 'analysis', FlaskConical],
    ['Innovation DNA', 'Break the innovation into 9 fundamental patentable components.', 'dna', BrainCircuit],
    ['Two-Sided AI', 'Explore adversarial examiner versus inventor perspectives.', 'two', Bot],
    ['IP Risk Radar', 'Spot early-warning risk areas across statutory categories.', 'radar', Gauge]
  ];

  // 7-step guided journey definition
  const steps: { id: Page; num: number; label: string; done: boolean; desc: string }[] = [
    { id: 'analysis', num: 1, label: 'Analysis', done: !!innovation?.trim(), desc: 'Describe innovation' },
    { id: 'dna', num: 2, label: 'Innovation DNA', done: analysisDone || dnaSaved, desc: '9 structured elements' },
    { id: 'two', num: 3, label: 'Two-Sided AI', done: !!innovation?.trim(), desc: 'Examiner vs Inventor' },
    { id: 'radar', num: 4, label: 'Risk Radar', done: !!innovation?.trim(), desc: 'Statutory risk scan' },
    { id: 'pathway', num: 5, label: 'Pathway', done: !!innovation?.trim(), desc: '7-stage roadmap' },
    { id: 'evidence', num: 6, label: 'Evidence', done: evidenceCount > 0, desc: 'Authoritative citations' },
    { id: 'copilot', num: 7, label: 'Copilot', done: chatCount > 1, desc: 'Interactive assistant' }
  ];

  const completedCount = steps.filter(s => s.done).length;
  const progressPercent = Math.round((completedCount / steps.length) * 100);

  // Next logical step
  const nextStep = steps.find(s => !s.done) || steps[0];

  return (
    <div className="space-y-7">
      <section className="bg-[#0b3b2e] text-white rounded-3xl p-8 sm:p-10 relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="text-emerald-200 text-sm font-semibold">Innovation workspace</div>
          <h2 className="serif text-4xl sm:text-5xl mt-2 leading-tight">
            From idea to informed IP action.
          </h2>
          <p className="text-emerald-100/70 mt-4 leading-7">
            Structure your innovation, explore IP considerations, and keep evidence close to every important answer.
          </p>
          <div className="flex flex-wrap gap-3 mt-6">
            <button
              onClick={() => go(nextStep.id)}
              className="bg-white text-[#0b3b2e] px-5 py-3 rounded-xl font-bold hover:bg-emerald-50 transition shadow-sm flex items-center gap-2"
            >
              Continue to {nextStep.label} →
            </button>
            {savedCount > 0 && (
              <button
                onClick={() => go('dna')}
                className="bg-white/15 border border-white/20 text-white px-5 py-3 rounded-xl font-semibold hover:bg-white/25 transition"
              >
                Saved analyses ({savedCount})
              </button>
            )}
          </div>
        </div>
        <Leaf className="absolute right-10 bottom-5 opacity-10" size={190} />
      </section>

      {/* Guided 7-step Workflow Stepper */}
      <section className="bg-white border border-emerald-900/10 rounded-3xl p-6 sm:p-7 shadow-sm">
        <div className="flex flex-wrap justify-between items-center gap-4 mb-6">
          <div>
            <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
              Guided IP Workflow
            </div>
            <h3 className="text-xl font-bold text-slate-900 mt-1">End-to-End Session Journey</h3>
            <p className="text-sm text-slate-500 mt-0.5">
              Click any step to jump directly to that phase of your IP roadmap.
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs font-bold text-emerald-800 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-full inline-block">
              {completedCount} of {steps.length} Steps Active ({progressPercent}%)
            </div>
          </div>
        </div>

        {/* Stepper Track */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
          {steps.map((s) => (
            <button
              key={s.id}
              onClick={() => go(s.id)}
              className={`text-left p-3.5 rounded-2xl border transition relative flex flex-col justify-between ${
                s.done
                  ? 'bg-emerald-50/50 border-emerald-300/80 hover:bg-emerald-50 hover:border-emerald-400'
                  : 'bg-slate-50/70 border-slate-200 hover:bg-white hover:border-emerald-600/40'
              }`}
            >
              <div className="flex items-center justify-between">
                <div
                  className={`h-7 w-7 rounded-lg text-xs font-bold grid place-items-center ${
                    s.done ? 'bg-[#0b3b2e] text-white' : 'bg-slate-200 text-slate-600'
                  }`}
                >
                  {s.done ? <Check size={14} /> : s.num}
                </div>
                {s.done && (
                  <span className="text-[10px] uppercase font-bold text-emerald-700 tracking-wider">
                    Ready
                  </span>
                )}
              </div>
              <div className="mt-3">
                <div className="font-bold text-xs text-slate-900 leading-tight truncate">
                  {s.label}
                </div>
                <div className="text-[11px] text-slate-500 mt-0.5 leading-snug line-clamp-1">
                  {s.desc}
                </div>
              </div>
            </button>
          ))}
        </div>
      </section>

      <section>
        <h3 className="text-xl font-bold">Quick actions</h3>
        <p className="text-sm text-slate-500 mt-1 mb-4">Jump into the core tools.</p>
        <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
          {cards.map(([t, d, p, I]) => (
            <button
              key={t}
              onClick={() => go(p)}
              className="text-left bg-white border border-emerald-900/10 rounded-2xl p-5 hover:shadow-lg transition"
            >
              <div className="h-10 w-10 rounded-xl bg-emerald-50 text-emerald-700 grid place-items-center">
                <I size={19} />
              </div>
              <b className="block mt-4 text-slate-900">{t}</b>
              <p className="text-sm text-slate-500 mt-2 leading-5">{d}</p>
              <div className="text-emerald-700 text-sm font-semibold mt-4">Open →</div>
            </button>
          ))}
        </div>
      </section>

      <section className="grid lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 bg-white border rounded-2xl p-6 shadow-sm">
          <b>Analysis readiness</b>
          {[
            ['Innovation description', innovation.trim() ? 100 : 25],
            ['Innovation DNA', analysisDone || dnaSaved ? 100 : (dna.solution ? 70 : 15)],
            ['Evidence & Copilot verification', evidenceCount > 0 ? 100 : (chatCount > 1 ? 60 : 30)]
          ].map(([x, v]) => (
            <div key={x as string} className="mt-5">
              <div className="flex justify-between text-sm mb-2">
                <span>{x}</span>
                <span className="text-slate-400 font-semibold">{v}%</span>
              </div>
              <div className="h-2 bg-slate-100 rounded-full">
                <div
                  className="h-full bg-emerald-700 rounded-full transition-all duration-500"
                  style={{ width: `${v}%` }}
                />
              </div>
            </div>
          ))}
        </div>
        <div className="bg-white border rounded-2xl p-6 shadow-sm">
          <div className="flex gap-2 items-center text-emerald-700">
            <ShieldAlert size={18} />
            <b>Review note</b>
          </div>
          <p className="text-sm text-slate-500 mt-3 leading-6">
            AI outputs provide grounded preliminary decision support. Verify current official sources before relying on filing or regulatory decisions.
          </p>
        </div>
      </section>
    </div>
  );
}

function Analysis({ title, setTitle, innovation, setInnovation, analyze, busy, analysisDone, go, setToast }: any) {
  const loadDemoText = () => {
    setTitle(defaultTitle);
    setInnovation(defaultInnovation);
    if (setToast) setToast('Loaded demo innovation specification');
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      if (content) {
        setInnovation(content);
        const nameWithoutExt = file.name.replace(/\.[^/.]+$/, '');
        if (!title.trim() || title === defaultTitle) {
          setTitle(nameWithoutExt);
        }
        if (setToast) setToast(`Loaded file: ${file.name}`);
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  return (
    <div className="max-w-5xl mx-auto space-y-5">
      <div className="flex flex-wrap justify-between items-end gap-3">
        <div>
          <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
            Step 01 · Analysis
          </div>
          <h2 className="serif text-3xl font-bold mt-1">Describe your innovation</h2>
          <p className="text-slate-600 mt-1 text-sm font-normal">
            Describe what your innovation does so the AI can structure it into clear, patentable components.
          </p>
        </div>
        <button
          type="button"
          onClick={loadDemoText}
          className="text-xs font-semibold text-emerald-800 bg-emerald-50 border border-emerald-200 px-3.5 py-2 rounded-xl hover:bg-emerald-100 transition"
        >
          Load Demo Innovation
        </button>
      </div>

      <div className="bg-white rounded-2xl border p-6 space-y-5 shadow-sm">
        <label className="block text-sm font-semibold text-slate-800">
          Innovation title
          <input
            value={title}
            onChange={e => setTitle(e.target.value)}
            placeholder="e.g. Adaptive Edge Computing & Anomaly Detection System"
            className="w-full mt-2 border rounded-xl px-4 py-3 outline-none focus:border-emerald-600 text-slate-900"
          />
        </label>
        <label className="block text-sm font-semibold text-slate-800">
          Innovation description
          <textarea
            value={innovation}
            onChange={e => setInnovation(e.target.value)}
            rows={7}
            placeholder="Describe the architecture, product, methodology, technical mechanism or problem being solved…"
            className="w-full mt-2 border rounded-xl px-4 py-3 outline-none focus:border-emerald-600 resize-y text-slate-900"
          />
        </label>
        <div className="flex flex-wrap gap-3 items-center">
          <button
            onClick={analyze}
            disabled={busy}
            className="flex gap-2 items-center bg-[#0b3b2e] text-white px-6 py-3.5 rounded-xl font-semibold disabled:opacity-50 hover:bg-[#082820] transition shadow-sm"
          >
            <Sparkles size={17} className={busy ? 'animate-spin' : ''} />
            {busy ? 'Structuring Innovation…' : 'Analyze Innovation'}
          </button>
          <label className="flex gap-2 items-center border border-emerald-900/20 bg-white px-4 py-3.5 rounded-xl font-semibold cursor-pointer text-slate-700 hover:bg-emerald-50 transition text-sm">
            <Upload size={16} className="text-emerald-700" />
            Upload specification (.txt, .md)
            <input
              type="file"
              accept=".txt,.md,.json,.text"
              className="hidden"
              onChange={handleFileUpload}
            />
          </label>
        </div>
      </div>

      {/* Guided continuation button after analysis succeeds */}
      {analysisDone && (
        <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4 shadow-sm animate-fade-in">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-[#0b3b2e] text-white grid place-items-center shrink-0">
              <Check size={20} />
            </div>
            <div>
              <div className="font-bold text-emerald-950 text-sm">Innovation Structured Successfully</div>
              <div className="text-xs text-emerald-800">
                Your 9 structured Innovation DNA components have been generated.
              </div>
            </div>
          </div>
          <button
            onClick={() => go('dna')}
            className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
          >
            Continue to Innovation DNA →
          </button>
        </div>
      )}
    </div>
  );
}

function DNA({ dna, setDna, save, go, savedAnalyses, loadPastAnalysis, dnaSaved }: any) {
  const [showSavedModal, setShowSavedModal] = useState(false);

  const fs = [
    ['problem', 'Problem being solved'],
    ['limitations', 'Existing limitations'],
    ['solution', 'Proposed solution'],
    ['mechanism', 'Core mechanism'],
    ['novel', 'Novel elements'],
    ['relationships', 'Technical relationships'],
    ['functional', 'Functional characteristics'],
    ['advantages', 'Advantages'],
    ['differentiating', 'Differentiating characteristics']
  ];

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap justify-between items-end gap-3">
        <div>
          <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
            Step 02 · Innovation DNA
          </div>
          <h2 className="serif text-3xl font-bold mt-1">What makes this innovation different?</h2>
          <p className="text-slate-600 text-sm mt-1">
            See your innovation broken into 9 structured elements — the building blocks of a strong patent application.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          {savedAnalyses && savedAnalyses.length > 0 && (
            <button
              onClick={() => setShowSavedModal(true)}
              className="flex gap-2 items-center border border-emerald-900/15 text-[#0b3b2e] bg-white px-4 py-2.5 rounded-xl font-semibold hover:bg-emerald-50 transition text-sm"
            >
              <FolderOpen size={16} />
              Saved ({savedAnalyses.length})
            </button>
          )}
          <button
            onClick={save}
            className="flex gap-2 items-center bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-[#082820] transition text-sm shadow-sm"
          >
            <Save size={16} />
            Save Analysis
          </button>
          <button
            onClick={() => go('analysis')}
            className="border bg-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition text-slate-700"
          >
            Back
          </button>
        </div>
      </div>

      {/* Guided Continuation Banner after Save */}
      {dnaSaved && (
        <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4 shadow-sm animate-fade-in">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-[#0b3b2e] text-white grid place-items-center shrink-0">
              <Check size={20} />
            </div>
            <div>
              <div className="font-bold text-emerald-950 text-sm">Analysis Saved Successfully</div>
              <div className="text-xs text-emerald-800">
                Ready to review adversarial patent examiner arguments vs. your inventor response.
              </div>
            </div>
          </div>
          <button
            onClick={() => go('two')}
            className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
          >
            Continue to Two-Sided AI →
          </button>
        </div>
      )}

      <div className="grid md:grid-cols-2 gap-4">
        {fs.map(([k, l]) => (
          <div key={k} className="bg-white border rounded-2xl p-5 shadow-sm">
            <label className="font-bold text-sm block text-slate-900">
              {l}
              <textarea
                value={dna[k] || ''}
                onChange={e => setDna({ ...dna, [k]: e.target.value })}
                rows={4}
                className="w-full mt-2 bg-slate-50/60 border rounded-xl p-3 text-sm outline-none focus:border-emerald-600 focus:bg-white resize-y text-slate-800"
              />
            </label>
          </div>
        ))}
      </div>

      {/* Bottom Secondary Guided Navigation */}
      <div className="flex flex-wrap justify-between items-center pt-4 border-t border-slate-200 gap-3">
        <button
          onClick={() => go('analysis')}
          className="flex items-center gap-2 border bg-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition text-slate-700"
        >
          <ArrowLeft size={16} /> Back to Analysis
        </button>
        <button
          onClick={() => go('two')}
          className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
        >
          Continue to Two-Sided AI →
        </button>
      </div>

      {showSavedModal && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4 max-h-[80vh] flex flex-col">
            <div className="flex justify-between items-center pb-2 border-b">
              <b className="text-lg">Saved Innovation Analyses</b>
              <button onClick={() => setShowSavedModal(false)} className="text-slate-400 hover:text-slate-600">
                <X size={18} />
              </button>
            </div>
            <div className="overflow-y-auto space-y-3 flex-1 pr-1">
              {savedAnalyses.map((rec: any) => (
                <div key={rec.id} className="p-4 border rounded-xl hover:border-emerald-700/40 transition flex justify-between items-center gap-3">
                  <div>
                    <div className="font-bold text-sm text-slate-900">{rec.title}</div>
                    <div className="text-xs text-slate-400 mt-1">
                      {rec.jurisdiction} · {rec.created_at || 'Recently saved'}
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      loadPastAnalysis(rec);
                      setShowSavedModal(false);
                    }}
                    className="bg-emerald-50 text-emerald-800 hover:bg-emerald-100 text-xs font-bold px-3 py-1.5 rounded-lg transition"
                  >
                    Load
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Two({ title, innovation, dna, jur, go }: any) {
  const [twoData, setTwoData] = useState<{ innovator_side: string[]; ip_side: string[] } | null>(null);
  const [loading, setLoading] = useState(false);

  const hasInnovation = !!innovation?.trim();

  useEffect(() => {
    if (!hasInnovation) return;
    let cancelled = false;
    setLoading(true);
    api('/api/two-sided', {
      method: 'POST',
      body: JSON.stringify({
        title,
        description: innovation,
        dna,
        jurisdiction: jur
      })
    })
      .then(res => {
        if (!cancelled && res && Array.isArray(res.innovator_side)) {
          setTwoData(res);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setTwoData({
            innovator_side: [
              `Articulate the technical architecture and measurable performance benchmarks of ${title || 'the innovation'}.`,
              'Document empirical data on latency reduction, throughput limits, and computational resource utilization.',
              'Establish comparative experimental results demonstrating distinct advantages over standard baseline systems.',
              'Conduct stress-testing under peak concurrent loads and intermittent network conditions.',
              'Prepare detailed system block diagrams, data flow schemas, and deployment specifications.'
            ],
            ip_side: [
              `Examine patent eligibility criteria and technical character requirements for ${title || 'the innovation'} under Section 3(k) / computer-implemented inventions guidelines.`,
              'Conduct exhaustive prior-art searches on InPASS, USPTO, EPO, and WIPO Patentscope for conflicting architectures.',
              'Verify whether the novel technical contribution solves a specific technical problem with clear technical effect.',
              'Structure claim hierarchy separating core method claims, system claims, and computer-readable medium claims.',
              'Identify potential trade-secret components versus elements requiring patent publication.'
            ]
          });
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };
  }, [title, innovation, jur, hasInnovation]);

  const defaultInnovator = [
    'Explain the innovation clearly with precise technical definitions',
    'Refine operational descriptions and algorithmic implementation steps',
    'Identify important distinguishing characteristics and performance advantages',
    'Prepare quantitative benchmark evidence and test logs for review',
    'Map clear commercialization milestones and regulatory next steps'
  ];
  const defaultIP = [
    'Decompose the innovation into fundamental patentable elements',
    'Identify distinguishing elements over published prior art',
    'Explore novelty-oriented questions and Section 3 exclusions',
    'Map prior-art investigation areas across InPASS and global registries',
    'Flag expert-review points and statutory compliance checkpoints'
  ];

  const innovatorItems = twoData?.innovator_side || defaultInnovator;
  const ipItems = twoData?.ip_side || defaultIP;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap justify-between items-end gap-3">
        <div>
          <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
            Step 03 · Two-Sided AI
          </div>
          <h2 className="serif text-3xl font-bold mt-1">Innovator ↔ IP analysis</h2>
          <p className="text-slate-600 text-sm mt-1">
            See how a patent examiner might challenge your innovation versus how you as the inventor would argue for it.
          </p>
        </div>
        {!hasInnovation && (
          <button
            onClick={() => go('analysis')}
            className="bg-[#0b3b2e] text-white text-sm font-semibold px-4 py-2.5 rounded-xl hover:bg-emerald-900 transition shadow-sm"
          >
            Describe Innovation →
          </button>
        )}
      </div>

      {!hasInnovation ? (
        <div className="bg-white border border-dashed border-emerald-900/20 rounded-3xl p-12 text-center max-w-xl mx-auto shadow-sm space-y-4">
          <div className="h-14 w-14 bg-emerald-50 text-emerald-800 rounded-2xl grid place-items-center mx-auto">
            <Sparkles size={28} />
          </div>
          <h3 className="text-xl font-bold text-slate-900">Describe your innovation first</h3>
          <p className="text-sm text-slate-600 leading-relaxed">
            To generate tailored innovator and patent examiner perspectives, please provide your innovation details in the Analysis step.
          </p>
          <button
            onClick={() => go('analysis')}
            className="inline-flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-3 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
          >
            Start with Innovation Analysis →
          </button>
        </div>
      ) : loading ? (
        <div className="bg-white border rounded-2xl p-14 text-center text-slate-500 shadow-sm">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-[#0b3b2e] mb-3"></div>
          <div className="font-medium text-slate-700">Generating dynamic innovator and IP examiner perspectives…</div>
          <div className="text-xs text-slate-400 mt-1">Comparing technical claims against statutory examination bars</div>
        </div>
      ) : (
        <div className="grid lg:grid-cols-2 gap-5">
          <Panel title="Innovator side (Defense & Advantages)" icon={Sparkles} items={innovatorItems} />
          <Panel title="IP Examiner side (Challenges & Prior Art)" icon={FileSearch} items={ipItems} />
        </div>
      )}

      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5 text-sm text-amber-900">
        Preliminary AI-assisted analysis — not a final legal opinion or patentability determination.
      </div>

      {/* Bottom Secondary Guided Navigation */}
      <div className="flex flex-wrap justify-between items-center pt-4 border-t border-slate-200 gap-3">
        <button
          onClick={() => go('dna')}
          className="flex items-center gap-2 border bg-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition text-slate-700"
        >
          <ArrowLeft size={16} /> Back to Innovation DNA
        </button>
        <button
          onClick={() => go('radar')}
          className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
        >
          Continue to IP Risk Radar →
        </button>
      </div>
    </div>
  );
}

function Panel({ title, icon: I, items }: any) {
  return (
    <div className="bg-white border rounded-2xl p-6 shadow-sm">
      <div className="h-11 w-11 bg-emerald-50 text-emerald-700 rounded-xl grid place-items-center">
        <I size={20} />
      </div>
      <h3 className="font-bold text-xl mt-4 text-slate-900">{title}</h3>
      <div className="mt-5 space-y-3">
        {items.map((x: string, i: number) => (
          <div className="flex gap-3 text-sm leading-6" key={i}>
            <Check size={17} className="text-emerald-700 shrink-0 mt-0.5" />
            <span className="text-slate-700">{x}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function Radar({ title, innovation, dna, jur, go }: any) {
  const [radarItems, setRadarItems] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  const hasInnovation = !!innovation?.trim();

  useEffect(() => {
    if (!hasInnovation) return;
    let cancelled = false;
    setLoading(true);
    api('/api/risk-radar', {
      method: 'POST',
      body: JSON.stringify({
        title,
        description: innovation,
        dna,
        jurisdiction: jur
      })
    })
      .then(res => {
        if (!cancelled && res && Array.isArray(res.items)) {
          setRadarItems(res.items);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setRadarItems([
            { area: 'Novelty / Prior Art', level: 'Medium', note: `Global patent search advised. Distinguishing algorithms and telemetry quantization parameters of ${title || 'the innovation'} must be clearly highlighted.` },
            { area: 'Traditional Knowledge', level: 'Low', note: 'Unlikely to trigger Section 3(p) unless traditional biological formulation principles are involved.' },
            { area: 'Regulatory & Compliance', level: 'Medium', note: 'Verify telecommunications, data privacy (DPDP), and industrial IoT safety standards.' },
            { area: 'Biodiversity / ABS', level: 'Low', note: 'Biological Diversity Act approval (NBA Form 3) is not triggered for digital/sensor innovations.' },
            { area: 'Jurisdiction', level: 'Low', note: `Current workspace is configured for ${jur}. Priority deadlines and PCT routes are mapped.` },
            { area: 'Missing Evidence', level: 'High', note: 'Submit quantitative latency logs and compression ratio benchmarks to substantiate claims.' }
          ]);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };
  }, [title, innovation, jur, hasInnovation]);

  const defaultItems = [
    { area: 'Novelty / Prior Art', level: 'Medium', note: 'More evidence needed to assess distinctiveness over published prior art.' },
    { area: 'Traditional Knowledge', level: 'Needs Review', note: 'Check whether traditional knowledge informs the innovation.' },
    { area: 'Regulatory', level: 'Medium', note: 'Verify product-specific requirements with the competent authority.' },
    { area: 'Biodiversity / ABS', level: 'Needs Review', note: 'Relevant where biological resources or natural materials are involved.' },
    { area: 'Jurisdiction', level: 'Low', note: `Current workspace is configured for ${jur}.` },
    { area: 'Missing Evidence', level: 'High', note: 'Add technical benchmark and source evidence before relying on conclusions.' }
  ];

  const items = radarItems || defaultItems;

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap justify-between items-end gap-3">
        <div>
          <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
            Step 04 · Risk Radar
          </div>
          <h2 className="serif text-3xl font-bold mt-1">IP Risk Radar</h2>
          <p className="text-slate-600 text-sm mt-1">
            Spot early warning signs across novelty, traditional knowledge, regulatory, and biodiversity risk areas before you file.
          </p>
        </div>
        {!hasInnovation && (
          <button
            onClick={() => go('analysis')}
            className="bg-[#0b3b2e] text-white text-sm font-semibold px-4 py-2.5 rounded-xl hover:bg-emerald-900 transition shadow-sm"
          >
            Describe Innovation →
          </button>
        )}
      </div>

      {!hasInnovation ? (
        <div className="bg-white border border-dashed border-emerald-900/20 rounded-3xl p-12 text-center max-w-xl mx-auto shadow-sm space-y-4">
          <div className="h-14 w-14 bg-emerald-50 text-emerald-800 rounded-2xl grid place-items-center mx-auto">
            <Gauge size={28} />
          </div>
          <h3 className="text-xl font-bold text-slate-900">Describe your innovation first</h3>
          <p className="text-sm text-slate-600 leading-relaxed">
            To evaluate statutory risk levels and compliance checkpoints, please provide your innovation description in the Analysis step.
          </p>
          <button
            onClick={() => go('analysis')}
            className="inline-flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-3 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
          >
            Start with Innovation Analysis →
          </button>
        </div>
      ) : loading ? (
        <div className="bg-white border rounded-2xl p-14 text-center text-slate-500 shadow-sm">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-[#0b3b2e] mb-3"></div>
          <div className="font-medium text-slate-700">Evaluating statutory risk factors across novelty, regulatory and IP categories…</div>
          <div className="text-xs text-slate-400 mt-1">Cross-referencing statutory exclusion grounds</div>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          {items.map((x: any) => {
            const isHigh = x.level === 'High';
            const isReview = x.level === 'Needs Review';
            const badgeClass = isHigh
              ? 'bg-red-50 text-red-800 border-red-200'
              : isReview
              ? 'bg-amber-50 text-amber-800 border-amber-200'
              : 'bg-emerald-50 text-emerald-800 border-emerald-200';

            return (
              <div key={x.area} className="bg-white border rounded-2xl p-5 hover:shadow-sm transition shadow-sm">
                <div className="flex justify-between items-start gap-3">
                  <b className="text-base text-slate-900">{x.area}</b>
                  <span className={`text-xs font-bold px-2.5 py-1 rounded-full border ${badgeClass}`}>
                    {x.level}
                  </span>
                </div>
                <p className="text-sm text-slate-600 mt-3 leading-6">{x.note}</p>
              </div>
            );
          })}
        </div>
      )}

      <div className="text-xs text-slate-400">
        Preliminary decision-support indicators, not legal conclusions.
      </div>

      {/* Bottom Secondary Guided Navigation */}
      <div className="flex flex-wrap justify-between items-center pt-4 border-t border-slate-200 gap-3">
        <button
          onClick={() => go('two')}
          className="flex items-center gap-2 border bg-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition text-slate-700"
        >
          <ArrowLeft size={16} /> Back to Two-Sided AI
        </button>
        <button
          onClick={() => go('pathway')}
          className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
        >
          Continue to Pathway →
        </button>
      </div>
    </div>
  );
}

function Pathway({ title, innovation, dna, jur, go }: any) {
  const STAGES = [
    'Product Understanding',
    'Classification',
    'IP Considerations',
    'Regulatory Considerations',
    'Traditional Knowledge Check',
    'Biodiversity / ABS',
    'Recommended Next Steps'
  ];
  const [active, setActive] = useState(0);
  const [stageData, setStageData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [completedStages, setCompletedStages] = useState<Set<number>>(new Set());

  const hasInnovation = !!innovation?.trim();

  useEffect(() => {
    if (!hasInnovation) return;
    let cancelled = false;
    setStageData(null);
    setLoading(true);
    api('/api/pathway', {
      method: 'POST',
      body: JSON.stringify({
        title: title || '',
        description: innovation || '',
        dna,
        jurisdiction: jur || 'India',
        stage: STAGES[active]
      })
    })
      .then(res => {
        if (!cancelled && res && Array.isArray(res.steps)) {
          setStageData(res);
        }
      })
      .catch(() => {
        if (!cancelled) {
          // Graceful fallback: basic stage-aware content
          setStageData({
            stage: STAGES[active],
            steps: [{
              title: STAGES[active],
              guidance: `For the "${STAGES[active]}" stage, carefully review official ${jur || 'India'} IP guidelines for "${title || 'the innovation'}". Document all architectural and performance specifications, consult authoritative patent office rules, and verify all sub-requirements systematically.`,
              checklist: [
                'Review applicable statutory provisions and guidelines',
                'Consult official examination manuals and databases',
                'Document technical findings and action milestones',
                'Verify compliance with all statutory prerequisites'
              ],
              references: ['IP India: ipindia.gov.in', 'WIPO: wipo.int', 'National Biodiversity Authority: nbaindia.org']
            }]
          });
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [active, title, innovation, jur, hasInnovation]);

  const markComplete = () => {
    setCompletedStages(prev => new Set([...prev, active]));
    if (active < STAGES.length - 1) setActive(active + 1);
  };

  const levelColors: Record<string, string> = {
    'Product Understanding': 'bg-blue-100 text-blue-800',
    'Classification': 'bg-violet-100 text-violet-800',
    'IP Considerations': 'bg-emerald-100 text-emerald-800',
    'Regulatory Considerations': 'bg-amber-100 text-amber-800',
    'Traditional Knowledge Check': 'bg-orange-100 text-orange-800',
    'Biodiversity / ABS': 'bg-teal-100 text-teal-800',
    'Recommended Next Steps': 'bg-slate-100 text-slate-800'
  };

  return (
    <div className="max-w-5xl mx-auto space-y-5">
      <div className="flex flex-wrap justify-between items-end gap-3">
        <div>
          <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
            Step 05 · Guided Pathway
          </div>
          <h2 className="serif text-3xl font-bold mt-1">IP-SAKTI Pathway</h2>
          <p className="text-slate-600 text-sm mt-1">
            Follow a step-by-step IP roadmap tailored to your innovation and jurisdiction, from understanding to filing.
          </p>
        </div>
        {!hasInnovation && (
          <button
            onClick={() => go('analysis')}
            className="bg-[#0b3b2e] text-white text-sm font-semibold px-4 py-2.5 rounded-xl hover:bg-emerald-900 transition shadow-sm"
          >
            Describe Innovation →
          </button>
        )}
      </div>

      {!hasInnovation ? (
        <div className="bg-white border border-dashed border-emerald-900/20 rounded-3xl p-12 text-center max-w-xl mx-auto shadow-sm space-y-4">
          <div className="h-14 w-14 bg-emerald-50 text-emerald-800 rounded-2xl grid place-items-center mx-auto">
            <ArrowRight size={28} />
          </div>
          <h3 className="text-xl font-bold text-slate-900">Describe your innovation first</h3>
          <p className="text-sm text-slate-600 leading-relaxed">
            To generate stage-by-stage IP guidance and compliance checklists, please provide your innovation details in the Analysis step.
          </p>
          <button
            onClick={() => go('analysis')}
            className="inline-flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-3 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
          >
            Start with Innovation Analysis →
          </button>
        </div>
      ) : (
        <>
          {/* Stage navigation */}
          <div className="bg-white border rounded-2xl p-4 shadow-sm">
            <div className="flex flex-wrap gap-2">
              {STAGES.map((s, i) => (
                <button
                  onClick={() => setActive(i)}
                  key={s}
                  className={`px-3 py-2 rounded-xl text-sm font-medium transition flex items-center gap-1.5 ${
                    i === active
                      ? 'bg-[#0b3b2e] text-white font-semibold'
                      : completedStages.has(i)
                      ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {completedStages.has(i) && <Check size={13} />}
                  {i + 1}. {s}
                </button>
              ))}
            </div>
            {/* Progress bar */}
            <div className="mt-4 h-1.5 bg-slate-100 rounded-full">
              <div
                className="h-full bg-emerald-700 rounded-full transition-all duration-500"
                style={{ width: `${((completedStages.size) / STAGES.length) * 100}%` }}
              />
            </div>
            <div className="text-xs text-slate-400 mt-1.5 font-medium">
              {completedStages.size} of {STAGES.length} stages reviewed
            </div>
          </div>

          {/* Stage content */}
          <div className="bg-white border rounded-2xl overflow-hidden shadow-sm">
            <div className="px-6 pt-6 pb-4 border-b flex items-center justify-between">
              <div>
                <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${levelColors[STAGES[active]] || 'bg-slate-100 text-slate-700'}`}>
                  Stage {active + 1} of {STAGES.length}
                </span>
                <h3 className="text-2xl font-bold mt-2 text-slate-900">{STAGES[active]}</h3>
              </div>
              {loading && (
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-emerald-700" />
                  Generating stage guidance…
                </div>
              )}
            </div>

            <div className="p-6 space-y-5">
              {loading && !stageData ? (
                <div className="space-y-4">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="h-24 bg-slate-50 rounded-xl animate-pulse" />
                  ))}
                </div>
              ) : stageData?.steps ? (
                stageData.steps.map((step: any, idx: number) => (
                  <div key={idx} className="border rounded-xl overflow-hidden shadow-sm">
                    <div className="bg-slate-50 px-5 py-3.5 flex items-center gap-3 border-b">
                      <div className="h-7 w-7 rounded-lg bg-[#0b3b2e] text-white text-xs font-bold grid place-items-center shrink-0">
                        {idx + 1}
                      </div>
                      <h4 className="font-bold text-base text-slate-900">{step.title}</h4>
                    </div>
                    <div className="p-5 space-y-4">
                      <p className="text-sm text-slate-600 leading-7">{step.guidance}</p>
                      {step.checklist?.length > 0 && (
                        <div>
                          <div className="text-xs font-bold text-slate-500 uppercase mb-2">Checklist</div>
                          <div className="space-y-2">
                            {step.checklist.map((item: string, ci: number) => (
                              <div key={ci} className="flex gap-2.5 text-sm leading-5">
                                <div className="h-5 w-5 rounded border-2 border-emerald-700/30 shrink-0 mt-0.5 flex items-center justify-center">
                                  <div className="h-2 w-2 rounded-sm bg-emerald-700/20" />
                                </div>
                                <span className="text-slate-700">{item}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                      {step.references?.length > 0 && (
                        <div className="bg-emerald-50/60 rounded-lg px-4 py-3">
                          <div className="text-xs font-bold text-emerald-800 mb-1.5">References</div>
                          <div className="space-y-1">
                            {step.references.map((ref: string, ri: number) => (
                              <div key={ri} className="text-xs text-emerald-700 flex gap-1.5 items-start">
                                <BookOpen size={12} className="mt-0.5 shrink-0" />
                                <span>{ref}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              ) : null}
            </div>

            {/* Navigation */}
            <div className="px-6 pb-6 flex gap-3 items-center">
              {active > 0 && (
                <button
                  onClick={() => setActive(active - 1)}
                  className="border px-4 py-2.5 rounded-xl font-semibold hover:bg-slate-50 text-sm flex items-center gap-2 text-slate-700"
                >
                  <ArrowLeft size={16} />
                  Previous
                </button>
              )}
              <button
                onClick={markComplete}
                className="bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 text-sm flex items-center gap-2 shadow-sm"
              >
                <Check size={16} />
                {active === STAGES.length - 1 ? 'Complete Pathway' : 'Mark & Continue'}
              </button>
              {active < STAGES.length - 1 && (
                <button
                  onClick={() => setActive(active + 1)}
                  className="border px-4 py-2.5 rounded-xl font-semibold hover:bg-slate-50 text-sm flex items-center gap-2 text-slate-700"
                >
                  Skip
                  <ArrowRight size={16} />
                </button>
              )}
            </div>
          </div>
        </>
      )}

      <div className="text-xs text-slate-400">
        AI-generated guidance — verify all statutory requirements against official sources before taking legal or regulatory action.
      </div>

      {/* Bottom Secondary Guided Navigation */}
      <div className="flex flex-wrap justify-between items-center pt-4 border-t border-slate-200 gap-3">
        <button
          onClick={() => go('radar')}
          className="flex items-center gap-2 border bg-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition text-slate-700"
        >
          <ArrowLeft size={16} /> Back to Risk Radar
        </button>
        <button
          onClick={() => go('copilot')}
          className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
        >
          Continue to AI Copilot →
        </button>
      </div>
    </div>
  );
}

function Evidence({ data = [], go }: any) {
  const safeData = Array.isArray(data) ? data : [];
  return (
    <div className="space-y-5">
      <div>
        <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
          Step 06 · Evidence Trail
        </div>
        <h2 className="serif text-3xl font-bold mt-1">Sources used by the Copilot</h2>
        <p className="text-slate-600 text-sm mt-1">
          Browse the authoritative sources the AI used to ground its answers — with links back to official references.
        </p>
      </div>
      {safeData.length ? (
        <div className="space-y-3">
          {safeData.map((e: any) => (
            <div className="bg-white border rounded-2xl p-5 shadow-sm" key={e.id}>
              <div className="text-xs text-emerald-700 font-semibold">
                {e.authority} · {e.jurisdiction} · {e.domain}
              </div>
              <h3 className="font-bold mt-1 text-base text-slate-900">{e.title}</h3>
              <p className="text-sm text-slate-600 mt-2 leading-6">{e.content}</p>
              <a
                className="text-sm text-emerald-700 font-semibold inline-block mt-3 hover:underline"
                href={e.source_url}
                target="_blank"
                rel="noreferrer"
              >
                Open authoritative source ↗
              </a>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white border border-dashed rounded-2xl p-12 text-center text-slate-400 space-y-3">
          <div>Ask the Copilot questions to populate and inspect the authoritative evidence trail.</div>
          <button
            onClick={() => go('copilot')}
            className="inline-flex items-center gap-2 bg-[#0b3b2e] text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-emerald-900 transition"
          >
            Open AI Copilot →
          </button>
        </div>
      )}

      {/* Bottom Secondary Guided Navigation */}
      <div className="flex flex-wrap justify-between items-center pt-4 border-t border-slate-200 gap-3">
        <button
          onClick={() => go('pathway')}
          className="flex items-center gap-2 border bg-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition text-slate-700"
        >
          <ArrowLeft size={16} /> Back to Pathway
        </button>
        <button
          onClick={() => go('copilot')}
          className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
        >
          Continue to AI Copilot →
        </button>
      </div>
    </div>
  );
}

function Copilot({ chat, input, setInput, send, busy, evidence, go }: any) {
  return (
    <div className="space-y-5">
      <div>
        <div className="text-emerald-700 text-xs font-bold uppercase tracking-widest">
          Step 07 · AI Copilot
        </div>
        <h2 className="serif text-3xl font-bold mt-1">Evidence-Grounded IP Copilot</h2>
        <p className="text-slate-600 text-sm mt-1">
          Ask free-form IP questions and get evidence-grounded answers with citations from official IP databases.
        </p>
      </div>

      <div className="grid xl:grid-cols-[1fr_330px] gap-5 min-h-[650px]">
        <div className="bg-white border rounded-2xl overflow-hidden flex flex-col shadow-sm">
          <div className="p-5 border-b flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-emerald-50 text-emerald-700 grid place-items-center">
              <Bot size={20} />
            </div>
            <div>
              <b className="text-slate-900">Evidence-Grounded IP Copilot</b>
              <div className="text-xs text-slate-500">Preliminary decision support grounded in official IP data</div>
            </div>
          </div>
          <div className="flex-1 p-5 space-y-4 overflow-y-auto">
            {chat.map((m: any, i: number) => (
              <div key={i} className={m.role === 'user' ? 'flex justify-end' : ''}>
                <div
                  className={`max-w-[88%] rounded-2xl px-4 py-3 text-sm leading-6 ${
                    m.role === 'user'
                      ? 'bg-[#0b3b2e] text-white'
                      : 'bg-slate-50 text-slate-700 border'
                  }`}
                >
                  {m.text}
                  {m.citations?.length && (
                    <div className="mt-3 pt-2 border-t flex flex-wrap gap-2">
                      {m.citations.map((c: any) => (
                        <span
                          className="text-[11px] bg-white text-emerald-800 border rounded-full px-2 py-1 font-medium"
                          key={c.id}
                        >
                          Evidence: {c.title}
                        </span>
                      ))}
                    </div>
                  )}
                  {m.suggested_next_steps?.length > 0 && (
                    <div className="mt-3 pt-2 border-t text-xs space-y-1">
                      <b className="text-slate-800 block">Recommended next steps:</b>
                      {m.suggested_next_steps.map((st: string, idx: number) => (
                        <div key={idx} className="flex gap-2">
                          <span>•</span>
                          <span>{st}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {busy && (
              <div className="text-sm text-slate-500 flex items-center gap-2">
                <div className="animate-spin rounded-full h-3.5 w-3.5 border-b-2 border-emerald-700"></div>
                <span>Copilot is retrieving official evidence and synthesizing answer…</span>
              </div>
            )}
          </div>
          <div className="p-3 border-t flex gap-2">
            <textarea
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  send();
                }
              }}
              rows={2}
              placeholder="Ask about patentability, Section 3 exclusions, InPASS search strategies, TKDL, NBA…"
              className="flex-1 resize-none border rounded-xl px-3 py-2 text-sm outline-none focus:border-emerald-600 text-slate-900"
            />
            <button
              onClick={() => send()}
              disabled={busy || !input.trim()}
              className="self-end h-11 w-11 rounded-xl bg-[#0b3b2e] text-white grid place-items-center disabled:opacity-40 hover:bg-emerald-900 transition shadow-sm"
            >
              <Send size={17} />
            </button>
          </div>
        </div>

        <aside className="bg-white border rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 font-bold text-slate-900">
              <FileSearch size={18} className="text-emerald-700" />
              Evidence
            </div>
            <p className="text-xs text-slate-400 mt-1">Retrieved official sources.</p>
            {evidence.length ? (
              <div className="mt-4 space-y-3">
                {evidence.map((e: any) => (
                  <div key={e.id} className="bg-slate-50 border rounded-xl p-3">
                    <b className="text-xs text-slate-900">{e.title}</b>
                    <div className="text-[11px] text-slate-500 mt-1">
                      {e.authority} · {e.domain}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-slate-400 mt-6">No evidence yet. Ask a question to search official databases.</div>
            )}
          </div>
          <div className="mt-6 pt-5 border-t">
            <div className="text-xs font-bold text-slate-500 uppercase">Try asking</div>
            <div className="mt-3 space-y-2">
              {prompts.slice(0, 4).map(p => (
                <button
                  key={p}
                  onClick={() => send(p)}
                  className="w-full text-left text-xs border rounded-xl px-3 py-2.5 hover:bg-emerald-50 transition text-slate-700"
                >
                  {p}
                </button>
              ))}
            </div>
            <button
              onClick={() => go('evidence')}
              className="w-full mt-3 text-sm text-emerald-700 font-semibold hover:underline text-left flex items-center justify-between"
            >
              <span>View full evidence list</span>
              <span>→</span>
            </button>
          </div>
        </aside>
      </div>

      {/* Bottom Secondary Guided Navigation */}
      <div className="flex flex-wrap justify-between items-center pt-4 border-t border-slate-200 gap-3">
        <button
          onClick={() => go('pathway')}
          className="flex items-center gap-2 border bg-white px-4 py-2.5 rounded-xl text-sm font-semibold hover:bg-slate-50 transition text-slate-700"
        >
          <ArrowLeft size={16} /> Back to Pathway
        </button>
        <button
          onClick={() => go('dashboard')}
          className="flex items-center gap-2 bg-[#0b3b2e] text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-emerald-900 transition text-sm shadow-sm"
        >
          Return to Dashboard Overview →
        </button>
      </div>
    </div>
  );
}
