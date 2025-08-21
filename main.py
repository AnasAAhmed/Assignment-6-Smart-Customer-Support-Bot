from pydantic import BaseModel
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
import re
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

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

class OrderStatusOutput(BaseModel):
    order_id: str
    status: str

ORDERS_DB = {
    "123": "Shipped",
    "456": "Processing",
    "789": "Delivered",
}

def enable_order_status_tool(ctx: RunContextWrapper[str], agent: Agent[str]) -> bool:
    """
    Checks if the user's query contains the word "order" and a three-digit number.
    Returns True if both are present, False otherwise.
    """
    user_input = ctx.context
    has_order_word = re.search(r'\b(?:order)\b', user_input, re.IGNORECASE)
    has_three_digits = re.search(r'\b\d{3}\b', user_input)
    return bool(has_order_word and has_three_digits)

@function_tool(
    name_override="get_order_status",
    description_override="Fetch a customer's order status by order_id from the simulated DB.",
    is_enabled=enable_order_status_tool,
    failure_error_function=lambda error, args: (
        f"I couldn’t find that order. Please check your order ID and try again. ({error})"
    ),
)

async def get_order_status(order_id: str) -> OrderStatusOutput:
    """Fetch order status from simulated DB."""
    if order_id not in ORDERS_DB:
        raise ValueError("Order ID not found")
    return OrderStatusOutput(order_id=order_id, status=ORDERS_DB[order_id])


@function_tool
async def get_company_info() -> str:
    return '''\
  Company Info:
    Our company specializes in high-quality electronics, including laptops, smartphones, and accessories. All products meet industry standards and come with manufacturer warranties.

  Support Info:
   Our support team is available 24/7. You can return products within 30 days, track shipments, and request assistance with warranties or technical issues. Customer satisfaction is our top priority.

    Terms & Policies:
    Our terms and conditions ensure fair use of our services. We respect user privacy, provide transparent pricing, and adhere to all legal regulations. Please review policies before making a purchase.'''




# This is all i mannaged to this by understandings docs at https://openai.github.io/openai-agents-python/guardrails/
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
       result = await Runner.run(
          sentiment_guardrail_agent,
          input,
          run_config=config
        )

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
    - Answer simple FAQs about products with get_company_info tool. 
    - Use get_order_status tool for order queries with validation.
    - If input is complex, unclear, or escalated, hand off to Human Agent.
    """,
    tools=[get_company_info, get_order_status],
    input_guardrails=[sentiment_guardrail],
    handoffs=[human_agent],  # <<< provide human agent here
    model_settings=ModelSettings(
        tool_choice="auto"
        # metadata='sssss' can use it giving error
    ),
)


async def main():
    user_input=str(input('Enter your query: '))
    # for q in queries:
        # print(f"\n🟢 USER: {q}")
    try:
            res = await Runner.run(
                 bot_agent, 
                 user_input, 
                 run_config=config,
                 context=user_input #<--- using this make use of is_enbled in function_tool
                 )
            print(f"🤖 BOT: {res.final_output}")
            print(f"🤖 BOT_Namey: {res.last_agent.name}")

    except InputGuardrailTripwireTriggered as e:
            print("🚨 Guardrail tripped: Negative sentiment detected")
            print("Reason:", e)
            print("🤝 Escalating to Human Agent...")
            res = await Runner.run(human_agent, user_input,run_config=config)
            print(f"👩 HUMAN: {res}")


if __name__ == "__main__":
    asyncio.run(main())

