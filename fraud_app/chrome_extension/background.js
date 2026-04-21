// 🚀 Fraud AI Shield - Background Service Worker (FINAL FIXED)

// 🔥 Debounce timer
let debounceTimer;


// 🚀 AUTO SCAN ON TAB SWITCH
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    const tab = await chrome.tabs.get(activeInfo.tabId);

    if (tab?.url && tab.url.startsWith("http")) {
      debounceAnalyze(tab.url);
    }
  } catch (err) {
    console.log("❌ Tab activation error:", err);
  }
});


// 🚀 AUTO SCAN ON PAGE LOAD
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {

  if (changeInfo.status === "complete" && tab?.url) {

    console.log("🌐 Page Loaded:", tab.url);

    // 🚨 FIX: Detect browser error pages (NXDOMAIN)
    if (
      tab.title?.includes("can't be reached") ||
      tab.url.includes("chrome-error")
    ) {

      console.log("🚨 Browser error detected → Suspicious");

      const errorData = {
        fraud_score: 60,
        risk: "suspicious"
      };

      chrome.storage.local.set({ scanResult: errorData });
      return;
    }

    if (tab.url.startsWith("http")) {
      debounceAnalyze(tab.url);
    }
  }
});


// 🚀 POPUP BUTTON REQUEST
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

  if (request.type === "CHECK_URL") {

    console.log("🟢 Popup requested scan:", request.url);

    analyzeUrl(request.url)
      .then((data) => {
        sendResponse({ success: true, data });
      })
      .catch((err) => {
        console.error("❌ API Error:", err);
        sendResponse({ success: false });
      });

    return true;
  }
});


// 🚀 MAIN ANALYSIS FUNCTION
async function analyzeUrl(url) {

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

    console.log("✅ API Response:", data);

    // 🔥 NORMALIZE DATA
    const score = data.fraud_score || 0;

    let risk = data.risk;

    if (!risk) {
      if (score > 70) risk = "fraud-high";
      else if (score > 40) risk = "suspicious";
      else risk = "safe";
    }

    const finalData = {
      fraud_score: score,
      risk: risk
    };

    // 🔥 STORE RESULT
    chrome.storage.local.set({ scanResult: finalData });

    // 🚫 BLOCK FRAUD SITES ONLY
    if (risk === "fraud-high") {

      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]?.id) {
          chrome.tabs.update(tabs[0].id, {
            url: chrome.runtime.getURL("warning.html")
          });
        }
      });
    }

    return finalData;

  } catch (error) {
    console.error("❌ Fetch failed:", error);

    // 🟡 IMPORTANT FIX → network/API fail = suspicious (NOT safe)
    const fallback = {
      fraud_score: 50,
      risk: "suspicious"
    };

    chrome.storage.local.set({ scanResult: fallback });

    return fallback;
  }
}


// 🚀 DEBOUNCE (PREVENT SPAM CALLS)
function debounceAnalyze(url) {
  clearTimeout(debounceTimer);

  debounceTimer = setTimeout(() => {
    analyzeUrl(url);
  }, 500);
}