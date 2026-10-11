
import os
import json
import operator
import ast

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-20b"

if not api_key:
    raise ValueError("GROQ API key not found")

client = Groq(api_key=api_key)


def get_product_price(product):
    prices = {
        "iPhone 17": 1000,
        "iPhone 15": 500,
    }
    return prices.get(product, 0)


def calculator(expression):
    # Safely evaluate basic arithmetic; don't use eval().
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def calculate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            return operations[type(node.op)](
                calculate(node.left),
                calculate(node.right),
            )

        raise ValueError("Unsupported expression")

    try:
        tree = ast.parse(expression, mode="eval")
        return calculate(tree.body)
    except (ValueError, SyntaxError, ZeroDivisionError):
        return "Calculator error"


tools = {
    "get_product_price": get_product_price,
    "calculator": calculator,
}

tool_schemas = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Get a product's price from the local price database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {"type": "string"}
                },
                "required": ["product"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a basic arithmetic expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"],
            },
        },
    },
]


def run_agent(question):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a shopping assistant. "
                "Use tools to get prices and calculate balances. "
                "Never invent tool results. "
                "After receiving tool results, answer the user."
            ),
        },
        {"role": "user", "content": question},
    ]

    for step in range(5):
        print(f"\n--- STEP {step + 1} ---")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tool_schemas,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message

        # Preserve tool-call metadata in the conversation.
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            print("Final answer:", message.content)
            return

        for call in message.tool_calls:
            name = call.function.name
            arguments = json.loads(call.function.arguments)

            print("Action:", name, arguments)

            if name not in tools:
                result = "Tool not found"
            else:
                try:
                    result = tools[name](**arguments)
                except Exception as error:
                    result = f"Tool error: {error}"

            print("Observation:", result)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

    print("Maximum steps reached.")


prompt = """
I have 5000 rupees. What is the price of an iPhone 17?
How much money will I have left?
"""

run_agent(prompt)
