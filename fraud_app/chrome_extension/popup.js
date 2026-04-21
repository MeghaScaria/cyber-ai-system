document.addEventListener("DOMContentLoaded", () => {

  // 🔹 ELEMENTS
  const btn = document.getElementById("checkBtn");
  const loader = document.getElementById("loader");
  const status = document.getElementById("status");
  const scoreText = document.getElementById("scoreText");
  const quote = document.getElementById("quote");
  const refreshBtn = document.getElementById("refreshQuote");
  const quoteBox = document.querySelector(".quote-glass");

  const canvas = document.getElementById("scoreCanvas");
  const ctx = canvas.getContext("2d");

  const bg = document.getElementById("bgCanvas");
  const bgCtx = bg.getContext("2d");

  // 🔥 STATE
  let currentState = "safe";
  let isLoading = false;
  let currentColor = "#00ff99";

  // 🌌 BACKGROUND SIZE
  bg.width = window.innerWidth;
  bg.height = window.innerHeight;

  // 🔥 PARTICLES
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

  // 🔥 QUOTES
  const safeQuotes = ["You're safe online 👍", "Enjoy browsing ✨"];
  const warningQuotes = ["Be careful ⚠", "Looks suspicious 👀"];
  const dangerQuotes = ["Avoid immediately 🚫", "High risk ⚠"];

  function getRandom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  // 🎯 DRAW METER
  function drawMeter(score) {
    ctx.clearRect(0, 0, 120, 120);

    let color = "#00ff99";
    if (score > 70) color = "#ff4d4d";
    else if (score > 40) color = "#ffd93d";

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

  // 🚀 DISPLAY RESULT
  function displayResult(data) {

    const score = data.fraud_score || 0;

    // 🔴 FRAUD
    if (data.risk === "fraud-high") {
      currentState = "danger";
      currentColor = "#ff4d4d";

      status.innerText = "⚠ Fraud Detected";
      status.style.color = "#ff4d4d";

      quote.innerText = getRandom(dangerQuotes);
      quote.style.color = "#ff4d4d";

      quoteBox.style.border = "1px solid rgba(255,77,77,0.5)";
    }

    // 🟡 SUSPICIOUS
    else if (data.risk === "suspicious" || score > 40) {
      currentState = "warning";
      currentColor = "#ffd93d";

      status.innerText = "⚠ Suspicious Website";
      status.style.color = "#ffd93d";

      quote.innerText = getRandom(warningQuotes);
      quote.style.color = "#ffd93d";

      quoteBox.style.border = "1px solid rgba(255,217,61,0.5)";
    }

    // 🟢 SAFE
    else {
      currentState = "safe";
      currentColor = "#00ff99";

      status.innerText = "✔ Safe Website";
      status.style.color = "#00ff99";

      quote.innerText = getRandom(safeQuotes);
      quote.style.color = "#00ff99";

      quoteBox.style.border = "1px solid rgba(0,255,150,0.5)";
    }

    drawMeter(score);
    scoreText.innerText = "Risk Score: " + score + "%";
  }

  // 🔄 REFRESH QUOTE
  refreshBtn.addEventListener("click", () => {
    if (currentState === "danger") quote.innerText = getRandom(dangerQuotes);
    else if (currentState === "warning") quote.innerText = getRandom(warningQuotes);
    else quote.innerText = getRandom(safeQuotes);
  });

  // 🚀 BUTTON CLICK
  btn.addEventListener("click", async () => {

    if (isLoading) return;

    isLoading = true;
    btn.disabled = true;
    loader.classList.remove("hidden");

    let [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true
    });

    chrome.runtime.sendMessage(
      { type: "CHECK_URL", url: tab.url },
      (response) => {

        loader.classList.add("hidden");

        if (!response || !response.success) {
          status.innerText = "API Error";
        } else {
          displayResult(response.data);
        }

        isLoading = false;
        btn.disabled = false;
      }
    );
  });

});