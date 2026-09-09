const API_BASE = window.location.origin;

async function checkSystemHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            const data = await res.json();
            const statusEl = document.getElementById("system-status");
            statusEl.innerText = `ChromaDB (${data.vectordb.kb_documents_count} docs) | ${data.ollama.status}`;
        }
    } catch (e) {
        console.warn("Health check error:", e);
    }
}

function useQuickPrompt(promptText) {
    const input = document.getElementById("prompt-input");
    input.value = promptText;
    sendMessage();
}

async function sendMessage() {
    const input = document.getElementById("prompt-input");
    const prompt = input.value.trim();
    if (!prompt) return;

    const model = document.getElementById("model-select").value;
    const useRag = document.getElementById("rag-toggle").checked;

    // Append User Message
    appendMessage("user", prompt);
    input.value = "";
    document.getElementById("autocomplete-box").style.display = "none";

    // Show Loading Message
    const loadingId = appendLoadingMessage();

    try {
        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                prompt: prompt,
                model: model,
                use_rag: useRag,
                top_k: 4
            })
        });

        const data = await res.json();
        removeLoadingMessage(loadingId);

        if (!res.ok) {
            appendMessage("assistant", `⚠️ Error: ${data.detail || "Failed to generate mentor response."}`);
            return;
        }

        // Update top metrics chips
        document.getElementById("chip-latency").innerText = `⏱️ Latency: ${data.latency_ms} ms (LLM: ${data.llm_time_ms}ms, RAG: ${data.retrieval_time_ms}ms)`;
        document.getElementById("chip-confidence").innerText = `🎯 Grounding: ${Math.round((data.confidence_score || 1.0) * 100)}%`;

        // Render response
        let contextHtml = "";
        if (data.context && data.context.length > 0) {
            const chunkItems = data.context.map((c, i) => `
                <div style="margin-bottom: 8px; padding: 6px; background: rgba(255,255,255,0.05); border-radius: 4px;">
                    <strong>[#${i+1}] Source: ${c.source} (Score: ${c.score})</strong>
                    <p style="font-size: 0.75rem; color: #cbd5e1; margin-top: 2px;">${escapeHtml(c.content.substring(0, 200))}...</p>
                </div>
            `).join("");

            contextHtml = `
                <details class="context-accordion">
                    <summary>📚 Verified Grounding Sources (${data.context.length} chunks retrieved)</summary>
                    <div style="margin-top: 8px;">${chunkItems}</div>
                </details>
            `;
        }

        appendMessage("assistant", formatMarkdown(data.answer) + contextHtml);

    } catch (err) {
        removeLoadingMessage(loadingId);
        appendMessage("assistant", `⚠️ Network or service error: ${err.message}`);
    }
}

function appendMessage(sender, htmlContent) {
    const container = document.getElementById("chat-messages");
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}`;

    const avatar = sender === "user" ? "🎓" : "🤖";
    msgDiv.innerHTML = `
        <div class="msg-avatar">${avatar}</div>
        <div class="msg-body">${htmlContent}</div>
    `;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
}

function appendLoadingMessage() {
    const id = "loading_" + Date.now();
    const container = document.getElementById("chat-messages");
    const msgDiv = document.createElement("div");
    msgDiv.id = id;
    msgDiv.className = "message assistant";
    msgDiv.innerHTML = `
        <div class="msg-avatar">🤖</div>
        <div class="msg-body">
            <em>Analyzing guidelines, retrieving rubric benchmarks, and consulting LLM mentor...</em>
        </div>
    `;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
    return id;
}

function removeLoadingMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function formatMarkdown(text) {
    if (!text) return "";
    let html = escapeHtml(text);
    // Replace headings
    html = html.replace(/^### (.*$)/gim, '<h3 style="margin: 8px 0; color: #38bdf8;">$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2 style="margin: 10px 0; color: #818cf8;">$1</h2>');
    // Replace bold
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    // Replace code blocks
    html = html.replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>');
    // Replace newlines
    html = html.replace(/\n/gim, '<br>');
    return html;
}

function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Autocomplete prompt suggestions
let debounceTimer;
document.getElementById("prompt-input").addEventListener("input", function(e) {
    clearTimeout(debounceTimer);
    const val = e.target.value;
    if (val.length < 2) {
        document.getElementById("autocomplete-box").style.display = "none";
        return;
    }
    debounceTimer = setTimeout(async () => {
        try {
            const res = await fetch(`${API_BASE}/suggestions?q=${encodeURIComponent(val)}`);
            if (res.ok) {
                const data = await res.json();
                const box = document.getElementById("autocomplete-box");
                if (data.suggestions.length > 0) {
                    box.innerHTML = data.suggestions.map(s => `
                        <div class="autocomplete-item" onclick="useQuickPrompt('${s.replace(/'/g, "\\'")}')">${s}</div>
                    `).join("");
                    box.style.display = "block";
                } else {
                    box.style.display = "none";
                }
            }
        } catch(e) {}
    }, 250);
});

// Handle Enter key submit
document.getElementById("prompt-input").addEventListener("keydown", function(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Init on load
window.addEventListener("DOMContentLoaded", () => {
    checkSystemHealth();
});
