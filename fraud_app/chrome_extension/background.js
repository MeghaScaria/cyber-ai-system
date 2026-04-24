// 🚀 Fraud AI Shield - Background Service Worker (FINAL STABLE VERSION)

let debounceTimer;
let isAnalyzing = false;   // 🔒 prevent multiple scans


// ==========================
// 🚀 TAB SWITCH AUTO SCAN
// ==========================
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    const tab = await chrome.tabs.get(activeInfo.tabId);

    if (tab?.url && tab.url.startsWith("http")) {
      debounceAnalyze(activeInfo.tabId, tab.url);
    }
  } catch (err) {
    console.log("❌ Tab activation error:", err);
  }
});


// ==========================
// 🚀 PAGE LOAD AUTO SCAN
// ==========================
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {

  if (changeInfo.status === "complete" && tab?.url) {

    // 🚫 avoid extension page loop
    if (tab.url.includes("warning.html")) return;

    console.log("🌐 Page Loaded:", tab.url);

    // 🚨 browser error page
    if (
      tab.title?.includes("can't be reached") ||
      tab.url.includes("chrome-error")
    ) {

      const errorData = {
        fraud_score: 20,
        risk: "suspicious",
        reasons: ["Invalid or unreachable domain"],
        explanation: "⚠ This domain could not be reached. It may be unsafe."
      };

      chrome.storage.local.set({
        scanResult: errorData,
        originalUrl: tab.url
      });

      saveHistory(tab.url, errorData);
      return;
    }

    debounceAnalyze(tabId, tab.url);
  }
});


// ==========================
// 🚀 POPUP REQUEST HANDLER
// ==========================
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

  if (request.type === "CHECK_URL") {

    analyzeUrl(request.url, null)
      .then((data) => sendResponse({ success: true, data }))
      .catch(() => sendResponse({ success: false }));

    return true;
  }
});


// ==========================
// 🚀 MAIN ANALYSIS FUNCTION
// ==========================
async function analyzeUrl(url, tabId = null) {

  // 🔒 prevent duplicate execution
  if (isAnalyzing) return;
  isAnalyzing = true;

  try {
    console.log("🔍 Analyzing:", url);

    const response = await fetch("http://127.0.0.1:8000/analyze-url", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url })
    });

    const data = await response.json();

    const finalData = {
      fraud_score: data.fraud_score || 0,
      risk: data.risk || "safe",
      reasons: data.reasons || [],
      explanation: data.explanation || "",
      status: data.status || "valid"
    };

    console.log("📊 FINAL RESULT:", finalData);

    // ==========================
    // 🔥 CRITICAL FIX: WAIT FOR STORAGE
    // ==========================
    await new Promise((resolve) => {
      chrome.storage.local.set({
        scanResult: finalData,
        originalUrl: url
      }, resolve);
    });

    console.log("💾 DATA STORED SUCCESSFULLY");

    // 📊 SAVE HISTORY
    saveHistory(url, finalData);

    // ==========================
    // 🚨 BLOCK ONLY AFTER STORAGE
    // ==========================
    if (finalData.risk === "fraud-high" && tabId !== null) {

      chrome.tabs.get(tabId, (tab) => {
        if (!tab || tab.url.includes("warning.html")) return;

        chrome.tabs.update(tabId, {
          url: chrome.runtime.getURL("warning.html")
        });
      });
    }

    isAnalyzing = false;
    return finalData;

  } catch (error) {

    console.error("❌ API FAILED:", error);

    const fallback = {
      fraud_score: 50,
      risk: "suspicious",
      reasons: ["Unable to verify website"],
      explanation: "⚠ Could not analyze this site. Proceed with caution."
    };

    await new Promise((resolve) => {
      chrome.storage.local.set({
        scanResult: fallback,
        originalUrl: url
      }, resolve);
    });

    saveHistory(url, fallback);

    isAnalyzing = false;
    return fallback;
  }
}


// ==========================
// 🚀 HISTORY STORAGE
// ==========================
function saveHistory(url, result) {

  chrome.storage.local.get("history", (data) => {

    let history = data.history || [];

    history.unshift({
      url: url,
      score: result.fraud_score,
      risk: result.risk,
      time: new Date().toLocaleString()
    });

    history = history.slice(0, 20);

    chrome.storage.local.set({ history });
  });
}


// ==========================
// 🚀 DEBOUNCE
// ==========================
function debounceAnalyze(tabId, url) {

  clearTimeout(debounceTimer);

  debounceTimer = setTimeout(() => {
    analyzeUrl(url, tabId);
  }, 500);
}