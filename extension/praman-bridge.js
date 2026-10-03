/**
 * Praman SERP Companion — Bridge Script
 * 
 * Runs on Praman web application (praman.blog and localhost:8000).
 * Acts as a secure message bridge between the Chrome Extension
 * and the Praman web interface.
 */

(function () {
  'use strict';

  // Inform the web app that the Praman extension is installed & active
  window.sessionStorage.setItem('PRAMAN_EXTENSION_ACTIVE', 'true');
  window.postMessage({ type: 'PRAMAN_EXTENSION_READY', version: '1.0.0' }, '*');

  // Listen for messages dispatched from popup.js or content.js
  if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'importPramanSerp' && request.observation) {
        // Forward observation to web application context via postMessage
        window.postMessage({
          type: 'PRAMAN_SERP_IMPORT',
          observation: request.observation
        }, '*');

        sendResponse({ received: true });
      }
    });
  }
})();
