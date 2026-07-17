"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const getElement = (...ids) => {
    for (const id of ids) {
      const element = document.getElementById(id);
      if (element) return element;
    }
    return null;
  };

  const statusElement = getElement(
    "service-status",
    "health-status",
    "status-badge"
  );

  const versionElement = getElement("app-version", "service-version");
  const form = getElement("agent-form");
  const promptInput = getElement("prompt", "agent-prompt");
  const modeInput = getElement("mode", "agent-mode");
  const apiKeyInput = getElement("api-key", "opssage-api-key");
  const resultElement = getElement("agent-result", "result", "response");
  const submitButton = form?.querySelector('button[type="submit"]');

  function showResult(message, type = "info") {
    if (!resultElement) return;

    resultElement.textContent = message;
    resultElement.classList.remove("success", "error", "loading");
    resultElement.classList.add(type);
  }

  async function checkHealth() {
    try {
      const response = await fetch("/health", {
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Health check returned HTTP ${response.status}`);
      }

      const data = await response.json();

      if (statusElement) {
        statusElement.textContent =
          data.status === "healthy" ? "Operational" : data.status;
        statusElement.classList.remove("offline");
        statusElement.classList.add("online");
      }

      if (versionElement) {
        versionElement.textContent = `v${data.version}`;
      }
    } catch (error) {
      if (statusElement) {
        statusElement.textContent = "Unavailable";
        statusElement.classList.remove("online");
        statusElement.classList.add("offline");
      }

      console.error("Health check failed:", error);
    }
  }

  async function runAgent(event) {
    event.preventDefault();

    const prompt = promptInput?.value.trim();
    const mode = modeInput?.value || "auto";
    const apiKey = apiKeyInput?.value.trim();

    if (!prompt) {
      showResult("Please enter a troubleshooting request.", "error");
      promptInput?.focus();
      return;
    }

    if (!apiKey) {
      showResult("X-API-Key is required for AI execution.", "error");
      apiKeyInput?.focus();
      return;
    }

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Running...";
    }

    showResult("OpsSage AI is analysing your request...", "loading");

    try {
      const response = await fetch("/agent/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "X-API-Key": apiKey,
        },
        body: JSON.stringify({
          prompt,
          mode,
        }),
      });

      let data;

      try {
        data = await response.json();
      } catch {
        data = {};
      }

      if (response.status === 401) {
        throw new Error("Invalid or missing API key.");
      }

      if (response.status === 429) {
        const retryAfter = response.headers.get("Retry-After");
        throw new Error(
          retryAfter
            ? `Rate limit exceeded. Try again after ${retryAfter} seconds.`
            : "Rate limit exceeded. Please try again later."
        );
      }

      if (response.status === 503) {
        throw new Error(
          "AI execution is disabled on this public demo deployment."
        );
      }

      if (!response.ok) {
        throw new Error(
          data.detail || `Request failed with HTTP ${response.status}.`
        );
      }

      const output =
        data.result ??
        data.response ??
        data.answer ??
        JSON.stringify(data, null, 2);

      showResult(
        typeof output === "string"
          ? output
          : JSON.stringify(output, null, 2),
        "success"
      );
    } catch (error) {
      showResult(error.message || "Unable to execute the agent.", "error");
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = "Run Agent";
      }
    }
  }

  form?.addEventListener("submit", runAgent);
  checkHealth();
});
