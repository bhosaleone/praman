/**
 * Praman Dashboard — Reactive Client Logic
 * Theme: Light Sepia & Saffron Accent
 */

let currentData = null;
let currentSort = { column: 'demand', direction: 'desc' };
let serpObservations = {}; // keyword -> { thin: bool|null, weak: bool|null, stale: bool|null, notes: string }
let currentEditingSeed = null;
let candidateViewMode = 'clean'; // 'clean' or 'raw'

document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  const input = document.getElementById('seeds-input');
  if (input && !input.value.trim()) {
    input.value = "शेती, हवामान, marathi sheti, पीक विमा";
  }
  runResearch();
});

function setupEventListeners() {
  // Preset buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      const seeds = btn.getAttribute('data-seeds');
      document.getElementById('lang-select').value = lang;
      document.getElementById('seeds-input').value = seeds;
      showToast(`Loaded ${btn.textContent.trim()} preset`);
      runResearch();
    });
  });

  // Run Research Button
  const runBtn = document.getElementById('run-research-btn');
  if (runBtn) {
    runBtn.addEventListener('click', runResearch);
  }

  // Search Filter in Table
  const searchInput = document.getElementById('table-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      filterTable(e.target.value);
    });
  }

  // Table Sorting Headers
  document.querySelectorAll('#demand-data-table th[data-sort]').forEach(th => {
    th.addEventListener('click', () => {
      const col = th.getAttribute('data-sort');
      if (currentSort.column === col) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
      } else {
        currentSort.column = col;
        currentSort.direction = 'desc';
      }
      renderTable();
    });
  });

  // Tab switching
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');

      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      const targetId = btn.getAttribute('data-tab');
      const panel = document.getElementById(targetId);
      if (panel) panel.style.display = 'block';
    });
  });

  // Candidates view toggle (Research vs Raw)
  const toggleClean = document.getElementById('toggle-candidates-clean');
  const toggleRaw = document.getElementById('toggle-candidates-raw');
  if (toggleClean && toggleRaw) {
    toggleClean.addEventListener('click', () => {
      candidateViewMode = 'clean';
      toggleClean.classList.add('active');
      toggleRaw.classList.remove('active');
      renderCandidatesView();
    });
    toggleRaw.addEventListener('click', () => {
      candidateViewMode = 'raw';
      toggleRaw.classList.add('active');
      toggleClean.classList.remove('active');
      renderCandidatesView();
    });
  }

  // Export & Report Action Buttons
  const exportCsvBtn = document.getElementById('export-csv-btn');
  if (exportCsvBtn) exportCsvBtn.addEventListener('click', exportCSV);

  const exportJsonBtn = document.getElementById('export-json-btn');
  if (exportJsonBtn) exportJsonBtn.addEventListener('click', exportJSON);

  const exportReportBtn = document.getElementById('export-report-btn');
  if (exportReportBtn) exportReportBtn.addEventListener('click', downloadMarkdownReport);

  const previewReportBtn = document.getElementById('preview-report-btn');
  if (previewReportBtn) previewReportBtn.addEventListener('click', openReportModal);

  const exportPlanBtn = document.getElementById('export-plan-btn');
  if (exportPlanBtn) exportPlanBtn.addEventListener('click', exportContentPlan);

  // Tree Canvas Controls
  const treeSearch = document.getElementById('tree-search-input');
  if (treeSearch) {
    treeSearch.addEventListener('input', () => {
      renderTreeCanvas();
    });
  }

  const treeSeedFilter = document.getElementById('tree-seed-filter');
  if (treeSeedFilter) {
    treeSeedFilter.addEventListener('change', () => {
      renderTreeCanvas();
    });
  }

  const treeExpandAll = document.getElementById('tree-expand-all');
  if (treeExpandAll) {
    treeExpandAll.addEventListener('click', () => {
      document.querySelectorAll('#tree-canvas-content details').forEach(d => d.open = true);
    });
  }

  const treeCollapseAll = document.getElementById('tree-collapse-all');
  if (treeCollapseAll) {
    treeCollapseAll.addEventListener('click', () => {
      document.querySelectorAll('#tree-canvas-content details').forEach(d => d.open = false);
    });
  }

  // Setup Modals
  setupSerpModalEvents();
  setupReportModalEvents();
  setupScoreModalEvents();
  setupInspectorModalEvents();
  setupIntentModalEvents();
  setupGuideModalEvents();
}

/* ==========================================================================
   Tutorial & Workflow Guide Modal
   ========================================================================== */
function setupGuideModalEvents() {
  const openBtn = document.getElementById('open-guide-btn');
  const modal = document.getElementById('guide-modal');
  const closeBtn = document.getElementById('guide-modal-close');
  const gotItBtn = document.getElementById('guide-modal-got-it');

  if (openBtn && modal) {
    openBtn.addEventListener('click', () => {
      modal.style.display = 'flex';
    });
  }

  const closeModal = () => {
    if (modal) modal.style.display = 'none';
  };

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (gotItBtn) gotItBtn.addEventListener('click', closeModal);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  // Quick preset triggers inside the guide modal
  document.querySelectorAll('.guide-preset-trigger').forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      const seeds = btn.getAttribute('data-seeds');
      const langSelect = document.getElementById('lang-select');
      const seedsInput = document.getElementById('seeds-input');
      if (langSelect) langSelect.value = lang;
      if (seedsInput) seedsInput.value = seeds;
      closeModal();
      showToast(`Loaded ${btn.textContent.trim()}! Measuring demand...`);
      runResearch();
    });
  });
}

/* ==========================================================================
   Score Explanation Modal
   ========================================================================== */
function setupScoreModalEvents() {
  const modal = document.getElementById('score-modal');
  const closeBtn = document.getElementById('score-modal-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
  }
}

function openScoreModal(kw) {
  const modal = document.getElementById('score-modal');
  const body = document.getElementById('score-modal-body');
  document.getElementById('score-modal-title').textContent = `Demand Score: "${kw.seed}"`;

  const dVal = kw.demand !== null ? kw.demand.toFixed(3) : '⊥ (Unmeasured)';
  const bRaw = kw.axes.breadth !== null ? kw.axes.breadth.toFixed(3) : '⊥';
  const cRaw = kw.axes.coverage !== null ? kw.axes.coverage.toFixed(3) : '⊥';
  const denRaw = kw.axes.density !== null ? kw.axes.density.toFixed(3) : '⊥';
  const depRaw = kw.axes.depth !== null ? kw.axes.depth.toFixed(3) : '⊥';

  const bComp = kw.components.breadth !== null ? kw.components.breadth.toFixed(3) : '0.000';
  const cComp = kw.components.coverage !== null ? kw.components.coverage.toFixed(3) : '0.000';
  const denComp = kw.components.density !== null ? kw.components.density.toFixed(3) : '0.000';
  const depComp = kw.components.depth !== null ? kw.components.depth.toFixed(3) : '0.000';

  body.innerHTML = `
    <div class="score-breakdown-card">
      <p style="font-size:0.9rem;color:var(--text-muted);">
        The demand score is a <strong>pinned-weight convex combination</strong> of four observed voices (MATH.md §6). The denominator never renormalizes.
      </p>

      <table class="score-breakdown-table">
        <thead>
          <tr>
            <th>Demand Voice</th>
            <th>Weight</th>
            <th>Raw Measured Value</th>
            <th>Contribution</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Expansion Breadth</strong></td>
            <td>50% (0.50)</td>
            <td>${bRaw}</td>
            <td>${bComp}</td>
          </tr>
          <tr>
            <td><strong>Head Coverage</strong></td>
            <td>25% (0.25)</td>
            <td>${cRaw}</td>
            <td>${cComp}</td>
          </tr>
          <tr>
            <td><strong>Question Density</strong></td>
            <td>15% (0.15)</td>
            <td>${denRaw}</td>
            <td>${denComp}</td>
          </tr>
          <tr>
            <td><strong>Rank Depth</strong></td>
            <td>10% (0.10)</td>
            <td>${depRaw}</td>
            <td>${depComp}</td>
          </tr>
          <tr class="score-total-row">
            <td><strong>Total Demand Index</strong></td>
            <td>100% (1.00)</td>
            <td>Mass: ${kw.measured_mass.toFixed(2)}</td>
            <td><strong>${dVal}</strong></td>
          </tr>
        </tbody>
      </table>

      <div style="font-size:0.85rem;color:var(--text-muted);background:var(--bg-input);padding:0.75rem;border-radius:var(--radius-sm);">
        ${kw.demand_complete
          ? '✅ <strong>Complete:</strong> All four demand voices were successfully measured (c = 1.0).'
          : '⚠️ <strong>Partial Measurement:</strong> Unmeasured voices keep their weight; achievable score is capped below 1.0 (Theorem 2).'}
      </div>
    </div>
  `;

  modal.style.display = 'flex';
}

/* ==========================================================================
   Research Tree / Inspector Modal
   ========================================================================== */
function setupInspectorModalEvents() {
  const modal = document.getElementById('inspector-modal');
  const closeBtn = document.getElementById('inspector-modal-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
  }
}

function setupIntentModalEvents() {
  const modal = document.getElementById('intent-modal');
  const closeBtn = document.getElementById('intent-modal-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
  }
}

/* ==========================================================================
   Intent Diagnostic & Evidence Inspector
   ========================================================================== */
function openIntentModal(seed) {
  const kw = currentData?.keywords?.find(k => k.seed === seed);
  if (!kw) return;

  const modal = document.getElementById('intent-modal');
  const body = document.getElementById('intent-modal-body');
  document.getElementById('intent-modal-title').textContent = `Intent Diagnostic: "${seed}"`;

  const cleanCands = kw.signals?.research_candidates || kw.signals?.discovered || [];
  const rawObs = kw.signals?.raw_observations || [];
  const allSuggestions = [...cleanCands, ...rawObs];

  // Bucket suggestions by apparent intent markers
  const buckets = {
    freshness: [],
    transactional: [],
    howto: [],
    comparison: [],
    informational: [],
    general: []
  };

  const freshRe = /\b(2025|2026|2027|today|latest|news|आज|आता|नवीन)\b/i;
  const transRe = /\b(pdf|download|free|price|cost|buy|ऑनलाइन|online|फॉर्म|अर्ज|यादी|लिस्ट)\b/i;
  const howtoRe = /\b(कसे|कसा|कशी|how|how to|पद्धती|नियम|योजना)\b/i;
  const compRe = /\b(vs|versus|तुलना|फरक|best|का)\b/i;
  const infoRe = /\b(काय|माहिती|what|अर्थ|विवरण|तपशील)\b/i;

  const seen = new Set();
  allSuggestions.forEach(s => {
    if (seen.has(s) || s.trim().length <= 3) return;
    seen.add(s);
    if (freshRe.test(s)) buckets.freshness.push(s);
    else if (transRe.test(s)) buckets.transactional.push(s);
    else if (howtoRe.test(s)) buckets.howto.push(s);
    else if (compRe.test(s)) buckets.comparison.push(s);
    else if (infoRe.test(s)) buckets.informational.push(s);
    else buckets.general.push(s);
  });

  const isUnclear = kw.intent === 'unclear';
  let diagnosticHtml = '';
  if (isUnclear) {
    diagnosticHtml = `
      <div class="intent-diagnostic-box">
        <div class="intent-status-badge">
          <span>🔍</span>
          <span>Diagnostic Status: <strong>Unclear (Explicit Marker Absent)</strong></span>
        </div>
        <p class="intent-diagnostic-desc">
          No explicit linguistic marker was detected in the head seed query <code>"${escapeHTML(seed)}"</code>.
          Praman adheres strictly to the <strong>METHODOLOGY</strong> contract: absence of explicit linguistic markers is surfaced as <code>unclear</code> rather than falsely guessed as informational.
          Review the autocomplete expansion evidence below to understand real search intent patterns.
        </p>
      </div>
    `;
  } else {
    diagnosticHtml = `
      <div class="intent-diagnostic-box">
        <div class="intent-status-badge">
          <span>🎯</span>
          <span>Detected Intent: <strong>${escapeHTML(kw.intent)}</strong> (${escapeHTML(kw.article_shape || 'General')})</span>
        </div>
        <p class="intent-diagnostic-desc">
          Matched explicit linguistic patterns in query structure. Review supporting suggestion patterns below.
        </p>
      </div>
    `;
  }

  // Render suggestion categories with [+ Measure] buttons
  let categoriesHtml = '';

  const renderGroup = (label, icon, items) => {
    if (!items.length) return '';
    return `
      <div class="intent-group-title">
        <span>${icon}</span>
        <span>${label} (${items.length})</span>
      </div>
      ${items.slice(0, 25).map(item => `
        <div class="intent-candidate-item">
          <span style="font-weight:600;font-size:0.9rem;">${escapeHTML(item)}</span>
          <button type="button" class="measure-candidate-btn" onclick="measureCandidate('${escapeHTML(item)}')">[+ Measure]</button>
        </div>
      `).join('')}
    `;
  };

  categoriesHtml += renderGroup('Freshness / Temporal Demand', '📅', buckets.freshness);
  categoriesHtml += renderGroup('Transactional / Downloads & Forms', '💳', buckets.transactional);
  categoriesHtml += renderGroup('How-To / Method Queries', '🛠️', buckets.howto);
  categoriesHtml += renderGroup('Informational / Question Queries', '❓', buckets.informational);
  categoriesHtml += renderGroup('Comparison Demand', '⚖️', buckets.comparison);
  categoriesHtml += renderGroup('General Autocomplete Extensions', '💡', buckets.general.slice(0, 15));

  if (!categoriesHtml) {
    categoriesHtml = '<p style="color:var(--text-dim);font-size:0.88rem;">No expansion suggestions captured for this seed.</p>';
  }

  body.innerHTML = `
    ${diagnosticHtml}

    <div class="intent-evidence-section">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:0.5rem;flex-wrap:wrap;gap:0.5rem;">
        <span style="font-weight:700;color:var(--text-muted);font-size:0.92rem;">
          📊 Expansion Evidence for Intent Discovery (${seen.size} queries)
        </span>
        <span style="font-size:0.78rem;color:var(--text-dim);">Scroll to explore • Click [+ Measure]</span>
      </div>

      <!-- Scrollable Suggestion List with custom scrollbar -->
      <div class="intent-evidence-scroll-container">
        ${categoriesHtml}
      </div>
    </div>
  `;

  modal.style.display = 'flex';
}

function openTreeModal(seed) {
  const kw = currentData?.keywords?.find(k => k.seed === seed);
  if (!kw) return;

  const modal = document.getElementById('inspector-modal');
  const body = document.getElementById('inspector-modal-body');
  document.getElementById('inspector-modal-title').textContent = `Research Tree: "${seed}"`;

  const cleanCands = kw.signals?.research_candidates || kw.signals?.discovered || [];
  const rawObs = kw.signals?.raw_observations || [];

  let cleanItemsHtml = cleanCands.map(c => `
    <div class="tree-item">
      <span>${escapeHTML(c)}</span>
      <button type="button" class="measure-candidate-btn" onclick="measureCandidate('${escapeHTML(c)}')">[+ Measure]</button>
    </div>
  `).join('');

  if (!cleanCands.length) {
    cleanItemsHtml = '<p style="color:var(--text-dim);font-size:0.88rem;">No quality-filtered research candidates discovered for this seed.</p>';
  }

  let rawItemsHtml = rawObs.slice(0, 30).map(r => `
    <div class="tree-item" style="opacity:0.85;">
      <span style="font-size:0.86rem;"><code>${escapeHTML(r)}</code></span>
      <button type="button" class="btn btn-outline btn-sm" onclick="measureCandidate('${escapeHTML(r)}')">+ Add</button>
    </div>
  `).join('');

  body.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem;">
      <div class="tree-seed-title" style="margin:0;">🌱 Seed: ${escapeHTML(seed)}</div>
      <button type="button" class="btn btn-outline btn-sm" onclick="switchToTreeTab('${escapeHTML(seed)}')">🌳 Open in Full Tree Canvas</button>
    </div>
    <p style="font-size:0.88rem;color:var(--text-muted);margin-bottom:1rem;">
      Discovered <strong>${cleanCands.length}</strong> quality research candidates and <strong>${rawObs.length}</strong> total expansion observations.
    </p>

    <div class="tree-section-header">🎯 Research Candidates (Actionable)</div>
    <div class="tree-list">
      ${cleanItemsHtml}
    </div>

    <details style="margin-top:1.5rem;">
      <summary style="font-size:0.9rem;font-weight:700;color:var(--text-muted);cursor:pointer;">
        📜 View Raw Autocomplete Observations (${rawObs.length})
      </summary>
      <div class="tree-list" style="margin-top:0.75rem;">
        ${rawItemsHtml}
      </div>
    </details>
  `;

  modal.style.display = 'flex';
}

function measureCandidate(cand) {
  const input = document.getElementById('seeds-input');
  const existing = input.value.split(/[,\n]+/).map(s => s.trim()).filter(Boolean);
  if (!existing.includes(cand)) {
    existing.push(cand);
    input.value = existing.join(', ');
  }
  showToast(`Measuring "${cand}"...`);
  const modals = document.querySelectorAll('.modal-backdrop');
  modals.forEach(m => m.style.display = 'none');
  runResearch();
}

/* ==========================================================================
   SERP Modal Logic
   ========================================================================== */
function setupSerpModalEvents() {
  const modal = document.getElementById('serp-modal');
  const closeBtn = document.getElementById('serp-modal-close');
  const cancelBtn = document.getElementById('serp-modal-cancel');
  const saveBtn = document.getElementById('serp-modal-save');

  const closeModal = () => { modal.style.display = 'none'; };
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

  ['thin', 'weak', 'stale'].forEach(field => {
    const container = document.getElementById(`toggle-${field}`);
    if (!container) return;
    container.querySelectorAll('.tristate-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        container.querySelectorAll('.tristate-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        updateSerpPreviewBadge();
      });
    });
  });

  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      if (!currentEditingSeed) return;
      const getVal = (field) => {
        const active = document.querySelector(`#toggle-${field} .tristate-btn.active`);
        if (!active) return null;
        const v = active.getAttribute('data-val');
        if (v === 'yes') return true;
        if (v === 'no') return false;
        return null;
      };

      serpObservations[currentEditingSeed] = {
        thin: getVal('thin'),
        weak: getVal('weak'),
        stale: getVal('stale'),
        notes: 'Recorded via Praman Web UI',
      };

      closeModal();
      showToast(`Updated SERP notes for "${currentEditingSeed}"`);
      runResearch();
    });
  }
}

function openSerpModal(seed) {
  currentEditingSeed = seed;
  const modal = document.getElementById('serp-modal');
  document.getElementById('serp-modal-keyword').textContent = seed;

  const current = serpObservations[seed] || { thin: null, weak: null, stale: null };

  const setToggle = (field, val) => {
    const container = document.getElementById(`toggle-${field}`);
    if (!container) return;
    container.querySelectorAll('.tristate-btn').forEach(btn => {
      const v = btn.getAttribute('data-val');
      if (val === true && v === 'yes') btn.classList.add('active');
      else if (val === false && v === 'no') btn.classList.add('active');
      else if (val === null && v === 'unrecorded') btn.classList.add('active');
      else btn.classList.remove('active');
    });
  };

  setToggle('thin', current.thin);
  setToggle('weak', current.weak);
  setToggle('stale', current.stale);

  updateSerpPreviewBadge();
  modal.style.display = 'flex';
}

function updateSerpPreviewBadge() {
  const getVal = (field) => {
    const active = document.querySelector(`#toggle-${field} .tristate-btn.active`);
    if (!active) return null;
    const v = active.getAttribute('data-val');
    if (v === 'yes') return true;
    if (v === 'no') return false;
    return null;
  };

  const thin = getVal('thin');
  const weak = getVal('weak');
  const stale = getVal('stale');

  const recordedCount = [thin, weak, stale].filter(v => v !== null).length;
  const badge = document.getElementById('serp-preview-badge');

  if (recordedCount < 2) {
    badge.className = 'badge badge-unmeasured';
    badge.textContent = `unmeasured (${recordedCount}/3 fields)`;
    return;
  }

  let band = 'medium';
  if (weak === true) {
    band = thin === true ? 'low' : 'medium';
  } else if (weak === false) {
    band = thin === false ? 'very_high' : 'high';
  } else {
    if (thin === true && stale === true) band = 'medium';
    else if (thin === false && stale === false) band = 'high';
  }

  badge.className = `badge badge-evidence-${band === 'low' ? 'strong' : (band === 'medium' ? 'moderate' : 'weak')}`;
  badge.textContent = `${band} (${recordedCount}/3 fields recorded)`;
}

/* ==========================================================================
   Report Preview Modal Logic
   ========================================================================== */
function setupReportModalEvents() {
  const modal = document.getElementById('report-modal');
  const closeBtn = document.getElementById('report-modal-close');
  const copyBtn = document.getElementById('copy-report-btn');
  const downloadBtn = document.getElementById('modal-download-report-btn');

  const closeModal = () => { modal.style.display = 'none'; };
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const content = document.getElementById('report-modal-content').value;
      navigator.clipboard.writeText(content).then(() => {
        showToast('Report copied to clipboard!');
      }).catch(err => {
        console.error('Clipboard error:', err);
        showToast('Failed to copy to clipboard');
      });
    });
  }

  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadMarkdownReport);
  }
}

function openReportModal() {
  if (!currentData || !currentData.markdown_report) {
    showToast('Run research first to generate report');
    return;
  }
  document.getElementById('report-modal-content').value = currentData.markdown_report;
  document.getElementById('report-modal').style.display = 'flex';
}

/* ==========================================================================
   Research Runner
   ========================================================================== */
async function runResearch() {
  const seedsRaw = document.getElementById('seeds-input').value;
  const seeds = seedsRaw.split(/[,\n]+/).map(s => s.trim()).filter(Boolean);
  if (!seeds.length) {
    showToast('Please enter at least one seed keyword');
    return;
  }

  const mode = document.getElementById('mode-select').value;
  const lang = document.getElementById('lang-select').value;
  const latinExp = document.getElementById('latin-exp-toggle').checked;
  const maxQueries = document.getElementById('max-queries-input').value;

  const btn = document.getElementById('run-research-btn');
  const spinner = document.getElementById('btn-spinner');
  btn.disabled = true;
  if (spinner) spinner.style.display = 'inline-block';

  try {
    const payload = {
      seeds: seeds,
      language: lang,
      mode: mode,
      latin_expansion: latinExp,
      max_queries: maxQueries ? parseInt(maxQueries, 10) : null,
      serp_observations: serpObservations,
    };

    const res = await fetch('/api/research', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`Server returned HTTP ${res.status}`);
    }

    currentData = await res.json();
    updateUIWithResults(currentData);
  } catch (err) {
    console.error('Research error:', err);
    showToast(`Measurement error: ${err.message}`);
  } finally {
    btn.disabled = false;
    if (spinner) spinner.style.display = 'none';
  }
}

/* ==========================================================================
   UI Rendering
   ========================================================================== */
function updateUIWithResults(data) {
  document.getElementById('banner-section').style.display = 'flex';
  document.getElementById('kpi-ribbon').style.display = 'grid';
  document.getElementById('tab-bar-container').style.display = 'flex';

  // 1. Provenance Banner
  const banner = document.getElementById('run-provenance-banner');
  banner.className = 'banner-pill';
  if (data.mode === 'fixture') {
    banner.classList.add('banner-fixture');
    banner.innerHTML = '⚡ <strong>FIXTURE MODE:</strong> Deterministic synthetic data. Proves nothing about real search demand.';
  } else if (data.mode === 'recorded') {
    banner.classList.add('banner-recorded');
    banner.innerHTML = 'ℹ️ <strong>RECORDED MODE:</strong> Verified replay of historical autocomplete probes.';
  } else {
    banner.classList.add('banner-live');
    banner.innerHTML = '🟢 <strong>LIVE MODE:</strong> Active queries against Google Autocomplete endpoint.';
  }

  if (data.is_truncated) {
    banner.innerHTML += ' <span style="margin-left:8px;color:#be123c;font-weight:700;">⚠️ Query budget ceiling hit (truncated).</span>';
  }

  // 2. KPIs
  const kws = data.keywords || [];
  document.getElementById('kpi-seeds-count').textContent = kws.length;

  // Strong evidence count (demand >= 0.50)
  const strongEvidence = kws.filter(k => (k.demand || 0) >= 0.50).length;
  document.getElementById('kpi-high-pri-count').textContent = strongEvidence;

  // Unique research candidates count
  const allCleanCandidates = new Set();
  const allRawObservations = new Set();

  kws.forEach(k => {
    (k.signals?.research_candidates || k.signals?.discovered || []).forEach(c => allCleanCandidates.add(c));
    (k.signals?.raw_observations || []).forEach(r => allRawObservations.add(r));
  });

  document.getElementById('kpi-discovered-count').textContent = allCleanCandidates.size;
  document.getElementById('tab-candidates-badge').textContent = allCleanCandidates.size;
  document.getElementById('count-clean').textContent = allCleanCandidates.size;
  document.getElementById('count-raw').textContent = allRawObservations.size;

  // Avg demand
  const measuredDemands = kws.map(k => k.demand).filter(d => d !== null);
  const avgDemand = measuredDemands.length ? (measuredDemands.reduce((a, b) => a + b, 0) / measuredDemands.length) : 0;
  document.getElementById('kpi-avg-demand').textContent = avgDemand.toFixed(3);

  // 3. Render Table
  renderTable();

  // 4. Render Content Planner
  renderPlanner(data.planner);

  // 5. Render Candidates
  renderCandidatesView();

  // 6. Render Research Tree Canvas
  renderTreeCanvas();
}

function renderTable() {
  if (!currentData || !currentData.keywords) return;
  const tbody = document.getElementById('demand-table-body');
  tbody.innerHTML = '';

  let kws = [...currentData.keywords];

  kws.sort((a, b) => {
    let valA, valB;
    switch (currentSort.column) {
      case 'seed':
        valA = a.seed; valB = b.seed;
        return currentSort.direction === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
      case 'demand':
        valA = a.demand !== null ? a.demand : -1;
        valB = b.demand !== null ? b.demand : -1;
        break;
      case 'evidence':
        valA = a.demand || 0; valB = b.demand || 0;
        break;
      case 'intent':
        valA = a.intent; valB = b.intent;
        return currentSort.direction === 'asc' ? valA.localeCompare(valB) : valB.localeCompare(valA);
      case 'breadth':
        valA = a.axes.breadth !== null ? a.axes.breadth : -1;
        valB = b.axes.breadth !== null ? b.axes.breadth : -1;
        break;
      case 'coverage':
        valA = a.axes.coverage !== null ? a.axes.coverage : -1;
        valB = b.axes.coverage !== null ? b.axes.coverage : -1;
        break;
      case 'density':
        valA = a.axes.density !== null ? a.axes.density : -1;
        valB = b.axes.density !== null ? b.axes.density : -1;
        break;
      case 'depth':
        valA = a.axes.depth !== null ? a.axes.depth : -1;
        valB = b.axes.depth !== null ? b.axes.depth : -1;
        break;
      default:
        valA = a.demand || 0; valB = b.demand || 0;
    }
    return currentSort.direction === 'asc' ? valA - valB : valB - valA;
  });

  kws.forEach(kw => {
    const tr = document.createElement('tr');

    const dVal = kw.demand !== null ? kw.demand : null;
    let dClass = 'demand-low';
    if (dVal !== null) {
      if (dVal >= 0.50) dClass = 'demand-high';
      else if (dVal >= 0.25) dClass = 'demand-med';
    }

    const dStr = dVal !== null ? dVal.toFixed(3) : '⊥';
    const partialNote = (!kw.demand_complete && dVal !== null) ? '<span class="partial-flag" title="Some voices unmeasured">(partial)</span>' : '';

    // Evidence Band
    const evBand = kw.evidence_band || (dVal !== null ? (dVal >= 0.50 ? 'strong' : (dVal >= 0.25 ? 'moderate' : 'weak')) : 'insufficient');
    const evClass = `badge-evidence-${evBand}`;
    const evLabel = evBand.charAt(0).toUpperCase() + evBand.slice(1);

    const formatAxis = (v, comp = true) => {
      if (v === null) return '<span style="color:#948372;">⊥</span>';
      const s = v.toFixed(3);
      return !comp ? `<span title="Non-comparable due to budget truncation">⚠ ${s}</span>` : s;
    };

    const compBand = kw.competition?.band || 'unmeasured';
    const compLabel = compBand !== 'unmeasured' ? `<span class="badge ${evClass}">${compBand}</span>` : '<span style="color:#948372;font-size:0.85rem;">unmeasured</span>';

    // Intent label with dedicated diagnostic and scrollable evidence inspector
    let intentHtml = `<span class="badge badge-intent" onclick="openIntentModal('${escapeHTML(kw.seed)}')" title="Click to view intent diagnostic and suggestion evidence">${kw.intent}</span>`;
    if (kw.intent === 'unclear') {
      intentHtml = `<span class="badge badge-intent" onclick="openIntentModal('${escapeHTML(kw.seed)}')" title="No explicit markers in query wording. Click to inspect suggestion evidence.">unclear 🔍</span>`;
    }

    tr.innerHTML = `
      <td class="seed-cell"><code>${escapeHTML(kw.seed)}</code></td>
      <td>
        <span class="demand-score-pill ${dClass}" onclick='openScoreModal(${JSON.stringify(kw)})' title="Click to view transparent formula breakdown">
          ${dStr}
        </span>${partialNote}
      </td>
      <td><span class="badge ${evClass}">${evLabel}</span></td>
      <td>${intentHtml}</td>
      <td>${formatAxis(kw.axes.breadth, kw.signals?.breadth_comparable)}</td>
      <td>${formatAxis(kw.axes.coverage)}</td>
      <td>${formatAxis(kw.axes.density)}</td>
      <td>${formatAxis(kw.axes.depth)}</td>
      <td>
        ${compLabel}
        <button type="button" class="serp-edit-btn" onclick="openSerpModal('${escapeHTML(kw.seed)}')">📝 Review</button>
      </td>
      <td>
        <button type="button" class="tree-trigger-btn" onclick="switchToTreeTab('${escapeHTML(kw.seed)}')">🌳 Tree (${kw.signals?.research_candidates?.length || kw.signals?.discovered?.length || 0})</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  document.getElementById('table-row-count').textContent = `Showing ${kws.length} seeds`;
}

function filterTable(query) {
  const q = query.toLowerCase();
  document.querySelectorAll('#demand-table-body tr').forEach(tr => {
    const text = tr.innerText.toLowerCase();
    tr.style.display = text.includes(q) ? '' : 'none';
  });
}

function renderPlanner(planner) {
  if (!planner) return;
  const calList = document.getElementById('calendar-list');
  const linkList = document.getElementById('link-graph-list');
  calList.innerHTML = '';
  linkList.innerHTML = '';

  (planner.calendar || []).forEach(item => {
    const div = document.createElement('div');
    div.className = 'calendar-item';
    div.innerHTML = `
      <div class="calendar-order-badge">#${item.recommended_publish_order}</div>
      <div class="calendar-item-body">
        <div class="calendar-title">${escapeHTML(item.primary_title)}</div>
        <div class="calendar-meta">
          <span>Demand: <strong>${item.cluster_demand.toFixed(3)}</strong></span>
          <span>Intent: <span class="badge badge-intent" onclick="openIntentModal('${escapeHTML(item.primary_title)}')" title="Click to view intent diagnostic & evidence">${item.primary_intent}</span></span>
        </div>
        <div class="calendar-shape">${escapeHTML(item.article_shape)}</div>
      </div>
    `;
    calList.appendChild(div);
  });

  (planner.link_graph || []).forEach(link => {
    const div = document.createElement('div');
    div.className = 'link-item';
    div.innerHTML = `
      <div class="link-flow">
        <span>${escapeHTML(link.source_topic)}</span>
        <span class="link-arrow">➔</span>
        <span>${escapeHTML(link.target_topic)}</span>
      </div>
      <div class="link-anchor-row">
        Anchor: <span class="link-anchor">"${escapeHTML(link.anchor_text)}"</span> — ${escapeHTML(link.rationale)}
      </div>
    `;
    linkList.appendChild(div);
  });

  if (!planner.link_graph || !planner.link_graph.length) {
    linkList.innerHTML = '<p style="color:#948372;font-size:0.9rem;padding:0.75rem;">No multi-topic cross-links detected yet. Add more related seeds.</p>';
  }
}

function renderCandidatesView() {
  if (!currentData || !currentData.keywords) return;
  const container = document.getElementById('candidates-container');
  container.innerHTML = '';

  const candidatesSet = new Set();
  currentData.keywords.forEach(k => {
    const list = candidateViewMode === 'clean'
      ? (k.signals?.research_candidates || k.signals?.discovered || [])
      : (k.signals?.raw_observations || []);
    list.forEach(item => candidatesSet.add(item));
  });

  const items = Array.from(candidatesSet);

  if (!items.length) {
    container.innerHTML = '<p style="color:var(--text-muted);padding:1rem;">No candidates available in this view.</p>';
    return;
  }

  items.slice(0, 60).forEach(c => {
    const card = document.createElement('div');
    card.className = 'candidate-card';
    card.innerHTML = `
      <span class="candidate-query-text" title="${escapeHTML(c)}">${escapeHTML(c)}</span>
      <button type="button" class="measure-candidate-btn" onclick="measureCandidate('${escapeHTML(c)}')">[+ Measure]</button>
    `;
    container.appendChild(card);
  });
}

/* ==========================================================================
   Export & Download Functions
   ========================================================================== */
function downloadMarkdownReport() {
  if (!currentData || !currentData.markdown_report) {
    showToast('Run research first to generate report');
    return;
  }
  const content = currentData.markdown_report;
  const filename = `praman_report_${currentData.language}_${new Date().toISOString().slice(0, 10)}.md`;
  triggerDownload(filename, content, 'text/markdown;charset=utf-8');
  showToast('Downloaded Markdown report');
}

function exportContentPlan() {
  if (!currentData || !currentData.planner) {
    showToast('No content plan available');
    return;
  }
  const planner = currentData.planner;
  const lines = [
    `# Praman Editorial Content Plan — ${currentData.language.toUpperCase()}`,
    `Generated on ${new Date().toISOString().slice(0, 10)}`,
    '',
    '## Recommended Publishing Calendar',
    '| Order | Topic / Title | Cluster Demand | Intent | Article Shape |',
    '|---|---|---|---|---|',
  ];

  (planner.calendar || []).forEach(c => {
    lines.push(`| #${c.recommended_publish_order} | **${c.primary_title}** | ${c.cluster_demand.toFixed(3)} | ${c.primary_intent} | ${c.article_shape} |`);
  });

  lines.push('', '## Internal Link Architecture', '| Source Topic | Target Topic | Suggested Anchor Text | Rationale |', '|---|---|---|---|');
  (planner.link_graph || []).forEach(l => {
    lines.push(`| ${l.source_topic} | ${l.target_topic} | **${l.anchor_text}** | ${l.rationale} |`);
  });

  const content = lines.join('\n');
  const filename = `praman_content_plan_${currentData.language}_${new Date().toISOString().slice(0, 10)}.md`;
  triggerDownload(filename, content, 'text/markdown;charset=utf-8');
  showToast('Downloaded Editorial Content Plan');
}

function exportCSV() {
  if (!currentData || !currentData.keywords) {
    showToast('No data to export');
    return;
  }
  let csvContent = currentData.csv_report;
  if (!csvContent) {
    const headers = ['Seed', 'Demand', 'Evidence_Band', 'Priority_Band', 'Intent', 'Breadth', 'Coverage', 'Density', 'Depth', 'Competition', 'Seen'];
    const rows = currentData.keywords.map(k => [
      k.seed,
      k.demand !== null ? k.demand.toFixed(4) : '',
      k.evidence_band || '',
      k.priority_band || '',
      k.intent,
      k.axes.breadth !== null ? k.axes.breadth.toFixed(4) : '',
      k.axes.coverage !== null ? k.axes.coverage.toFixed(4) : '',
      k.axes.density !== null ? k.axes.density.toFixed(4) : '',
      k.axes.depth !== null ? k.axes.depth.toFixed(4) : '',
      k.competition?.band || '',
      k.signals?.suggestions_seen || 0
    ]);
    csvContent = [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  }

  const filename = `praman_demand_${new Date().toISOString().slice(0, 10)}.csv`;
  triggerDownload(filename, csvContent, 'text/csv;charset=utf-8');
  showToast('Downloaded CSV report');
}

function exportJSON() {
  if (!currentData) {
    showToast('No data to export');
    return;
  }
  const dataStr = JSON.stringify(currentData, null, 2);
  const filename = `praman_demand_${new Date().toISOString().slice(0, 10)}.json`;
  triggerDownload(filename, dataStr, 'application/json;charset=utf-8');
  showToast('Downloaded JSON export');
}

function triggerDownload(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function showToast(message) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => { toast.remove(); }, 300);
  }, 2500);
}

function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[tag] || tag));
}

/* ==========================================================================
   Tree Canvas & Tab Implementation
   ========================================================================== */
function switchToTreeTab(seed) {
  // Close any active modals
  document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');

  // Activate tab-tree
  document.querySelectorAll('.tab-btn').forEach(b => {
    const isTarget = b.getAttribute('data-tab') === 'tab-tree';
    b.classList.toggle('active', isTarget);
    b.setAttribute('aria-selected', isTarget ? 'true' : 'false');
  });
  document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
  const treePanel = document.getElementById('tab-tree');
  if (treePanel) treePanel.style.display = 'block';

  // If a specific seed was requested, select it in the dropdown and render
  if (seed) {
    const sel = document.getElementById('tree-seed-filter');
    if (sel) {
      sel.value = seed;
    }
  }
  renderTreeCanvas();

  // Scroll viewport smoothly to top
  const viewport = document.getElementById('tree-canvas-viewport');
  if (viewport) {
    viewport.scrollTop = 0;
    viewport.focus();
  }
}

function renderTreeCanvas() {
  if (!currentData || !currentData.keywords) return;
  const container = document.getElementById('tree-canvas-content');
  if (!container) return;

  const kws = currentData.keywords;
  const seedFilter = document.getElementById('tree-seed-filter');
  const searchInput = document.getElementById('tree-search-input');
  const filterQuery = searchInput ? searchInput.value.trim().toLowerCase() : '';
  const selectedSeed = seedFilter ? seedFilter.value : 'all';

  // Populate/sync seed dropdown options if needed
  if (seedFilter && seedFilter.options.length <= 1) {
    seedFilter.innerHTML = '<option value="all">🌱 All Evaluated Seeds</option>';
    kws.forEach(k => {
      const opt = document.createElement('option');
      opt.value = k.seed;
      const count = k.signals?.research_candidates?.length || k.signals?.discovered?.length || 0;
      opt.textContent = `${k.seed} (${count} candidates)`;
      seedFilter.appendChild(opt);
    });
  }

  // Filter seeds based on dropdown
  let filteredKws = kws;
  if (selectedSeed !== 'all') {
    filteredKws = kws.filter(k => k.seed === selectedSeed);
  }

  if (!filteredKws.length) {
    container.innerHTML = `
      <div class="tree-empty-state">
        <span class="tree-empty-icon">🔍</span>
        <p>No seeds match the current filter selection.</p>
      </div>
    `;
    return;
  }

  let html = '';

  filteredKws.forEach(kw => {
    let cleanCands = kw.signals?.research_candidates || kw.signals?.discovered || [];
    let rawObs = kw.signals?.raw_observations || [];

    // Filter by search query if user typed into tree search box
    if (filterQuery) {
      cleanCands = cleanCands.filter(c => c.toLowerCase().includes(filterQuery));
      rawObs = rawObs.filter(r => r.toLowerCase().includes(filterQuery));
    }

    // Determine evidence band badge styling
    const evBand = (kw.evidence_band || 'insufficient').toLowerCase();
    const evClass = `badge-evidence-${evBand}`;
    const evLabel = evBand === 'strong' ? 'Strong Evidence' :
                    evBand === 'moderate' ? 'Moderate Evidence' :
                    evBand === 'weak' ? 'Weak Evidence' : 'Insufficient Evidence';

    // Score pill
    const dVal = kw.demand !== null ? kw.demand.toFixed(3) : '⊥';
    const dClass = kw.demand === null ? 'demand-low' :
                   kw.demand >= 0.50 ? 'demand-high' :
                   kw.demand >= 0.25 ? 'demand-med' : 'demand-low';

    // Clean candidates HTML
    let cleanCandsHtml = '';
    if (cleanCands.length > 0) {
      cleanCandsHtml = `
        <div class="tree-candidate-grid">
          ${cleanCands.map(c => `
            <div class="tree-item">
              <span class="candidate-query-text" title="${escapeHTML(c)}">${escapeHTML(c)}</span>
              <button type="button" class="measure-candidate-btn" onclick="measureCandidate('${escapeHTML(c)}')">[+ Measure]</button>
            </div>
          `).join('')}
        </div>
      `;
    } else {
      cleanCandsHtml = `<p style="font-size:0.86rem;color:var(--text-dim);padding:0.5rem 0;">No matching research candidates found.</p>`;
    }

    // Raw observations HTML
    let rawObsHtml = '';
    if (rawObs.length > 0) {
      rawObsHtml = `
        <details style="margin-top:0.75rem;">
          <summary class="tree-branch-title">
            <span>📜 Raw Autocomplete Observations (${rawObs.length})</span>
            <span style="font-size:0.75rem;color:var(--text-dim);font-weight:normal;">alphabet probes &amp; artifacts</span>
          </summary>
          <div class="tree-candidate-grid" style="margin-top:0.6rem;opacity:0.9;">
            ${rawObs.slice(0, 50).map(r => `
              <div class="tree-item" style="background:#fff;">
                <span style="font-size:0.84rem;"><code>${escapeHTML(r)}</code></span>
                <button type="button" class="btn btn-outline btn-sm" onclick="measureCandidate('${escapeHTML(r)}')">+ Add</button>
              </div>
            `).join('')}
          </div>
        </details>
      `;
    }

    html += `
      <div class="tree-seed-block" id="tree-node-${escapeHTML(kw.seed)}">
        <div class="tree-seed-header">
          <div class="tree-seed-name">
            <span>🌱</span>
            <span>${escapeHTML(kw.seed)}</span>
          </div>
          <div class="tree-seed-badges">
            <span class="demand-score-pill ${dClass}" onclick='openScoreModal(${JSON.stringify(kw)})' title="Click to view score breakdown">
              Score: ${dVal}
            </span>
            <span class="badge ${evClass}">${evLabel}</span>
            <span class="badge badge-intent" onclick="openIntentModal('${escapeHTML(kw.seed)}')" title="Click to view intent diagnostic & evidence">
              ${kw.intent}
            </span>
          </div>
        </div>

        <div class="tree-branches">
          <div class="tree-branch-section">
            <div class="tree-branch-title">
              <span>🎯 Research Candidates (${cleanCands.length})</span>
              <span style="font-size:0.76rem;color:var(--accent-saffron);font-weight:700;">Click [+ Measure] to expand research</span>
            </div>
            ${cleanCandsHtml}
          </div>
          ${rawObsHtml}
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}
