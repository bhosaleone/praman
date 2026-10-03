/**
 * Praman SERP Companion — Content Script
 * 
 * Automatically analyzes Google Search Results for:
 * 1. Weak Domains (UGC, Forums, Quora, Reddit, Medium, Free Blogs)
 * 2. Stale Content (Published/Updated > 2 years ago)
 * 3. Thin Results (Missing exact title matches, low snippet relevance)
 * 
 * Complies 100% with Google Terms of Service (runs only in human browser session).
 */

(function () {
  'use strict';

  // Prevent double injection
  if (window.__pramanInjected) return;
  window.__pramanInjected = true;

  const WEAK_DOMAIN_PATTERNS = [
    'quora.com', 'reddit.com', 'pinterest.com', 'facebook.com', 
    'instagram.com', 'twitter.com', 'x.com', 'medium.com', 
    'blogspot.com', 'wordpress.com', 'answers.com', 'wikihow.com',
    'linkedin.com/pulse', 'tumblr.com'
  ];

  const STRONG_DOMAIN_PATTERNS = [
    '.gov.in', '.nic.in', 'wikipedia.org', 'lokmat.com', 'esakal.com',
    'abplive.com', 'ndtv.com', 'indiatimes.com', 'thehindu.com', 
    'indianexpress.com', 'jagran.com', 'amarujala.com', 'vikatan.com',
    'eenadu.net', 'investopedia.com', 'rbi.org.in', 'sebi.gov.in'
  ];

  function getSearchQuery() {
    const urlParams = new URLSearchParams(window.location.search);
    const qUrl = urlParams.get('q');
    if (qUrl) return qUrl.trim();

    const input = document.querySelector('textarea[name="q"], input[name="q"]');
    return input ? input.value.trim() : '';
  }

  function analyzeSerp() {
    const query = getSearchQuery();
    if (!query) return null;

    // Grab organic result cards
    // Google uses various classes: .g, div[data-hveid], div[data-sokoban-container]
    const resultElements = Array.from(document.querySelectorAll('#rso > div, #rso .g, div.MjjYud'))
      .filter(el => {
        // Must contain an anchor and an h3 heading
        const link = el.querySelector('a[href^="http"]');
        const h3 = el.querySelector('h3');
        return link && h3 && !link.href.includes('google.com');
      });

    const parsedResults = [];
    const seenUrls = new Set();

    for (const el of resultElements) {
      const a = el.querySelector('a[href^="http"]');
      const h3 = el.querySelector('h3');
      if (!a || !h3) continue;

      let href = a.href;
      try {
        const u = new URL(href);
        const host = u.hostname.replace(/^www\./, '').toLowerCase();
        if (seenUrls.has(host + u.pathname)) continue;
        seenUrls.add(host + u.pathname);

        const title = h3.innerText.trim();
        const snippetText = el.innerText || '';

        parsedResults.push({
          domain: host,
          url: href,
          title: title,
          snippet: snippetText.slice(0, 300)
        });
      } catch (e) {
        // ignore invalid urls
      }

      if (parsedResults.length >= 10) break;
    }

    if (parsedResults.length === 0) return null;

    // 1. Weak Domains Analysis (Top 5)
    const top5 = parsedResults.slice(0, 5);
    let weakCount = 0;
    let strongCount = 0;

    top5.forEach(r => {
      const isWeak = WEAK_DOMAIN_PATTERNS.some(w => r.domain.includes(w) || r.url.includes(w));
      const isStrong = STRONG_DOMAIN_PATTERNS.some(s => r.domain.endsWith(s) || r.domain === s);
      if (isWeak) weakCount++;
      if (isStrong) strongCount++;
    });

    let weakDomains = null;
    if (weakCount >= 2) {
      weakDomains = true;
    } else if (strongCount >= 3) {
      weakDomains = false;
    } else if (weakCount === 1) {
      weakDomains = true;
    } else if (strongCount >= 1) {
      weakDomains = false;
    }

    // 2. Stale Content Analysis
    // Look for dates: e.g., "15 Jan 2021", "2022", "3 years ago"
    const currentYear = new Date().getFullYear();
    let staleCount = 0;
    let freshCount = 0;

    top5.forEach(r => {
      const dateMatch = r.snippet.match(/\b(20[12][0-9])\b/);
      const relativeMatch = r.snippet.match(/(\d+)\s+(years?|months?)\s+ago/i);

      if (dateMatch) {
        const year = parseInt(dateMatch[1], 10);
        if (currentYear - year >= 2) {
          staleCount++;
        } else {
          freshCount++;
        }
      } else if (relativeMatch) {
        const num = parseInt(relativeMatch[1], 10);
        const unit = relativeMatch[2].toLowerCase();
        if (unit.startsWith('year') && num >= 2) {
          staleCount++;
        } else {
          freshCount++;
        }
      }
    });

    let topResultsStale = null;
    if (staleCount >= 2) {
      topResultsStale = true;
    } else if (freshCount >= 2) {
      topResultsStale = false;
    }

    // 3. Thin Results Analysis
    // Check if query tokens appear in titles of top 5 results
    const queryTokens = query.toLowerCase().split(/\s+/).filter(w => w.length > 2);
    let titleMatchCount = 0;

    top5.forEach(r => {
      const titleLower = r.title.toLowerCase();
      const match = queryTokens.some(tok => titleLower.includes(tok));
      if (match) titleMatchCount++;
    });

    // Check if Google showed "No good matches" banner
    const noMatchesFound = document.body.innerText.includes("It looks like there aren't many great matches") ||
                           document.body.innerText.includes("या शोधासाठी फारसे उत्तम निकाल दिसत नाहीत");

    let thinResults = null;
    if (noMatchesFound || titleMatchCount <= 1) {
      thinResults = true;
    } else if (titleMatchCount >= 3) {
      thinResults = false;
    }

    // 4. Derive Competition Band (Matching Praman competition.py)
    let band = deriveCompetitionBand(thinResults, weakDomains, topResultsStale);

    // Summary Notes
    const notesArr = [];
    if (weakDomains === true) notesArr.push(`Weak domains in top 5 (${top5.map(t => t.domain).slice(0, 3).join(', ')})`);
    if (topResultsStale === true) notesArr.push('Top results >2 yrs old');
    if (thinResults === true) notesArr.push('Titles lack exact query match');
    if (!notesArr.length) notesArr.push(`Ranked by: ${top5.map(t => t.domain).slice(0, 3).join(', ')}`);

    const observation = {
      keyword: query,
      thin: thinResults,
      weak: weakDomains,
      stale: topResultsStale,
      band: band,
      notes: notesArr.join('; '),
      topDomains: top5.map(t => t.domain),
      resultsCount: parsedResults.length,
      timestamp: new Date().toISOString()
    };

    return observation;
  }

  function deriveCompetitionBand(thin, weak, stale) {
    const fields = [thin, weak, stale];
    const recorded = fields.filter(f => f !== null).length;
    if (recorded < 2) return null;

    if (weak === true) return thin === true ? 'low' : 'medium';
    if (weak === false) return thin === false ? 'very_high' : 'high';
    if (thin === true && stale === true) return 'medium';
    if (thin === false && stale === false) return 'high';
    return 'medium';
  }

  // Render floating Praman widget on Google SERP
  function injectPramanFloatingWidget(obs) {
    if (!obs) return;

    const existing = document.getElementById('praman-serp-widget');
    if (existing) existing.remove();

    const widget = document.createElement('div');
    widget.id = 'praman-serp-widget';
    
    const bandColors = {
      'low': '#15803d',
      'medium': '#d97706',
      'high': '#ea580c',
      'very_high': '#be123c',
      'null': '#948372'
    };

    const color = bandColors[obs.band] || '#ea580c';
    const bandLabel = obs.band ? obs.band.toUpperCase() : 'NEEDS REVIEW';

    widget.innerHTML = `
      <div style="
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 999999;
        background: #ffffff;
        border: 2px solid #dfd2be;
        border-radius: 14px;
        box-shadow: 0 10px 30px rgba(60, 40, 20, 0.18);
        padding: 14px 18px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        color: #271f18;
        max-width: 340px;
        display: flex;
        flex-direction: column;
        gap: 10px;
      ">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e5dac9; padding-bottom:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <div style="width:24px; height:24px; background:#ea580c; border-radius:6px; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:13px;">प्र</div>
            <strong style="font-size:13px; color:#271f18;">Praman SERP Companion</strong>
          </div>
          <button id="praman-close-btn" style="background:none; border:none; color:#948372; font-size:18px; cursor:pointer; line-height:1;">&times;</button>
        </div>

        <div>
          <div style="font-size:11px; color:#645648; text-transform:uppercase; letter-spacing:0.05em; font-weight:700;">Analyzed Keyword</div>
          <div style="font-size:13px; font-weight:700; color:#271f18; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${obs.keyword}">
            ${obs.keyword}
          </div>
        </div>

        <div style="display:flex; align-items:center; justify-content:space-between; background:#faf6ee; padding:8px 10px; border-radius:8px;">
          <span style="font-size:12px; font-weight:600; color:#645648;">Competition Band:</span>
          <span style="font-size:11px; font-weight:800; color:#ffffff; background:${color}; padding:3px 8px; border-radius:6px; letter-spacing:0.04em;">
            ${bandLabel}
          </span>
        </div>

        <div style="font-size:11px; color:#645648; line-height:1.4;">
          <strong>Signals:</strong> Weak: ${obs.weak ? 'Yes' : (obs.weak === false ? 'No' : 'N/A')} | 
          Thin: ${obs.thin ? 'Yes' : (obs.thin === false ? 'No' : 'N/A')} | 
          Stale: ${obs.stale ? 'Yes' : (obs.stale === false ? 'No' : 'N/A')}
        </div>

        <div style="display:flex; gap:8px; margin-top:2px;">
          <button id="praman-copy-btn" style="
            flex: 1;
            background: #f4ece0;
            border: 1px solid #dfd2be;
            color: #271f18;
            font-size: 11px;
            font-weight: 700;
            padding: 8px 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
          ">📋 Copy Data</button>

          <button id="praman-send-btn" style="
            flex: 1;
            background: linear-gradient(135deg, #f97316, #ea580c);
            border: none;
            color: #ffffff;
            font-size: 11px;
            font-weight: 700;
            padding: 8px 10px;
            border-radius: 6px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(234, 88, 12, 0.3);
          ">⚡ Open in Praman</button>
        </div>
      </div>
    `;

    document.body.appendChild(widget);

    // Save to storage
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
      chrome.storage.local.get(['pramanObservations'], (res) => {
        const list = res.pramanObservations || {};
        list[obs.keyword] = obs;
        chrome.storage.local.set({ pramanObservations: list });
      });
    }

    // Copy event
    const copyBtn = document.getElementById('praman-copy-btn');
    copyBtn.addEventListener('click', () => {
      const jsonStr = JSON.stringify(obs, null, 2);
      navigator.clipboard.writeText(jsonStr).then(() => {
        copyBtn.innerText = '✅ Copied!';
        setTimeout(() => copyBtn.innerText = '📋 Copy Data', 2000);
      });
    });

    // Send to Praman
    const sendBtn = document.getElementById('praman-send-btn');
    sendBtn.addEventListener('click', () => {
      sendBtn.innerText = '⚡ Connecting...';
      if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.sendMessage) {
        chrome.runtime.sendMessage({ action: 'openPraman', observation: obs }, (res) => {
          sendBtn.innerText = '⚡ Sent!';
          setTimeout(() => sendBtn.innerText = '⚡ Open in Praman', 2000);
          if (chrome.runtime.lastError) {
            const encoded = encodeURIComponent(JSON.stringify(obs));
            window.open(`https://www.praman.blog/?import_serp=${encoded}`, '_blank');
          }
        });
      } else {
        const encoded = encodeURIComponent(JSON.stringify(obs));
        window.open(`https://www.praman.blog/?import_serp=${encoded}`, '_blank');
        sendBtn.innerText = '⚡ Sent!';
        setTimeout(() => sendBtn.innerText = '⚡ Open in Praman', 2000);
      }
    });

    // Close button
    const closeBtn = document.getElementById('praman-close-btn');
    closeBtn.addEventListener('click', () => {
      widget.remove();
    });
  }

  // Run analysis when page loads
  setTimeout(() => {
    const obs = analyzeSerp();
    if (obs) {
      injectPramanFloatingWidget(obs);
    }
  }, 1000);

  // Listen for messages from popup
  if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'getSerpObservation') {
        const obs = analyzeSerp();
        sendResponse({ observation: obs });
      }
    });
  }

})();
