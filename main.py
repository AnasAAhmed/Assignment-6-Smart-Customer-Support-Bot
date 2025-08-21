from pydantic import BaseModel
from agents.models.gemini_provider import GeminiProvider
from agents import (
    Agent,
    function_tool,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    OpenAIChatCompletionsModel,
    Runner,
    AsyncOpenAI,
    RunConfig,
    TResponseInputItem,
    input_guardrail,
    handoff,
    ModelSettings,
)
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,

    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

gemini_provider = GeminiProvider(api_key="YOUR_GEMINI_API_KEY")

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

class OrderStatusOutput(BaseModel):
    order_id: str
    status: str

# Simulated DB
ORDERS_DB = {
    "123": "Shipped",
    "456": "Processing",
    "789": "Delivered",
}

@function_tool
async def get_order_status(order_id: str) -> OrderStatusOutput:
    """Fetch order status from simulated DB."""
    if order_id not in ORDERS_DB:
        raise ValueError("Order ID not found. Please check and try again.")
    return OrderStatusOutput(order_id=order_id, status=ORDERS_DB[order_id])


# -----------------------------
# 2. GUARDRAIL AGENT
# -----------------------------
class SentimentCheckOutput(BaseModel):
    is_negative: bool
    reasoning: str

sentiment_guardrail_agent = Agent(
    name="Sentiment Guardrail",
    instructions="Check if the user input is offensive, rude, or overly negative.",
    output_type=SentimentCheckOutput,
)

@input_guardrail
async def sentiment_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(sentiment_guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_negative,
    )


human_agent = Agent(
    name="Human Agent",
    instructions="You are a human support agent. Handle complex or sensitive queries.",
)


bot_agent = Agent(
    name="Customer Support Bot",
    instructions="""
    You are a helpful customer support bot.
    - Answer simple FAQs about products.
    - Use get_order_status tool for order queries.
    - If input is complex, unclear, or escalated, hand off to Human Agent.
    """,
    tools=[get_order_status],
    input_guardrails=[sentiment_guardrail],
    model_settings=ModelSettings(
        tool_choice="auto",  
        metadata={"team": "support-bot-v1"} #not suppoted becase of i dont have openai key
    ),
)


async def main():
    queries = [
        "What is your return policy?",
        "Check order 123",
        "Your company sucks, I want refund!",
        "Can you reset my password and also fix billing?",
        "Check order 000", 
    ]

    for q in queries:
        print(f"\n🟢 USER: {q}")
        try:
            res = await Runner.run(bot_agent, q, run_config=config,)

            # If bot decides it's too complex, handoff
            if "reset my password" in q or "billing" in q:
                print("🤝 Handoff to Human Agent...")
                res = await handoff(human_agent, res)

            # Log tool usage
            if res.invocations:
                for inv in res.invocations:
                    print(f"   ⚙️ Tool used: {inv.tool} → {inv.output}")

            print(f"🤖 BOT: {res.final_output}")

        except InputGuardrailTripwireTriggered as e:
            print("🚨 Guardrail tripped: Negative sentiment detected")
            print("Reason:", e.output_info.reasoning)
            print("🤝 Escalating to Human Agent...")
            res = await Runner.run(human_agent, q)
            print(f"👩 HUMAN: {res.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
