/**
 * Praman SERP Companion — Background Service Worker (Manifest V3)
 * 
 * Manages extension lifecycle, badge counts, and context menu integrations.
 * 100% compliant with Google Terms of Service:
 * - Operates entirely client-side.
 * - Does not perform automated scraping, headless queries, or bypass any rate limits.
 */

// Lifecycle setup
chrome.runtime.onInstalled.addListener((details) => {
  console.log('[Praman SERP Companion] Installed successfully (reason:', details.reason, ')');

  // Initialize storage if empty
  chrome.storage.local.get(['pramanObservations'], (res) => {
    if (!res.pramanObservations) {
      chrome.storage.local.set({ pramanObservations: {} });
    }
  });

  // Create context menu for quick Praman search
  chrome.contextMenus.create({
    id: 'praman-search-selection',
    title: 'Inspect SERP on Google with Praman ("%s")',
    contexts: ['selection']
  });
});

// Context menu click listener
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'praman-search-selection' && info.selectionText) {
    const query = encodeURIComponent(info.selectionText.trim());
    chrome.tabs.create({ url: `https://www.google.com/search?q=${query}` });
  }
});

// Handle messages from content script or popup to focus or open Praman
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'openPraman' && request.observation) {
    (async () => {
      const allTabs = await chrome.tabs.query({});
      const pramanTab = allTabs.find(t => t.url && (t.url.includes('praman.blog') || t.url.includes('localhost:8000') || t.url.includes('127.0.0.1:8000')));

      if (pramanTab) {
        await chrome.tabs.update(pramanTab.id, { active: true });
        if (pramanTab.windowId) {
          await chrome.windows.update(pramanTab.windowId, { focused: true });
        }
        chrome.tabs.sendMessage(pramanTab.id, {
          action: 'importPramanSerp',
          observation: request.observation
        });
      } else {
        const encoded = encodeURIComponent(JSON.stringify(request.observation));
        const targetUrl = `https://www.praman.blog/?import_serp=${encoded}`;
        await chrome.tabs.create({ url: targetUrl });
      }
      sendResponse({ status: 'ok' });
    })();
    return true; // Keep sendResponse open for async
  }
});

