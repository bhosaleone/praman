/**
 * Praman SERP Companion — Popup Script
 */

document.addEventListener('DOMContentLoaded', async () => {
  const activeView = document.getElementById('active-serp-view');
  const inactiveView = document.getElementById('inactive-view');
  const queryText = document.getElementById('query-text');
  const bandBadge = document.getElementById('band-badge');
  const weakSignal = document.getElementById('weak-signal');
  const thinSignal = document.getElementById('thin-signal');
  const staleSignal = document.getElementById('stale-signal');
  const copyBtn = document.getElementById('copy-serp-btn');
  const sendBtn = document.getElementById('send-praman-btn');
  const recentList = document.getElementById('recent-list');
  const clearBtn = document.getElementById('clear-history-btn');

  let currentObservation = null;

  // Load recent observations from storage
  function loadRecent() {
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
      chrome.storage.local.get(['pramanObservations'], (res) => {
        const obs = res.pramanObservations || {};
        const keys = Object.keys(obs);
        if (keys.length === 0) {
          recentList.innerHTML = '<em>No recent queries analyzed yet.</em>';
          return;
        }

        recentList.innerHTML = '';
        keys.slice(-5).reverse().forEach(k => {
          const item = obs[k];
          const div = document.createElement('div');
          div.style.cssText = 'padding: 4px 0; border-bottom: 1px solid #f4ece0; display:flex; justify-content:space-between; align-items:center;';
          div.innerHTML = `
            <span style="font-weight:600; max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${k}">${k}</span>
            <span style="font-size:10px; font-weight:800; color:#ea580c;">${(item.band || 'review').toUpperCase()}</span>
          `;
          recentList.appendChild(div);
        });
      });
    }
  }

  loadRecent();

  clearBtn.addEventListener('click', () => {
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
      chrome.storage.local.set({ pramanObservations: {} }, () => {
        loadRecent();
      });
    }
  });

  // Query active tab
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url || (!tab.url.includes('google.com/search') && !tab.url.includes('google.co.in/search'))) {
    activeView.style.display = 'none';
    inactiveView.style.display = 'block';
    return;
  }

  // Ask content script for observation
  try {
    chrome.tabs.sendMessage(tab.id, { action: 'getSerpObservation' }, (response) => {
      if (chrome.runtime.lastError || !response || !response.observation) {
        queryText.innerText = 'Run a search on Google to analyze';
        bandBadge.innerText = 'No SERP Data';
        return;
      }

      const obs = response.observation;
      currentObservation = obs;

      queryText.innerText = obs.keyword;
      
      const band = obs.band || 'unmeasured';
      bandBadge.className = `badge badge-${band}`;
      bandBadge.innerText = band.toUpperCase();

      weakSignal.innerText = obs.weak === true ? '⚠️ Yes (Forums/UGC)' : (obs.weak === false ? '✅ No (Strong Domains)' : 'Uncertain');
      weakSignal.style.color = obs.weak === true ? '#15803d' : (obs.weak === false ? '#be123c' : '#645648');

      thinSignal.innerText = obs.thin === true ? '⚠️ Yes (Missing Match)' : (obs.thin === false ? '✅ No (Exact Match)' : 'Uncertain');
      thinSignal.style.color = obs.thin === true ? '#15803d' : (obs.thin === false ? '#be123c' : '#645648');

      staleSignal.innerText = obs.stale === true ? '⚠️ Yes (> 2 yrs old)' : (obs.stale === false ? '✅ No (Fresh 2025/2026)' : 'Uncertain');
      staleSignal.style.color = obs.stale === true ? '#15803d' : (obs.stale === false ? '#be123c' : '#645648');
    });
  } catch (e) {
    console.error('Error contacting content script:', e);
  }

  // Copy button
  copyBtn.addEventListener('click', () => {
    if (!currentObservation) return;
    const text = JSON.stringify(currentObservation, null, 2);
    navigator.clipboard.writeText(text).then(() => {
      copyBtn.innerText = '✅ Copied to Clipboard!';
      setTimeout(() => copyBtn.innerText = '📋 Copy SERP Data', 2000);
    });
  });

  // Send to Praman button
  sendBtn.addEventListener('click', async () => {
    if (!currentObservation) return;

    // Check if Praman tab is already open
    const allTabs = await chrome.tabs.query({});
    const pramanTab = allTabs.find(t => t.url && (t.url.includes('praman.blog') || t.url.includes('localhost:8000')));

    const dataPayload = encodeURIComponent(JSON.stringify(currentObservation));

    sendBtn.innerText = '⚡ Connecting...';

    if (pramanTab) {
      // Focus existing tab and execute import
      await chrome.tabs.update(pramanTab.id, { active: true });
      await chrome.windows.update(pramanTab.windowId, { focused: true });
      chrome.tabs.sendMessage(pramanTab.id, { 
        action: 'importPramanSerp', 
        observation: currentObservation 
      });
      sendBtn.innerText = '⚡ Sent to Praman!';
      setTimeout(() => sendBtn.innerText = '⚡ Open in Praman', 2000);
    } else {
      // Open new Praman tab with query parameter
      const targetUrl = `https://www.praman.blog/?import_serp=${dataPayload}`;
      chrome.tabs.create({ url: targetUrl });
      sendBtn.innerText = '⚡ Opened in Praman!';
      setTimeout(() => sendBtn.innerText = '⚡ Open in Praman', 2000);
    }
  });

});
