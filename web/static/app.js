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
  setupSerpImportEvents();
  setupSerpBridgeAndUrlListener();
  setupReportModalEvents();
  setupScoreModalEvents();
  setupInspectorModalEvents();
  setupIntentModalEvents();
  setupGuideModalEvents();
  setupBlueprintModalEvents();
  setupExpandSeedsEvents();
  setupGroqKeyEvents();
}

/* ==========================================================================
   Tutorial & Workflow Guide Modal
   ========================================================================== */
function openGuideModalDirect() {
  const modal = document.getElementById('guide-modal');
  if (modal) {
    document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');
    modal.style.display = 'flex';
  }
}
window.openGuideModalDirect = openGuideModalDirect;

function closeGuideModalDirect() {
  const modal = document.getElementById('guide-modal');
  if (modal) {
    modal.style.display = 'none';
  }
}
window.closeGuideModalDirect = closeGuideModalDirect;

function setupGuideModalEvents() {
  const openBtn = document.getElementById('open-guide-btn');
  const modal = document.getElementById('guide-modal');
  const closeBtn = document.getElementById('guide-modal-close');
  const gotItBtn = document.getElementById('guide-modal-got-it');

  if (openBtn) {
    openBtn.addEventListener('click', openGuideModalDirect);
  }

  if (closeBtn) closeBtn.addEventListener('click', closeGuideModalDirect);
  if (gotItBtn) gotItBtn.addEventListener('click', closeGuideModalDirect);

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeGuideModalDirect();
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
      closeGuideModalDirect();
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
          <button type="button" class="measure-candidate-btn" data-candidate="${escapeHTML(item)}" onclick="handleMeasureCandidateClick(this)" title="Measure independent demand for this candidate">[+ Measure]</button>
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
      <button type="button" class="measure-candidate-btn" data-candidate="${escapeHTML(c)}" onclick="handleMeasureCandidateClick(this)" title="Measure independent demand for this candidate">[+ Measure]</button>
    </div>
  `).join('');

  if (!cleanCands.length) {
    cleanItemsHtml = '<p style="color:var(--text-dim);font-size:0.88rem;">No quality-filtered research candidates discovered for this seed.</p>';
  }

  let rawItemsHtml = rawObs.slice(0, 30).map(r => `
    <div class="tree-item" style="opacity:0.85;">
      <span style="font-size:0.86rem;"><code>${escapeHTML(r)}</code></span>
      <button type="button" class="btn btn-outline btn-sm" data-candidate="${escapeHTML(r)}" onclick="handleMeasureCandidateClick(this)" title="Add and measure this observation">+ Add</button>
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

function handleMeasureCandidateClick(btn) {
  if (!btn) return;
  const cand = btn.getAttribute('data-candidate');
  if (cand) {
    measureCandidate(cand, btn);
  }
}

async function measureCandidate(cand, btn = null) {
  if (!cand) return;
  cand = cand.trim();

  // If button was passed, show immediate loading feedback
  if (btn) {
    btn.disabled = true;
    btn.setAttribute('data-original-text', btn.innerHTML);
    btn.innerHTML = '⏳ Measuring...';
  }

  const input = document.getElementById('seeds-input');
  const existing = input.value.split(/[,\n]+/).map(s => s.trim()).filter(Boolean);

  if (existing.includes(cand)) {
    showToast(`ℹ️ "${cand}" is already measured. Showing in Demand Table...`);
    switchToTableTabAndHighlight(cand);
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = btn.getAttribute('data-original-text') || '[+ Measure]';
    }
    return;
  }

  existing.push(cand);
  input.value = existing.join(', ');

  showToast(`🌱 Promoting "${cand}" to measured seed...`);

  // Close any open backdrop modal so user isn't stuck behind a popup
  document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');

  try {
    await runResearch();
    switchToTableTabAndHighlight(cand);
    showToast(`✅ "${cand}" measured! See Demand Score & Blueprint below.`);
  } catch (err) {
    console.error('Error measuring candidate:', err);
    showToast(`Error measuring "${cand}": ${err.message}`);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = btn.getAttribute('data-original-text') || '[+ Measure]';
    }
  }
}

function switchToTableTabAndHighlight(seed) {
  // 1. Activate tab-table in tab bar
  document.querySelectorAll('.tab-btn').forEach(b => {
    const isTarget = b.getAttribute('data-tab') === 'tab-table';
    b.classList.toggle('active', isTarget);
    b.setAttribute('aria-selected', isTarget ? 'true' : 'false');
  });
  document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
  const tablePanel = document.getElementById('tab-table');
  if (tablePanel) tablePanel.style.display = 'block';

  // 2. Find row in #demand-table-body and highlight
  setTimeout(() => {
    const rows = document.querySelectorAll('#demand-table-body tr');
    let targetRow = null;
    rows.forEach(r => {
      if (r.getAttribute('data-seed') === seed) {
        targetRow = r;
      }
    });

    if (targetRow) {
      targetRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
      targetRow.classList.remove('row-highlight-pulse');
      void targetRow.offsetWidth; // Trigger reflow
      targetRow.classList.add('row-highlight-pulse');
    }
  }, 120);
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

  const googleBtn = document.getElementById('serp-modal-google-btn');
  if (googleBtn) {
    googleBtn.addEventListener('click', () => {
      if (currentEditingSeed) {
        window.open(`https://www.google.com/search?q=${encodeURIComponent(currentEditingSeed)}`, '_blank');
      }
    });
  }

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
   SERP Companion Ingestion & Import Modal
   ========================================================================== */
function importSerpData(payload, shouldRunResearch = true) {
  if (!payload) return 0;

  let items = [];
  if (Array.isArray(payload)) {
    items = payload;
  } else if (payload.keyword || payload.seed) {
    items = [payload];
  } else if (typeof payload === 'object') {
    // Dictionary of keyword -> observation
    for (const [k, v] of Object.entries(payload)) {
      if (v && typeof v === 'object') {
        items.push({ keyword: k, ...v });
      }
    }
  }

  if (items.length === 0) return 0;

  const seedsTextarea = document.getElementById('seeds-input');
  const existingSeedsText = seedsTextarea ? seedsTextarea.value : '';
  const existingSeedsList = existingSeedsText
    .split(/[\n,]/)
    .map(s => s.trim().toLowerCase())
    .filter(s => s.length > 0);

  const newSeedsToAdd = [];
  let importedCount = 0;

  items.forEach(item => {
    const kw = (item.keyword || item.seed || '').trim();
    if (!kw) return;

    // Normalize booleans
    const parseBool = (val) => {
      if (val === true || val === 'yes' || val === 'true') return true;
      if (val === false || val === 'no' || val === 'false') return false;
      return null;
    };

    const thin = parseBool(item.thin !== undefined ? item.thin : item.thin_results);
    const weak = parseBool(item.weak !== undefined ? item.weak : item.weak_domains);
    const stale = parseBool(item.stale !== undefined ? item.stale : item.top_results_stale);

    // Notes
    let notes = item.notes || '';
    if (!notes && item.topDomains && Array.isArray(item.topDomains)) {
      notes = `Top domains: ${item.topDomains.slice(0, 3).join(', ')}`;
    }
    if (!notes) {
      notes = 'Imported via Praman SERP Companion';
    }

    serpObservations[kw] = {
      thin: thin,
      weak: weak,
      stale: stale,
      notes: notes
    };

    importedCount++;

    if (!existingSeedsList.includes(kw.toLowerCase())) {
      newSeedsToAdd.push(kw);
      existingSeedsList.push(kw.toLowerCase());
    }
  });

  if (newSeedsToAdd.length > 0 && seedsTextarea) {
    const prefix = existingSeedsText.trim() ? existingSeedsText.trim() + '\n' : '';
    seedsTextarea.value = prefix + newSeedsToAdd.join('\n');
  }

  const sampleKw = (items[0].keyword || items[0].seed || '');
  const countStr = importedCount === 1 ? `"${sampleKw}"` : `${importedCount} keywords`;
  showToast(`✅ Imported SERP data for ${countStr}`);

  if (shouldRunResearch) {
    runResearch();
  }

  return importedCount;
}

function setupSerpImportEvents() {
  const modal = document.getElementById('serp-import-modal');
  const openBtn = document.getElementById('import-serp-btn');
  const tableOpenBtn = document.getElementById('table-import-serp-btn');
  const closeBtn = document.getElementById('serp-import-close');
  const cancelBtn = document.getElementById('serp-import-cancel');
  const pasteBtn = document.getElementById('serp-import-paste-btn');
  const sampleBtn = document.getElementById('serp-import-sample-btn');
  const clearBtn = document.getElementById('serp-import-clear-btn');
  const applyBtn = document.getElementById('serp-import-apply-btn');
  const textarea = document.getElementById('serp-import-json');
  const previewDiv = document.getElementById('serp-import-preview');
  const previewContent = document.getElementById('serp-import-preview-content');
  const countBadge = document.getElementById('serp-import-count-badge');
  const errorDiv = document.getElementById('serp-import-error');

  const openModal = () => {
    if (!modal) return;
    document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');
    modal.style.display = 'flex';
    updatePreview();
    if (textarea) textarea.focus();
  };

  const closeModal = () => {
    if (modal) modal.style.display = 'none';
  };

  if (openBtn) openBtn.addEventListener('click', openModal);
  if (tableOpenBtn) tableOpenBtn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (textarea) textarea.value = '';
      updatePreview();
    });
  }

  if (sampleBtn) {
    sampleBtn.addEventListener('click', () => {
      const sample = {
        keyword: "शेती योजना 2026",
        thin: true,
        weak: true,
        stale: false,
        band: "low",
        notes: "UGC forums & Quora dominating top 5 results",
        topDomains: ["quora.com", "facebook.com", "blogspot.com"]
      };
      if (textarea) {
        textarea.value = JSON.stringify(sample, null, 2);
        updatePreview();
      }
    });
  }

  if (pasteBtn) {
    pasteBtn.addEventListener('click', async () => {
      try {
        const text = await navigator.clipboard.readText();
        if (text && textarea) {
          textarea.value = text;
          updatePreview();
          showToast('📋 Pasted clipboard contents');
        }
      } catch (err) {
        console.warn('Clipboard read failed:', err);
        showToast('Please paste manually using Ctrl+V / Cmd+V');
        if (textarea) textarea.focus();
      }
    });
  }

  function updatePreview() {
    if (!textarea || !previewDiv || !previewContent) return;
    const val = textarea.value.trim();
    if (!val) {
      previewDiv.style.display = 'none';
      if (errorDiv) errorDiv.style.display = 'none';
      return;
    }

    try {
      const parsed = JSON.parse(val);
      let items = [];
      if (Array.isArray(parsed)) items = parsed;
      else if (parsed.keyword || parsed.seed) items = [parsed];
      else if (typeof parsed === 'object') {
        for (const [k, v] of Object.entries(parsed)) {
          if (v && typeof v === 'object') items.push({ keyword: k, ...v });
        }
      }

      if (items.length === 0) {
        throw new Error('No valid keyword observations found in JSON');
      }

      if (errorDiv) errorDiv.style.display = 'none';
      previewDiv.style.display = 'block';
      if (countBadge) countBadge.textContent = `${items.length} observation${items.length > 1 ? 's' : ''}`;

      previewContent.innerHTML = items.slice(0, 5).map(it => {
        const kw = it.keyword || it.seed || 'unnamed';
        const band = (it.band || 'unmeasured').toUpperCase();
        return `
          <div style="display:flex; justify-content:space-between; align-items:center; padding: 4px 0; border-bottom: 1px solid #ebdccb;">
            <strong>${escapeHTML(kw)}</strong>
            <span class="badge badge-comp-${(it.band || 'unmeasured').toLowerCase()}">${band}</span>
          </div>
        `;
      }).join('');

      if (items.length > 5) {
        previewContent.innerHTML += `<div style="font-size:0.75rem; color:#948372; margin-top:4px;">...and ${items.length - 5} more</div>`;
      }
    } catch (e) {
      previewDiv.style.display = 'none';
      if (errorDiv) {
        errorDiv.textContent = `Invalid JSON: ${e.message}`;
        errorDiv.style.display = 'block';
      }
    }
  }

  if (textarea) {
    textarea.addEventListener('input', updatePreview);
  }

  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      if (!textarea) return;
      const val = textarea.value.trim();
      if (!val) {
        showToast('Please paste or type SERP observation JSON first');
        return;
      }
      try {
        const parsed = JSON.parse(val);
        const count = importSerpData(parsed, true);
        if (count > 0) {
          closeModal();
        } else {
          showToast('Could not find valid keywords in JSON');
        }
      } catch (e) {
        showToast(`Error parsing JSON: ${e.message}`);
      }
    });
  }
}

function setupSerpBridgeAndUrlListener() {
  // 1. Check URL parameters on page load: ?import_serp=...
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const importSerp = urlParams.get('import_serp');
    if (importSerp) {
      const decoded = decodeURIComponent(importSerp);
      const parsed = JSON.parse(decoded);
      importSerpData(parsed, true);
      // Clean up URL parameter cleanly without page refresh
      const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
      window.history.replaceState({ path: cleanUrl }, document.title, cleanUrl);
    }
  } catch (err) {
    console.error('Error auto-importing SERP data from URL query param:', err);
  }

  // 2. Listen for window messages (from praman-bridge.js injected by Chrome extension)
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'PRAMAN_SERP_IMPORT' && event.data.observation) {
      importSerpData(event.data.observation, true);
    } else if (event.data && event.data.type === 'PRAMAN_EXTENSION_READY') {
      console.log('Praman SERP Companion Chrome extension is active (v' + (event.data.version || '1.0') + ')');
    }
  });
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
    if (typeof gtag === 'function') {
      gtag('event', 'search', {
        search_term: seeds.join(','),
        language: lang,
        mode: mode,
        results_count: currentData.keywords ? currentData.keywords.length : 0
      });
    }
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
    tr.setAttribute('data-seed', kw.seed);
    tr.id = `demand-row-${encodeURIComponent(kw.seed)}`;

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
    const compLabel = compBand !== 'unmeasured' 
      ? `<span class="badge badge-comp-${compBand}" title="${escapeHTML(kw.competition?.notes || '')}">${compBand}</span>` 
      : '<span style="color:#948372;font-size:0.85rem;">unmeasured</span>';

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
        <button type="button" class="blueprint-trigger-btn" onclick='openBlueprintModal(${JSON.stringify(kw)})' title="Turn measured research into an evidence-grounded editorial blueprint">⚡ Blueprint</button>
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
      <button type="button" class="measure-candidate-btn" data-candidate="${escapeHTML(c)}" onclick="handleMeasureCandidateClick(this)" title="Measure independent demand for this candidate">[+ Measure]</button>
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
  if (typeof gtag === 'function') {
    gtag('event', 'export_data', { format: 'csv' });
  }
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
  if (typeof gtag === 'function') {
    gtag('event', 'export_data', { format: 'json' });
  }
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
              <button type="button" class="measure-candidate-btn" data-candidate="${escapeHTML(c)}" onclick="handleMeasureCandidateClick(this)" title="Measure independent demand for this candidate">[+ Measure]</button>
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
                <button type="button" class="btn btn-outline btn-sm" data-candidate="${escapeHTML(r)}" onclick="handleMeasureCandidateClick(this)" title="Add and measure this observation">+ Add</button>
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

/* ==========================================================================
   Groq AI Deterministic Blueprint Modal
   ========================================================================== */
let currentBlueprintData = null;

function setupBlueprintModalEvents() {
  const modal = document.getElementById('blueprint-modal');
  const closeBtn = document.getElementById('blueprint-modal-close');
  const copyMdBtn = document.getElementById('blueprint-copy-md-btn');
  const copySchemaBtn = document.getElementById('blueprint-copy-schema-btn');

  const closeModal = () => { if (modal) modal.style.display = 'none'; };
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  if (copyMdBtn) {
    copyMdBtn.addEventListener('click', () => {
      if (!currentBlueprintData || !currentBlueprintData.markdown_blueprint) return;
      navigator.clipboard.writeText(currentBlueprintData.markdown_blueprint).then(() => {
        showToast('📋 Copied full Markdown blueprint to clipboard!');
      }).catch(err => {
        console.error('Clipboard error:', err);
      });
    });
  }

  if (copySchemaBtn) {
    copySchemaBtn.addEventListener('click', () => {
      if (!currentBlueprintData || !currentBlueprintData.faq_schema) return;
      const jsonStr = '<script type="application/ld+json">\n' + JSON.stringify(currentBlueprintData.faq_schema, null, 2) + '\n</script>';
      navigator.clipboard.writeText(jsonStr).then(() => {
        showToast('📋 Copied FAQ Schema (JSON-LD) for Rank Math!');
      }).catch(err => {
        console.error('Clipboard error:', err);
      });
    });
  }
}

async function openBlueprintModal(kw) {
  const modal = document.getElementById('blueprint-modal');
  const body = document.getElementById('blueprint-modal-body');
  if (!modal || !body) return;

  document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');
  modal.style.display = 'flex';

  body.innerHTML = `
    <div style="text-align: center; padding: 3rem 1rem;">
      <div class="btn-spinner" style="display: inline-block; width: 32px; height: 32px; border-width: 3px; border-color: #ea580c; border-top-color: transparent; margin-bottom: 1rem;"></div>
      <h4 style="font-size: 1.15rem; color: #271f18; margin-bottom: 0.5rem;">Synthesizing Evidence-Grounded Blueprint...</h4>
      <p style="font-size: 0.88rem; color: #645648; max-width: 500px; margin: 0 auto;">
        Turning Praman's measured search queries for <strong>"${escapeHTML(kw.seed)}"</strong> into an evidence-grounded editorial blueprint.
      </p>
    </div>
  `;

  try {
    const userKey = localStorage.getItem('praman_groq_api_key') || '';
    const payload = {
      seed: kw.seed,
      language: (currentData && currentData.language) || 'mr',
      demand: kw.demand,
      intent: kw.intent,
      competition_band: kw.competition?.band || null,
      suggestions: (kw.signals && (kw.signals.discovered || kw.signals.research_candidates)) || [],
      groq_api_key: userKey
    };

    const resp = await fetch('/api/blueprint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const err = await resp.json();
      throw new Error(err.error || `Server responded with ${resp.status}`);
    }

    const data = await resp.json();
    currentBlueprintData = data;
    renderBlueprintModal(kw, data);
  } catch (err) {
    console.error('Error generating blueprint:', err);
    const isKeyError = err.message && (err.message.includes('Groq API key') || err.message.includes('key is not configured'));

    if (isKeyError) {
      body.innerHTML = `
        <div style="padding: 2.5rem 1.5rem; text-align: center; max-width: 520px; margin: 0 auto;">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">🔑</div>
          <h3 style="font-size: 1.25rem; color: #271f18; margin-bottom: 0.5rem;">Connect Blueprint Intelligence Key</h3>
          <p style="font-size: 0.88rem; color: #645648; line-height: 1.5; margin-bottom: 1.25rem;">
            Praman turns measured research into an evidence-grounded editorial blueprint. Enter your free Groq API key below for instant, zero-hallucination synthesis. Free forever (14,400 requests/day, no credit card needed).
          </p>
          <div style="display: flex; gap: 8px; margin-bottom: 1rem;">
            <input type="password" id="modal-groq-key-input" class="number-input" placeholder="Paste gsk_... here" style="flex: 1; padding: 10px 12px; font-family: monospace; font-size: 0.88rem;">
            <button type="button" id="modal-groq-key-save-btn" class="btn btn-primary" style="white-space: nowrap;">⚡ Save &amp; Generate</button>
          </div>
          <div style="font-size: 0.8rem; color: #948372;">
            Need a key? <a href="https://console.groq.com/keys" target="_blank" rel="noopener" style="color: #ea580c; font-weight: 700; text-decoration: underline;">Get free key at console.groq.com &rarr;</a>
          </div>
        </div>
      `;

      const saveBtn = document.getElementById('modal-groq-key-save-btn');
      const input = document.getElementById('modal-groq-key-input');
      if (input) {
        input.value = localStorage.getItem('praman_groq_api_key') || '';
        input.focus();
      }
      if (saveBtn && input) {
        saveBtn.addEventListener('click', () => {
          const val = input.value.trim();
          if (!val) {
            showToast('Please enter your Groq API key (starts with gsk_)');
            return;
          }
          localStorage.setItem('praman_groq_api_key', val);
          showToast('🔑 Key saved! Synthesizing blueprint...');
          openBlueprintModal(kw);
        });
      }
      return;
    }

    body.innerHTML = `
      <div style="padding: 2rem; text-align: center; color: #be123c;">
        <h4>Failed to Generate Blueprint</h4>
        <p style="font-size: 0.88rem; margin-top: 0.5rem;">${escapeHTML(err.message)}</p>
        <button type="button" class="btn btn-outline btn-sm" onclick='openBlueprintModal(${JSON.stringify(kw)})' style="margin-top: 1rem;">Try Again</button>
      </div>
    `;
  }
}

function renderBlueprintModal(kw, bp) {
  const body = document.getElementById('blueprint-modal-body');
  if (!body) return;

  const demandStr = kw.demand !== null ? kw.demand.toFixed(3) : '⊥';
  const compBand = (kw.competition?.band || 'unmeasured').toUpperCase();

  let outlineHtml = '';
  (bp.outline || []).forEach(sec => {
    const lvl = sec.level || 'H2';
    const queries = sec.queries_answered || [];
    const points = sec.key_points || [];

    outlineHtml += `
      <div class="blueprint-section-card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
          <h4 style="margin: 0; font-size: 1rem; color: #271f18;"><span style="color: #ea580c; font-weight: 800;">${lvl}</span>: ${escapeHTML(sec.heading)}</h4>
        </div>
        ${queries.length > 0 ? `
          <div style="font-size: 0.78rem; color: #645648; margin-bottom: 8px;">
            <strong>Answering Praman queries:</strong> ${queries.map(q => `<code style="background: #faf6ee; padding: 2px 5px; border-radius: 4px; margin-right: 4px;">${escapeHTML(q)}</code>`).join('')}
          </div>
        ` : ''}
        <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.86rem; color: #3c2814;">
          ${points.map(pt => `<li style="margin-bottom: 4px;">${escapeHTML(pt)}</li>`).join('')}
        </ul>
      </div>
    `;
  });

  let faqHtml = '';
  (bp.faq || []).forEach(f => {
    const q = f.question || f.q || '';
    const a = f.answer || f.a || '';
    faqHtml += `
      <div class="blueprint-faq-card">
        <strong style="color: #271f18; font-size: 0.92rem;">Q: ${escapeHTML(q)}</strong>
        <p style="margin: 4px 0 0; font-size: 0.86rem; color: #503e2c;">A: ${escapeHTML(a)}</p>
      </div>
    `;
  });

  body.innerHTML = `
    <!-- Metadata Overview Bar -->
    <div class="blueprint-meta-box">
      <div style="font-size: 0.82rem; color: #854d0e; background: #fefce8; border: 1px solid #fef08a; padding: 7px 12px; border-radius: 6px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
        <span>💡</span>
        <span><strong>Core Promise:</strong> Praman turns measured research into an evidence-grounded editorial blueprint—grounding every H2/H3 and FAQ directly in verified search demand.</span>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
        <div>
          <span style="font-size: 0.72rem; font-weight: 700; color: #645648; text-transform: uppercase;">Seed Keyword</span>
          <h3 style="margin: 2px 0 0; font-size: 1.15rem; color: #271f18;">${escapeHTML(bp.seed)}</h3>
        </div>
        <div style="display: flex; gap: 6px; align-items: center;">
          <span class="demand-score-pill demand-high" style="font-size: 0.85rem;">Demand ${demandStr}</span>
          <span class="badge badge-comp-${(kw.competition?.band || 'unmeasured').toLowerCase()}">${compBand}</span>
          <span class="badge badge-intent">${escapeHTML(kw.intent)}</span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr; gap: 8px; font-size: 0.88rem; background: #ffffff; padding: 10px 12px; border-radius: 6px; border: 1px solid #ebdccb;">
        <div><strong>SEO Title Tag:</strong> <code>${escapeHTML(bp.title)}</code></div>
        <div><strong>Meta Description:</strong> <span style="color: #645648;">${escapeHTML(bp.meta_description)}</span> <small style="color: #948372;">(${bp.meta_description?.length || 0} chars)</small></div>
        <div><strong>Target Word Count:</strong> ~${bp.target_word_count || 1200} words | <strong>Intelligence Layer:</strong> Groq LPU (Deterministic 0.0 temp)</div>
      </div>
    </div>

    <!-- Editorial Outline Hierarchy -->
    <div style="margin-bottom: 1.5rem;">
      <h3 style="font-size: 1rem; color: #271f18; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 6px;">
        <span>📑</span> Editorial Outline &amp; Heading Hierarchy
      </h3>
      ${outlineHtml}
    </div>

    <!-- FAQ & RankMath Schema Section -->
    ${faqHtml ? `
      <div>
        <h3 style="font-size: 1rem; color: #271f18; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 6px;">
          <span>❓</span> Frequently Asked Questions (PAA &amp; Schema)
        </h3>
        ${faqHtml}
      </div>
    ` : ''}
  `;
}

/* ==========================================================================
   Cross-Language Indic Seed Expansion Modal
   ========================================================================== */
function setupExpandSeedsEvents() {
  const expandBtn = document.getElementById('expand-indic-seeds-btn');
  const modal = document.getElementById('expand-seeds-modal');
  const closeBtn = document.getElementById('expand-seeds-close');
  const cancelBtn = document.getElementById('expand-seeds-cancel');
  const applyBtn = document.getElementById('expand-seeds-apply-btn');
  const listDiv = document.getElementById('expand-seeds-list');
  const seedsInput = document.getElementById('seeds-input');

  const closeModal = () => { if (modal) modal.style.display = 'none'; };
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

  if (expandBtn) {
    expandBtn.addEventListener('click', async () => {
      const currentSeeds = seedsInput.value.trim().split(/[\n,]/).map(s => s.trim()).filter(Boolean);
      const querySeed = currentSeeds[0] || 'शेती योजना';

      expandBtn.innerHTML = '⚡ Expanding...';

      try {
        const userKey = localStorage.getItem('praman_groq_api_key') || '';
        const resp = await fetch('/api/expand-seeds', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            seed: querySeed,
            language: (currentData && currentData.language) || 'mr',
            groq_api_key: userKey
          })
        });

        expandBtn.innerHTML = '🌐 Expand Indic (AI)';

        if (!resp.ok) {
          const errData = await resp.json().catch(() => ({}));
          throw new Error(errData.error || 'Failed to expand seeds');
        }

        const data = await resp.json();
        const variants = data.variants || [];

        if (variants.length === 0) {
          showToast('No variants discovered for this seed');
          return;
        }

        listDiv.innerHTML = variants.map((v, i) => `
          <label style="display: flex; align-items: flex-start; gap: 10px; background: #faf6ee; padding: 10px 12px; border-radius: 8px; border: 1px solid #ebdccb; cursor: pointer;">
            <input type="checkbox" class="expand-seed-checkbox" value="${escapeHTML(v.seed)}" checked style="margin-top: 3px;">
            <div>
              <div style="font-weight: 700; color: #271f18; font-size: 0.92rem;">
                <span class="badge" style="background:#e5dac9; color:#3c2814; font-size:0.72rem; margin-right:6px;">${v.language.toUpperCase()}</span>
                ${escapeHTML(v.seed)}
              </div>
              <div style="font-size: 0.8rem; color: #645648; margin-top: 2px;">${escapeHTML(v.explanation || '')}</div>
            </div>
          </label>
        `).join('');

        document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');
        modal.style.display = 'flex';
      } catch (err) {
        expandBtn.innerHTML = '🌐 Expand Indic (AI)';
        console.error('Error expanding seeds:', err);
        const isKey = err.message && (err.message.includes('Groq API key') || err.message.includes('key is not configured'));
        if (isKey) {
          const keyModal = document.getElementById('groq-key-modal');
          if (keyModal) {
            document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');
            keyModal.style.display = 'flex';
          }
          showToast('🔑 Please configure your free Groq API key first');
        } else {
          showToast(`Error discovering Indic variants: ${err.message}`);
        }
      }
    });
  }

  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      const selected = Array.from(document.querySelectorAll('.expand-seed-checkbox:checked')).map(cb => cb.value.trim());
      if (selected.length === 0) {
        showToast('Please select at least one seed');
        return;
      }

      const existing = seedsInput.value.trim();
      const prefix = existing ? existing + '\n' : '';
      seedsInput.value = prefix + selected.join('\n');

      closeModal();
      showToast(`✅ Added ${selected.length} authentic search seeds to queue!`);
      runResearch();
    });
  }
}

/* ==========================================================================
   Groq API Key Settings Modal
   ========================================================================== */
function setupGroqKeyEvents() {
  const btn = document.getElementById('groq-key-btn');
  const modal = document.getElementById('groq-key-modal');
  const closeBtn = document.getElementById('groq-key-modal-close');
  const cancelBtn = document.getElementById('groq-key-modal-cancel');
  const saveBtn = document.getElementById('groq-key-modal-save');
  const clearBtn = document.getElementById('groq-key-clear-btn');
  const input = document.getElementById('groq-key-input');

  const openModal = () => {
    if (!modal) return;
    document.querySelectorAll('.modal-backdrop').forEach(m => m.style.display = 'none');
    if (input) {
      input.value = localStorage.getItem('praman_groq_api_key') || '';
    }
    modal.style.display = 'flex';
    if (input) input.focus();
  };

  const closeModal = () => { if (modal) modal.style.display = 'none'; };

  if (btn) btn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      localStorage.removeItem('praman_groq_api_key');
      if (input) input.value = '';
      showToast('🗑️ Cleared stored Groq API key');
    });
  }

  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      const val = input ? input.value.trim() : '';
      if (!val) {
        showToast('Please enter a valid key or click Clear');
        return;
      }
      localStorage.setItem('praman_groq_api_key', val);
      closeModal();
      showToast('🔑 Groq API key saved successfully!');
    });
  }
}


