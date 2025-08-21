# Assignment 6: Build a Smart Customer Support Bot using OpenAI Agent SDK

Assignment 6: Build a Smart Customer Support Bot using OpenAI Agent SDK, This project is a CLI Based **Smart Customer Support Bot using OpenAI Agent SDK** built with the **OpenAI Agent SDK** and **Google Gemini API** in python & @GuardRails with help of docs at [https://openai.github.io/openai-agents-python/guardrails/](https://openai.github.io/openai-agents-python/guardrails/) .

The agent is designed to answer a set of predefined math questions such as:

- "What is the weather in shangai?"
- "What is two plus three?"
- "what is the weather in islamabad and what is 4 + 4?"

---

## 🚀 Setup Instructions

1. **Clone the repository** (or copy the Python file into your project folder).

2. **Install dependencies:**
   ```bash
   pip install openai-agents python-dotenv

Create a .env file in your project directory:
```
GEMINI_API_KEY=your_api_key_here
WEATHER_API_KEY=your_api_key_here
```

You can obtain your API key from Google AI Studio
.

2. **Run the chatbot:**
   ```bash
   uv run main.py

## 📝 Example Interaction

Below is a test run of the chatbot

What you want to know about weather info of a city OR addition of two numbers OR BOTH:

Q1:What is the weather in shangai

get_weather tools hits <---
You: what is the weather in shangai
Agent: OK. The weather in Shangai, Zulia, Venezuela is last updated at 09:00 on 2025-08-21. It is Sunny with 9 clouds, 28.7°C (83.6°f), humidity: 71, wind_speed: 11.2.

Q2:What is two plus three

add tools hits <---
You: what is two plus three
Agent: The answer is 5.

Q3:what is the weather in islamabad and what is 4 + 4

get_weather tools hits <---
add tools hits <---
You: wha is the weather in islamabad and what is 4 + 4
Agent: OK. The weather in Islamabad is 30.6°C, 87.0°f, Sunny Cloud:19, humidity:66, wind_speed:3.6. And 4 + 4 = 8.


