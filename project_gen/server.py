"""
server.py – Flask web server that serves the browser UI and a REST API.

Endpoints:
  GET  /                    → Web UI (HTML)
  POST /api/generate        → Generate + download ZIP
  GET  /api/stacks          → List all stacks
  GET  /api/preview         → Preview file tree for given options
"""

import io
import json
import traceback
from flask import Flask, request, jsonify, send_file, render_template_string

from project_gen.stacks import (
    STACK_META,
    resolve_stack,
)
from project_gen.generator import generate_project_to_zip

# Re-export lists from prompts without importing questionary in this context
PLATFORMS_LIST = ["Web", "Desktop", "Hybrid"]
CATEGORIES_LIST = [
    "E-commerce", "SaaS product", "Business dashboard", "Blogging platform",
    "AI chatbot interface", "Streaming platform", "Social media app",
    "Video conferencing", "Cryptocurrency tracker", "Gaming hub",
    "Ticketing system", "Learning management system", "Healthcare management",
    "Event management", "Travel booking", "Restaurant ordering system",
    "Finance tracker", "Inventory management", "Portfolio site", "Music player",
]
STYLES_LIST = ["Modern", "Minimal", "Dark Theme", "Corporate", "Playful", "Elegant"]
SCOPES_LIST = ["Scalable app", "Landing page", "Static-only"]

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# HTML UI (single-file, self-contained)
# ─────────────────────────────────────────────────────────────

WEB_UI = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>🚀 Project Generator</title>
<style>
  :root {
    --bg: #0a0a0f;
    --surface: #13131a;
    --surface2: #1c1c28;
    --border: #2a2a3a;
    --primary: #6366f1;
    --primary-glow: rgba(99,102,241,0.25);
    --green: #10b981;
    --text: #e2e8f0;
    --muted: #64748b;
    --radius: 14px;
    --font: 'Inter', system-ui, sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* ── Header ── */
  header {
    border-bottom: 1px solid var(--border);
    padding: 20px 32px;
    display: flex;
    align-items: center;
    gap: 16px;
    background: var(--surface);
    backdrop-filter: blur(10px);
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .logo { font-size: 1.4rem; font-weight: 900; color: #fff; letter-spacing: -0.03em; }
  .logo span { color: var(--primary); }
  .badge {
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    background: var(--primary-glow);
    color: var(--primary);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 20px;
  }

  /* ── Layout ── */
  .container {
    max-width: 960px;
    margin: 0 auto;
    padding: 48px 24px 80px;
    width: 100%;
  }

  .page-title {
    font-size: 2.5rem;
    font-weight: 900;
    color: #fff;
    letter-spacing: -0.04em;
    margin-bottom: 8px;
    line-height: 1.1;
  }
  .page-sub {
    color: var(--muted);
    font-size: 1.05rem;
    margin-bottom: 40px;
  }

  /* ── Steps ── */
  .steps {
    display: flex;
    gap: 8px;
    margin-bottom: 40px;
    flex-wrap: wrap;
  }
  .step-dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700;
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--muted);
    cursor: pointer;
    transition: all 0.2s;
  }
  .step-dot.active { background: var(--primary); border-color: var(--primary); color: #fff; }
  .step-dot.done { background: var(--green); border-color: var(--green); color: #fff; }

  /* ── Card ── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px;
    margin-bottom: 20px;
  }
  .card-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 16px;
  }

  /* ── Option Grid ── */
  .option-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 10px;
  }
  .option-btn {
    padding: 12px 14px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--surface2);
    color: var(--text);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    text-align: left;
    line-height: 1.4;
  }
  .option-btn:hover { border-color: var(--primary); background: var(--primary-glow); }
  .option-btn.selected {
    border-color: var(--primary);
    background: var(--primary-glow);
    color: #fff;
    box-shadow: 0 0 0 1px var(--primary);
  }
  .option-btn .icon { display: block; font-size: 1.3rem; margin-bottom: 6px; }

  /* ── Text Input ── */
  .text-input {
    width: 100%;
    padding: 12px 16px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--surface2);
    color: var(--text);
    font-size: 0.9rem;
    font-family: var(--font);
    transition: border-color 0.15s;
    outline: none;
  }
  .text-input:focus { border-color: var(--primary); }
  .text-input::placeholder { color: var(--muted); }

  /* ── Stack Preview ── */
  .stack-preview {
    display: none;
    margin-top: 16px;
    padding: 14px 18px;
    border-radius: 10px;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    font-size: 0.85rem;
  }
  .stack-preview.visible { display: block; }
  .stack-label { color: var(--green); font-weight: 700; margin-bottom: 6px; }
  .stack-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
  .stack-tag {
    padding: 3px 10px;
    border-radius: 20px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.25);
    color: var(--green);
    font-size: 11px;
    font-weight: 600;
  }

  /* ── Color Picker ── */
  .color-row { display: flex; gap: 12px; align-items: center; }
  .color-swatch {
    width: 42px; height: 42px;
    border-radius: 10px;
    border: 2px solid var(--border);
    cursor: pointer;
    flex-shrink: 0;
    transition: transform 0.15s;
  }
  .color-swatch:hover { transform: scale(1.05); }

  /* ── Action buttons ── */
  .btn-primary {
    padding: 14px 32px;
    border-radius: 12px;
    background: var(--primary);
    color: #fff;
    border: none;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.15s;
    display: inline-flex; align-items: center; gap: 8px;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35);
  }
  .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(99,102,241,0.45); }
  .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

  .btn-secondary {
    padding: 14px 24px;
    border-radius: 12px;
    background: var(--surface2);
    color: var(--text);
    border: 1px solid var(--border);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
  }
  .btn-secondary:hover { border-color: var(--primary); }

  /* ── Progress / Download ── */
  .progress-wrap {
    display: none;
    text-align: center;
    padding: 40px;
  }
  .spinner {
    width: 48px; height: 48px;
    border: 3px solid var(--border);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .success-wrap {
    display: none;
    text-align: center;
    padding: 40px 20px;
  }
  .success-icon { font-size: 3.5rem; margin-bottom: 16px; }
  .success-title { font-size: 1.6rem; font-weight: 800; color: var(--green); margin-bottom: 8px; }
  .success-sub { color: var(--muted); margin-bottom: 28px; font-size: 0.95rem; }

  /* ── Next steps ── */
  .next-steps {
    text-align: left;
    background: var(--surface2);
    border-radius: 12px;
    padding: 20px 24px;
    max-width: 500px;
    margin: 0 auto;
  }
  .next-steps-title { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); font-weight: 700; margin-bottom: 12px; }
  .step-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 7px 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
  }
  .step-item:last-child { border-bottom: none; }
  .step-num {
    width: 20px; height: 20px;
    border-radius: 50%;
    background: var(--primary);
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
  }
  .step-cmd {
    font-family: 'Fira Code', 'Courier New', monospace;
    color: var(--text);
    word-break: break-all;
  }
  .step-hint { color: var(--muted); font-size: 0.8rem; margin-top: 2px; }

  /* ── cURL box ── */
  .curl-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    overflow-x: auto;
    white-space: pre;
    margin-top: 16px;
  }
  .curl-box .hl { color: var(--green); }

  /* ── Divider ── */
  .divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 32px 0;
  }

  /* ── cURL section ── */
  .section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #fff;
    margin-bottom: 8px;
  }
  .section-sub { color: var(--muted); font-size: 0.9rem; margin-bottom: 16px; }

  /* ── Responsive ── */
  @media (max-width: 600px) {
    .page-title { font-size: 1.8rem; }
    .option-grid { grid-template-columns: repeat(2, 1fr); }
  }
</style>
</head>
<body>

<header>
  <div class="logo">Project<span>Gen</span></div>
  <div class="badge">v2.0</div>
</header>

<div class="container">
  <h1 class="page-title">Full-stack scaffolding<br>in seconds.</h1>
  <p class="page-sub">Pick your stack. Download. Only edit <code style="color:#6366f1">.env</code>. Start building.</p>

  <!-- ── Step 1: Platform ── -->
  <div class="card" id="card-platform">
    <div class="card-title">Step 1 – Platform</div>
    <div class="option-grid" id="platform-grid">
      <button class="option-btn" onclick="select('platform','Web',this)"><span class="icon">🌐</span>Web</button>
      <button class="option-btn" onclick="select('platform','Desktop',this)"><span class="icon">🖥️</span>Desktop</button>
      <button class="option-btn" onclick="select('platform','Hybrid',this)"><span class="icon">⚡</span>Hybrid</button>
    </div>
  </div>

  <!-- ── Step 2: Category ── -->
  <div class="card" id="card-category">
    <div class="card-title">Step 2 – Project Category</div>
    <div class="option-grid" id="category-grid">
""" + "".join(
    f'      <button class="option-btn" onclick="select(\'category\',\'{c}\',this)">{c}</button>\n'
    for c in CATEGORIES_LIST
) + """    </div>

    <div class="stack-preview" id="stack-preview">
      <div class="stack-label" id="stack-label">–</div>
      <div id="stack-desc" style="color:#94a3b8;font-size:0.82rem;"></div>
      <div class="stack-tags" id="stack-tags"></div>
    </div>
  </div>

  <!-- ── Step 3: Design ── -->
  <div class="card">
    <div class="card-title">Step 3 – Design</div>

    <p style="font-size:0.8rem;color:var(--muted);margin-bottom:8px;">Primary brand color</p>
    <div class="color-row">
      <input type="color" id="color-picker" class="color-swatch" value="#6366f1" oninput="updateColor(this.value)" />
      <input type="text" id="color-text" class="text-input" style="width:160px" value="#6366f1" oninput="syncColorFromText(this.value)" />
      <div style="display:flex;gap:6px;flex-wrap:wrap;">
        <div id="p1" class="color-swatch" style="background:#6366f1;width:32px;height:32px;" onclick="applyPreset('#6366f1')" title="#6366f1"></div>
        <div id="p2" class="color-swatch" style="background:#10b981;width:32px;height:32px;" onclick="applyPreset('#10b981')" title="#10b981"></div>
        <div id="p3" class="color-swatch" style="background:#f59e0b;width:32px;height:32px;" onclick="applyPreset('#f59e0b')" title="#f59e0b"></div>
        <div id="p4" class="color-swatch" style="background:#ef4444;width:32px;height:32px;" onclick="applyPreset('#ef4444')" title="#ef4444"></div>
        <div id="p5" class="color-swatch" style="background:#8b5cf6;width:32px;height:32px;" onclick="applyPreset('#8b5cf6')" title="#8b5cf6"></div>
        <div id="p6" class="color-swatch" style="background:#ec4899;width:32px;height:32px;" onclick="applyPreset('#ec4899')" title="#ec4899"></div>
        <div id="p7" class="color-swatch" style="background:#0ea5e9;width:32px;height:32px;" onclick="applyPreset('#0ea5e9')" title="#0ea5e9"></div>
      </div>
    </div>

    <div style="margin-top:20px;">
      <p style="font-size:0.8rem;color:var(--muted);margin-bottom:8px;">Design style</p>
      <div class="option-grid" id="style-grid">
""" + "".join(
    f'        <button class="option-btn" onclick="select(\'style\',\'{s}\',this)">{s}</button>\n'
    for s in STYLES_LIST
) + """      </div>
    </div>
  </div>

  <!-- ── Step 4: Scope + Name ── -->
  <div class="card">
    <div class="card-title">Step 4 – Scope &amp; Name</div>
    <div class="option-grid" id="scope-grid" style="margin-bottom:20px;">
""" + "".join(
    f'      <button class="option-btn" onclick="select(\'scope\',\'{s}\',this)">{s}</button>\n'
    for s in SCOPES_LIST
) + """    </div>
    <p style="font-size:0.8rem;color:var(--muted);margin-bottom:8px;">Project name (used as the folder &amp; ZIP name)</p>
    <input type="text" id="project-name" class="text-input" placeholder="my-awesome-app" value="my-project" style="max-width:320px" />
  </div>

  <!-- ── Generate Button ── -->
  <div id="generate-section" style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">
    <button class="btn-primary" id="gen-btn" onclick="generateProject()">
      ⚡ Generate &amp; Download ZIP
    </button>
    <span id="form-error" style="color:#f87171;font-size:0.85rem;"></span>
  </div>

  <!-- ── Progress ── -->
  <div class="card progress-wrap" id="progress-wrap">
    <div class="spinner"></div>
    <div style="color:var(--muted);font-size:0.95rem;">Building your project...</div>
  </div>

  <!-- ── Success ── -->
  <div class="card success-wrap" id="success-wrap">
    <div class="success-icon">✅</div>
    <div class="success-title">Project Generated!</div>
    <div class="success-sub">Your ZIP is downloading. Unzip, then follow these steps:</div>
    <div class="next-steps" id="next-steps"></div>
    <div style="margin-top:20px;display:flex;gap:10px;justify-content:center;">
      <button class="btn-primary" onclick="redownload()">⬇️ Download Again</button>
      <button class="btn-secondary" onclick="resetForm()">← New Project</button>
    </div>
  </div>

  <hr class="divider" />

  <!-- ── cURL / API docs ── -->
  <div>
    <div class="section-title">🔧 Use via cURL / API</div>
    <div class="section-sub">Generate projects programmatically – great for CI pipelines and scripts.</div>

    <div style="margin-bottom:16px;">
      <p style="font-size:0.8rem;color:var(--muted);margin-bottom:8px;">POST /api/generate – Example</p>
      <div class="curl-box"><span class="hl">curl</span> -X POST http://localhost:5050/api/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    <span class="hl">"project_name"</span>: "shop-app",
    <span class="hl">"platform"</span>:     "Web",
    <span class="hl">"category"</span>:     "E-commerce",
    <span class="hl">"colors"</span>:       ["#6366f1"],
    <span class="hl">"style"</span>:        "Modern",
    <span class="hl">"scope"</span>:        "Scalable app"
  }' \\
  --output shop-app.zip</div>
    </div>

    <div>
      <p style="font-size:0.8rem;color:var(--muted);margin-bottom:8px;">GET /api/stacks – List available stacks</p>
      <div class="curl-box"><span class="hl">curl</span> http://localhost:5050/api/stacks</div>
    </div>
  </div>
</div>

<script>
// ── State ─────────────────────────────────────
const state = {
  platform: '',
  category: '',
  colors: ['#6366f1'],
  style: '',
  scope: '',
};

const stackMeta = """ + json.dumps({
    f"{p}|{c}": {
        "label": STACK_META.get(resolve_stack(p, c), {}).get("label", ""),
        "tags": STACK_META.get(resolve_stack(p, c), {}).get("tags", []),
    }
    for p in PLATFORMS_LIST
    for c in CATEGORIES_LIST
}) + """;

let lastZipUrl = null;
let lastZipName = null;

// ── Selection ─────────────────────────────────
function select(field, value, el) {
  state[field] = value;

  const gridId = field + '-grid';
  const grid = document.getElementById(gridId);
  if (grid) {
    grid.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
    el.classList.add('selected');
  }

  if (field === 'platform' || field === 'category') {
    updateStackPreview();
  }
}

function updateStackPreview() {
  const key = state.platform + '|' + state.category;
  const meta = stackMeta[key];
  const preview = document.getElementById('stack-preview');

  if (meta && meta.label) {
    document.getElementById('stack-label').textContent = '💡 ' + meta.label;
    document.getElementById('stack-desc').textContent = '';
    const tagsEl = document.getElementById('stack-tags');
    tagsEl.innerHTML = meta.tags.map(t => `<span class="stack-tag">${t}</span>`).join('');
    preview.classList.add('visible');
  } else {
    preview.classList.remove('visible');
  }
}

// ── Color ─────────────────────────────────────
function updateColor(val) {
  state.colors = [val];
  document.getElementById('color-text').value = val;
}
function syncColorFromText(val) {
  if (/^#[0-9a-fA-F]{6}$/.test(val)) {
    state.colors = [val];
    document.getElementById('color-picker').value = val;
  }
}
function applyPreset(hex) {
  state.colors = [hex];
  document.getElementById('color-picker').value = hex;
  document.getElementById('color-text').value = hex;
}

// ── Generate ──────────────────────────────────
async function generateProject() {
  const err = document.getElementById('form-error');
  err.textContent = '';

  if (!state.platform) return (err.textContent = 'Please select a platform.');
  if (!state.category) return (err.textContent = 'Please select a category.');
  if (!state.style)    return (err.textContent = 'Please select a design style.');
  if (!state.scope)    return (err.textContent = 'Please select a scope.');

  const projectName = document.getElementById('project-name').value.trim() || 'my-project';

  const payload = {
    project_name: projectName,
    platform: state.platform,
    category: state.category,
    colors: state.colors,
    style: state.style,
    scope: state.scope,
  };

  // Show progress
  document.getElementById('generate-section').style.display = 'none';
  document.getElementById('progress-wrap').style.display = 'block';
  document.getElementById('success-wrap').style.display = 'none';

  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.error || 'Generation failed');
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    lastZipUrl = url;
    lastZipName = projectName + '.zip';

    // Auto-download
    const a = document.createElement('a');
    a.href = url;
    a.download = lastZipName;
    a.click();

    // Detect stack for next steps
    const stackId = res.headers.get('X-Stack-Id') || '';
    showSuccess(projectName, stackId);

  } catch (e) {
    document.getElementById('generate-section').style.display = 'flex';
    document.getElementById('progress-wrap').style.display = 'none';
    err.textContent = '❌ ' + e.message;
  }
}

function showSuccess(name, stackId) {
  document.getElementById('progress-wrap').style.display = 'none';
  document.getElementById('success-wrap').style.display = 'block';

  const steps = getNextSteps(name, stackId);
  const el = document.getElementById('next-steps');
  el.innerHTML = '<div class="next-steps-title">Quick Start</div>' +
    steps.map((s, i) => `
      <div class="step-item">
        <div class="step-num">${i+1}</div>
        <div>
          <div class="step-cmd">${s.cmd}</div>
          ${s.hint ? `<div class="step-hint">${s.hint}</div>` : ''}
        </div>
      </div>`).join('');
}

function getNextSteps(name, stackId) {
  const base = [
    { cmd: `unzip ${name}.zip && cd ${name}` },
    { cmd: 'cp .env.example .env', hint: '← Fill in secrets. That\'s it!' },
  ];
  if (stackId === 'nextjs_postgres_prisma') {
    return [...base,
      { cmd: 'npm install' },
      { cmd: 'npm run db:push && npm run db:seed' },
      { cmd: 'npm run dev', hint: 'http://localhost:3000' },
    ];
  } else if (stackId === 'react_node_mongo') {
    return [...base,
      { cmd: 'cd server && npm install && npm run seed && npm run dev' },
      { cmd: 'cd ../client && npm install && npm run dev', hint: 'http://localhost:5173' },
    ];
  } else if (stackId === 'django_postgres') {
    return [...base,
      { cmd: 'python -m venv venv && source venv/bin/activate' },
      { cmd: 'pip install -r requirements.txt' },
      { cmd: 'python manage.py migrate && python manage.py runserver', hint: 'http://localhost:8000' },
    ];
  } else if (stackId === 'vue_express_mysql') {
    return [...base,
      { cmd: 'cd server && npm install && node src/sync-db.js && npm run dev' },
      { cmd: 'cd ../client && npm install && npm run dev', hint: 'http://localhost:5173' },
    ];
  } else if (stackId === 'electron_sqlite') {
    return [...base,
      { cmd: 'npm install && npm run dev', hint: 'Opens Electron window' },
    ];
  } else {
    return [...base,
      { cmd: 'npm install && npm run dev', hint: 'http://localhost:5173' },
    ];
  }
}

function redownload() {
  if (lastZipUrl) {
    const a = document.createElement('a');
    a.href = lastZipUrl;
    a.download = lastZipName;
    a.click();
  }
}

function resetForm() {
  document.getElementById('generate-section').style.display = 'flex';
  document.getElementById('success-wrap').style.display = 'none';
  document.getElementById('form-error').textContent = '';
}
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return WEB_UI


@app.route("/api/stacks", methods=["GET"])
def list_stacks():
    return jsonify(STACK_META)


@app.route("/api/preview", methods=["POST"])
def preview():
    body = request.get_json(silent=True) or {}
    platform = body.get("platform", "Web")
    category = body.get("category", "E-commerce")
    stack_id = resolve_stack(platform, category)
    meta = STACK_META.get(stack_id, {})
    return jsonify({"stack_id": stack_id, "meta": meta})


@app.route("/api/generate", methods=["POST"])
def generate():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "JSON body required"}), 400

    required = ["project_name", "platform", "category"]
    missing = [k for k in required if not body.get(k)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    project_name = body["project_name"].strip().replace(" ", "-") or "my-project"
    options = {
        "platform": body["platform"],
        "category": body["category"],
        "colors": body.get("colors", ["#3B82F6"]),
        "style": body.get("style", "Modern"),
        "scope": body.get("scope", "Scalable app"),
    }

    try:
        zip_bytes, stack_id, meta = generate_project_to_zip(options, project_name)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    response = send_file(
        io.BytesIO(zip_bytes),
        mimetype="application/zip",
        as_attachment=True,
        download_name=f"{project_name}.zip",
    )
    response.headers["X-Stack-Id"] = stack_id
    response.headers["X-Stack-Label"] = meta.get("label", "")
    return response


# ─────────────────────────────────────────────────────────────
# Entry
# ─────────────────────────────────────────────────────────────

def run_server(host="0.0.0.0", port=5050, debug=False):
    print(f"\n🌐  Project Generator Web UI  →  http://localhost:{port}")
    print(f"   API: http://localhost:{port}/api/generate\n")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server(debug=True)