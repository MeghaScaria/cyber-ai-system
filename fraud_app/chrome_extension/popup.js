document.addEventListener("DOMContentLoaded", () => {

  // 🔹 ELEMENTS
  const btn = document.getElementById("checkBtn");
  const loader = document.getElementById("loader");
  const status = document.getElementById("status");
  const scoreText = document.getElementById("scoreText");
  const quote = document.getElementById("quote");
  const refreshBtn = document.getElementById("refreshQuote");
  const quoteBox = document.querySelector(".quote-glass");

  const reasonsList = document.getElementById("reasonsList");
  const explanationText = document.getElementById("explanationText");
  const openHistoryBtn = document.getElementById("openHistory");

  const canvas = document.getElementById("scoreCanvas");
  const ctx = canvas.getContext("2d");

  const bg = document.getElementById("bgCanvas");
  const bgCtx = bg.getContext("2d");

  const alertSound = new Audio(chrome.runtime.getURL("alert.mp3"));

  let currentState = "safe";
  let currentColor = "#00ff99";

  // ==========================
  // 🌌 BACKGROUND ANIMATION
  // ==========================
  bg.width = window.innerWidth;
  bg.height = window.innerHeight;

  let particles = Array.from({ length: 40 }, () => ({
    x: Math.random() * bg.width,
    y: Math.random() * bg.height,
    size: Math.random() * 2,
    speed: Math.random() * 1 + 0.5
  }));

  function animateBg() {
    bgCtx.clearRect(0, 0, bg.width, bg.height);

    bgCtx.fillStyle = currentColor;
    bgCtx.shadowBlur = 10;
    bgCtx.shadowColor = currentColor;

    particles.forEach(p => {
      p.y += p.speed;
      if (p.y > bg.height) p.y = 0;
      bgCtx.fillRect(p.x, p.y, p.size, p.size);
    });

    requestAnimationFrame(animateBg);
  }

  animateBg();

  // ==========================
  // 💬 QUOTES
  // ==========================
  const safeQuotes = ["You're safe online 👍", "Enjoy browsing ✨"];
  const warningQuotes = ["Be careful ⚠", "Looks suspicious 👀"];
  const dangerQuotes = ["Avoid immediately 🚫", "High risk ⚠"];

  function getRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // ==========================
  // 🎯 DRAW METER
  // ==========================
  function drawMeter(score, color) {
    ctx.clearRect(0, 0, 120, 120);

    ctx.beginPath();
    ctx.arc(60, 60, 50, 0, Math.PI * 2);
    ctx.strokeStyle = "#222";
    ctx.lineWidth = 10;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(
      60,
      60,
      50,
      -Math.PI / 2,
      (Math.PI * 2 * score / 100) - Math.PI / 2
    );
    ctx.strokeStyle = color;
    ctx.lineWidth = 10;
    ctx.stroke();

    ctx.fillStyle = "white";
    ctx.font = "16px Arial";
    ctx.textAlign = "center";
    ctx.fillText(score + "%", 60, 65);
  }

  // ==========================
  // 🚀 DISPLAY RESULT
  // ==========================
  function displayResult(data) {

    if (!data) {
      status.innerText = "⚠ No data";
      return;
    }

    const score = data.fraud_score || 0;

    reasonsList.innerHTML = "";
    explanationText.innerText = data.explanation || "";

    if (data.reasons?.length) {
      data.reasons.forEach(reason => {
        const li = document.createElement("li");
        li.textContent = "• " + reason;
        reasonsList.appendChild(li);
      });
    }

    if (data.risk === "fraud-high") {
      currentState = "danger";
      currentColor = "#ff4d4d";

      status.innerText = "🚨 Fraud Detected";
      status.style.color = currentColor;

      quote.innerText = getRandom(dangerQuotes);
      quote.style.color = currentColor;

      quoteBox.style.border = "1px solid rgba(255,77,77,0.5)";
      alertSound.play();
    }

    else if (data.risk === "suspicious") {
      currentState = "warning";
      currentColor = "#ffd93d";

      status.innerText = "⚠ Suspicious";
      status.style.color = currentColor;

      quote.innerText = getRandom(warningQuotes);
      quote.style.color = currentColor;

      quoteBox.style.border = "1px solid rgba(255,217,61,0.5)";
    }

    else {
      currentState = "safe";
      currentColor = "#00ff99";

      status.innerText = "✔ Safe";
      status.style.color = currentColor;

      quote.innerText = getRandom(safeQuotes);
      quote.style.color = currentColor;

      quoteBox.style.border = "1px solid rgba(0,255,150,0.5)";
    }

    drawMeter(score, currentColor);
    scoreText.innerText = "Risk Score: " + score + "%";
  }

  // ==========================
  // 🔥 AUTO LOAD (NO API CALL)
  // ==========================
  chrome.storage.local.get("scanResult", (res) => {
    displayResult(res.scanResult);
  });

  // ==========================
  // 🔘 MANUAL SCAN (TRIGGER BACKGROUND ONLY)
  // ==========================
  btn.addEventListener("click", async () => {

    btn.disabled = true;
    loader.classList.remove("hidden");

    let [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true
    });

    // 👇 ONLY TRIGGER BACKGROUND
    chrome.runtime.sendMessage({
      type: "CHECK_URL",
      url: tab.url
    });

    // wait a bit then read updated result
    setTimeout(() => {
      chrome.storage.local.get("scanResult", (res) => {
        displayResult(res.scanResult);
        loader.classList.add("hidden");
        btn.disabled = false;
      });
    }, 800);
  });

  // ==========================
  // 🔄 REFRESH QUOTE
  // ==========================
  refreshBtn.addEventListener("click", () => {
    if (currentState === "danger") quote.innerText = getRandom(dangerQuotes);
    else if (currentState === "warning") quote.innerText = getRandom(warningQuotes);
    else quote.innerText = getRandom(safeQuotes);
  });

  // ==========================
  // 📊 HISTORY
  // ==========================
  openHistoryBtn.addEventListener("click", () => {
    chrome.tabs.create({
      url: chrome.runtime.getURL("history.html")
    });
  });

});