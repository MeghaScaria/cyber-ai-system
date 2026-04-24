document.addEventListener("DOMContentLoaded", () => {

  const scoreText = document.getElementById("scoreText");
  const statusEl = document.getElementById("status");
  const explanationEl = document.getElementById("explanation");
  const reasonsEl = document.getElementById("reasons");
  const titleEl = document.getElementById("title");

  const canvas = document.getElementById("progressRing");
  const ctx = canvas.getContext("2d");

  const bgCanvas = document.getElementById("bgRing");
  const bgCtx = bgCanvas.getContext("2d");

  // 🌧️ RAIN CANVAS (single instance)
  let rainCanvas = document.getElementById("rainCanvas");

  if (!rainCanvas) {
    rainCanvas = document.createElement("canvas");
    rainCanvas.id = "rainCanvas";
    document.body.appendChild(rainCanvas);
  }

  const rainCtx = rainCanvas.getContext("2d");

  rainCanvas.style.position = "fixed";
  rainCanvas.style.top = 0;
  rainCanvas.style.left = 0;
  rainCanvas.style.width = "100%";
  rainCanvas.style.height = "100%";
  rainCanvas.style.zIndex = "-1";

  rainCanvas.width = window.innerWidth;
  rainCanvas.height = window.innerHeight;

  // 🎯 Background ring
  bgCtx.beginPath();
  bgCtx.arc(65, 65, 55, 0, 2 * Math.PI);
  bgCtx.strokeStyle = "#222";
  bgCtx.lineWidth = 8;
  bgCtx.stroke();

  // ==========================
  // 🌧️ RAIN CONTROL
  // ==========================
  let rainAnimationId = null;

  function stopRain() {
    if (rainAnimationId) {
      cancelAnimationFrame(rainAnimationId);
      rainAnimationId = null;
    }
    rainCtx.clearRect(0, 0, rainCanvas.width, rainCanvas.height);
  }

  function startRain(color) {

    stopRain(); // 🔥 prevent duplicate rain

    const drops = Array.from({ length: 120 }, () => ({
      x: Math.random() * rainCanvas.width,
      y: Math.random() * rainCanvas.height,
      length: Math.random() * 20 + 10,
      speed: Math.random() * 4 + 2
    }));

    function drawRain() {
      rainCtx.clearRect(0, 0, rainCanvas.width, rainCanvas.height);

      rainCtx.strokeStyle = color;
      rainCtx.lineWidth = 1;

      drops.forEach(d => {
        rainCtx.beginPath();
        rainCtx.moveTo(d.x, d.y);
        rainCtx.lineTo(d.x, d.y + d.length);
        rainCtx.stroke();

        d.y += d.speed;

        if (d.y > rainCanvas.height) {
          d.y = 0;
          d.x = Math.random() * rainCanvas.width;
        }
      });

      rainAnimationId = requestAnimationFrame(drawRain);
    }

    drawRain();
  }

  // ==========================
  // ✅ LOAD DATA (ONLY STORAGE)
  // ==========================
  chrome.storage.local.get("scanResult", (res) => {

    const data = res.scanResult;

    if (!data) {
      titleEl.innerText = "⚠ No Data";
      explanationEl.innerText = "No scan result found.";
      return;
    }

    renderUI(data);
  });

  // ==========================
  // 🎯 UI RENDER
  // ==========================
  function renderUI(data) {

    const score = data.fraud_score || 0;

    let color = "#00ff99"; // safe default
    let rainColor = null;
    let status = "Safe";
    let title = "✅ Safe Website";

    // 🚨 STRICT BACKEND CONTROL
    if (data.risk === "fraud-high") {
      color = "#ff4d4d";
      rainColor = "rgba(255,77,77,0.6)";
      status = "🚨 Fraud Website Blocked";
      title = "🚨 Fraud Website Blocked";
    }

    else if (data.risk === "suspicious") {
      color = "#ffd93d";
      rainColor = "rgba(255,217,61,0.5)";
      status = "⚠ Suspicious";
      title = "⚠ Suspicious Website";
    }

    // 🎯 APPLY UI
    titleEl.innerText = title;
    statusEl.innerText = status;
    statusEl.style.color = color;
    explanationEl.innerText = data.explanation || "";

    // ✅ CLEAN BULLETS (NO DOUBLE DOT)
    reasonsEl.innerHTML = "";
    (data.reasons || []).forEach(r => {
      const li = document.createElement("li");
      li.textContent = r;
      reasonsEl.appendChild(li);
    });

    // 🌧️ RAIN ONLY FOR RISK
    if (rainColor) {
      startRain(rainColor);
    } else {
      stopRain();
    }

    // ==========================
    // 🎯 RING ANIMATION (FIXED CENTER)
    // ==========================
    let current = 0;

    function animate() {
      ctx.clearRect(0, 0, 130, 130);

      ctx.beginPath();
      ctx.arc(
        65,
        65,
        55,
        -Math.PI / 2,
        (-Math.PI / 2) + (2 * Math.PI * (current / 100))
      );

      ctx.strokeStyle = color;
      ctx.lineWidth = 8;
      ctx.stroke();

      scoreText.innerText = current + "%";

      if (current < score) {
        current += 2;
        requestAnimationFrame(animate);
      }
    }

    animate();
  }

  // ==========================
  // 🔙 NAVIGATION
  // ==========================
  document.getElementById("goBack").onclick = () => {
    window.history.back();
  };

  document.getElementById("continue").onclick = () => {
    chrome.storage.local.get("originalUrl", (res) => {
      if (res.originalUrl) {
        window.location.href = res.originalUrl;
      }
    });
  };

});