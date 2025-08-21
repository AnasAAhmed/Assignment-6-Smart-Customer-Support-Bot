# Assignment 6: Build a Smart Customer Support Bot using OpenAI Agent SDK

Assignment 6: Build a Smart Customer Support Bot using OpenAI Agent SDK, This project is a CLI Based **Smart Customer Support Bot using OpenAI Agent SDK** built with the **OpenAI Agent SDK** and **Google Gemini API** in python & @GuardRails with help of docs at [https://openai.github.io/openai-agents-python/guardrails/](https://openai.github.io/openai-agents-python/guardrails/) .

The agent is designed to answer a set of predefined math questions such as:

- "What is your policy?"
- "check order status of order 123?"

---

## 🚀 Setup Instructions

1. **Clone the repository** (or copy the Python file into your project folder).

2. **Install dependencies:**
   ```bash
   pip install openai-agents python-dotenv

Create a .env file in your project directory:
```
GEMINI_API_KEY=your_api_key_here
```

You can obtain your API key from Google AI Studio
.

2. **Run the chatbot:**
   ```bash
   uv run main.py

## 📝 Example Interaction

Below is a test run of the chatbot

(python-ai-agent) PS C:\programming\ai-assignments> & C:/programming/ai-assignments/.venv/Scripts/python.exe c:/programming/ai-assignments/assignment-6/main.py
Enter your query: stupid ,idiot
🚨 Guardrail tripped: Negative sentiment detected
Reason: Guardrail InputGuardrail triggered tripwire
🤝 Escalating to Human Agent...
👩 HUMAN: RunResult:
- Final output (str):
    I understand that you're feeling frustrated and angry right now. I want to help if I can, but I can't respond to abusive language. Could you please tell me what's going on and what you need help with, using respectful language? I'll do my best to assist you.
- 1 new item(s)
- 0 input guardrail result(s)
- 0 output guardrail result(s)
(See `RunResult` for more details)
(python-ai-agent) PS C:\programming\ai-assignments> & C:/programming/ai-assignments/.venv/Scripts/python.exe c:/programming/ai-assignments/assignment-6/main.py
Enter your query: check order status of order 123
🤖 BOT: Order 123 has shipped.

(python-ai-agent) PS C:\programming\ai-assignments> & C:/programming/ai-assignments/.venv/Scripts/python.exe c:/programming/ai-assignments/assignment-6/main.py
Enter your query: what are your policy
🤖 BOT: Our company specializes in high-quality electronics, including laptops, smartphones, and accessories. All products meet industry standards and come with manufacturer warranties. Our support team is available 24/7. You can return products within 30 days, track shipments, and request assistance with warranties or technical issues. Customer satisfaction is our top priority. 
(python-ai-agent) PS C:\programming\ai-assignments> & C:/programming/ai-assignments/.venv/Scripts/python.exe c:/programming/ai-assignments/assignment-6/main.py
Enter your query: what are your policy
🤖 BOT: Our company specializes in high-quality electronics, including laptops, smartphones, and accessories. All products meet industry standards and come with manufacturer warranties. Our support team is available 24/7. You can return products within 30 days, track shipments, and request assistance with warranties or technical issues. Customer satisfaction is our top priority. 
Our terms and conditions ensure fair use of our services. We respect user privacy, provide transparent pricing, and adhere to all legal regulations. Please review policies before making a purchase.

🤖 BOT_Name: Customer Support Bot