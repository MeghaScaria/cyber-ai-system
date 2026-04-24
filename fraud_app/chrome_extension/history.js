document.addEventListener("DOMContentLoaded", () => {

  const container = document.getElementById("historyList");
  const emptyState = document.getElementById("emptyState");
  const clearBtn = document.getElementById("clearHistory");

  function loadHistory() {

    chrome.storage.local.get("history", (data) => {

      const history = data.history || [];

      container.innerHTML = "";

      if (history.length === 0) {
        emptyState.style.display = "block";
        return;
      }

      emptyState.style.display = "none";

      history.forEach(item => {

        const div = document.createElement("div");

        let riskClass = "safe";
        if (item.risk === "fraud-high") riskClass = "fraud";
        else if (item.risk === "suspicious") riskClass = "suspicious";

        div.className = `item ${riskClass}`;

        div.innerHTML = `
          <div class="url">${item.url}</div>
          <div class="meta">
            ${item.risk.toUpperCase()} • ${item.score}% • ${item.time}
          </div>
        `;

        container.appendChild(div);
      });
    });
  }

  // 🔄 CLEAR HISTORY
  clearBtn.addEventListener("click", () => {

    chrome.storage.local.set({ history: [] }, () => {
      loadHistory();
    });

  });

  // 🚀 INITIAL LOAD
  loadHistory();

});