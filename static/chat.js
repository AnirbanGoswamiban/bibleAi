const messages = document.getElementById("messages");
const input = document.getElementById("messageInput");
const sendButton = document.querySelector("button");

let isGenerating = false;

function removeWelcome() {
    const welcome = document.querySelector(".welcome");
    if (welcome) {
        welcome.remove();
    }
}

function addMessage(role, text = "") {
    const div = document.createElement("div");

    div.className = `message ${role}`;
    div.textContent = text;

    messages.appendChild(div);

    messages.scrollTop = messages.scrollHeight;

    return div;
}

async function sendMessage() {

    if (isGenerating) return;

    const question = input.value.trim();

    if (!question) return;

    removeWelcome();

    addMessage("user", question);

    input.value = "";

    isGenerating = true;

    sendButton.disabled = true;
    input.disabled = true;

    sendButton.textContent = "Thinking...";

    const assistantDiv = addMessage(
        "assistant",
        "✠ Consulting the Scriptures...\n\n"
    );

    try {

        const response = await fetch("/chat/stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: question
            })
        });

        assistantDiv.textContent = "";

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            const chunk = decoder.decode(value);

            // assistantDiv.textContent += chunk;

            for (const char of chunk) {
                assistantDiv.textContent += char;
                messages.scrollTop = messages.scrollHeight;
                await new Promise(r =>
                    setTimeout(r, 5));
            }


            messages.scrollTop =
                messages.scrollHeight;
        }

    } catch (err) {

        assistantDiv.textContent =
            "An error occurred while consulting the Scriptures.";

        console.error(err);

    } finally {

        isGenerating = false;

        sendButton.disabled = false;
        input.disabled = false;

        sendButton.textContent = "Send";

        input.focus();
    }
}