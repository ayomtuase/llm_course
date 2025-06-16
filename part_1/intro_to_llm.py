# https://academy.towardsai.net/courses/take/beginner-to-advanced-llm-dev/multimedia/59791076-introduction-to-llms-and-how-to-use-via-api

import openai

from common import client

print("\n--- Starting Conversation: Turn 1 ---")

system_message = {
    "role": "system",
    "content": "You are a helpful AI Tutor explaining Large Language Model concepts simply.",
}

user_message_1 = {
    "role": "user",
    "content": "Can you explain what 'tokens' are in the context of LLMs, like I'm new to this?",
}

messages_history = [system_message, user_message_1]

print(f"Sending messages: {messages_history}")

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.5
MAX_TOKENS = 150
SEED = 123

try:
    print(f"\nMaking API call to {MODEL}...")
    completion_1 = client.chat.completions.create(
        model=MODEL,
        messages=messages_history,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        seed=SEED,
    )
    print("API call successful.")

    assistant_response_1 = completion_1.choices[0].message.content
    assistant_message_1 = completion_1.choices[0].message

    print("\nAI Tutor (Turn 1):")
    print(assistant_response_1)

    usage_1 = completion_1.usage
    print(
        f"\nToken Usage (Turn 1): Prompt={usage_1.prompt_tokens}, Completion={usage_1.completion_tokens}, Total={usage_1.total_tokens}"
    )
    finish_reason_1 = completion_1.choices[0].finish_reason
    print(f"Finish Reason: {finish_reason_1}")

except openai.AuthenticationError as e:
    print(f"OpenAI Authentication Error: {e}")
except openai.APIError as e:
    print(f"OpenAI API returned an API Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print("\n--- Continuing Conversation: Turn 2 ---")

user_message_2 = {
    "role": "user",
    "content": "Thanks! So, based on your explanation, are common words like 'the' or 'is' usually single tokens?",
}

messages_history.append(assistant_message_1)
messages_history.append(user_message_2)

print(f"\nSending updated messages: {messages_history}")

# Parameters for the second call (could be the same or different)
# Let's make it slightly more deterministic for a factual answer
TEMPERATURE_2 = 0.2
MAX_TOKENS_2 = 100
# Using the same seed ensures the *entire conversation flow* is reproducible if inputs are identical
SEED_2 = 123

try:
    print(f"\nMaking API call to {MODEL} (Turn 2)...")
    completion_2 = client.chat.completions.create(
        model=MODEL,
        messages=messages_history,  # Send the *full* history
        temperature=TEMPERATURE_2,
        max_tokens=MAX_TOKENS_2,
        seed=SEED_2,
    )
    print("API call successful.")

    # --- Process the response from the second turn ---
    assistant_response_2 = completion_2.choices[0].message.content
    # We don't strictly need to save assistant_message_2 unless continuing the conversation

    print("\nAI Tutor (Turn 2):")
    print(assistant_response_2)

    # Print token usage for this call
    usage_2 = completion_2.usage
    print(
        f"\nToken Usage (Turn 2): Prompt={usage_2.prompt_tokens}, Completion={usage_2.completion_tokens}, Total={usage_2.total_tokens}"
    )
    # Note: prompt_tokens for turn 2 will be larger as it includes the history from turn 1.
    finish_reason_2 = completion_2.choices[0].finish_reason
    print(f"Finish Reason: {finish_reason_2}")

except openai.AuthenticationError as e:
    print(f"OpenAI Authentication Error: {e}")
except openai.APIError as e:
    print(f"OpenAI API returned an API Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# # Example usage object from completion_1 or completion_2:
print(usage_1.prompt_tokens)  # -> number of input tokens
print(usage_1.completion_tokens)  # -> number of output tokens
print(usage_1.total_tokens)  # -> sum of both


def calculate_cost(usage, input_price_per_mil, output_price_per_mil):
    """Calculates the cost of an API call based on token usage and prices.

    Args:
        usage: The usage object from the OpenAI completion response
               (e.g., completion.usage). It should have attributes
               'prompt_tokens' and 'completion_tokens'.
        input_price_per_mil: Cost in USD per 1 million input tokens.
        output_price_per_mil: Cost in USD per 1 million output tokens.

    Returns:
        The total cost in USD for the API call, or None if usage is invalid.
    """
    if (
        not usage
        or not hasattr(usage, "prompt_tokens")
        or not hasattr(usage, "completion_tokens")
    ):
        print("Warning: Invalid usage object provided for cost calculation.")
        return None

    input_cost = (usage.prompt_tokens / 1_000_000) * input_price_per_mil
    output_cost = (usage.completion_tokens / 1_000_000) * output_price_per_mil
    total_cost = input_cost + output_cost
    return total_cost


PRICE_INPUT_PER_MIL = 0.60
PRICE_OUTPUT_PER_MIL = 2.40

print(f"\n--- Cost Calculations (GPT-4o-mini, April 2025 Rates) ---")
print(
    f"Prices: Input=${PRICE_INPUT_PER_MIL:.2f}/1M, Output=${PRICE_OUTPUT_PER_MIL:.2f}/1M"
)

try:
    if "usage_1" in locals():  # Check if usage_1 variable exists
        cost_1 = calculate_cost(usage_1, PRICE_INPUT_PER_MIL, PRICE_OUTPUT_PER_MIL)
        if cost_1 is not None:
            print(f"\nCost for Turn 1:")
            print(
                f"  Prompt Tokens: {usage_1.prompt_tokens}, Completion Tokens: {usage_1.completion_tokens}"
            )
            print(f"  Total Cost: ${cost_1:.8f}")
    else:
        print("\nSkipping Turn 1 cost calculation (usage_1 not found).")

    # Calculate cost for Turn 2 (assuming completion_2 and usage_2 exist from Block 3)
    if "usage_2" in locals():  # Check if usage_2 variable exists
        cost_2 = calculate_cost(usage_2, PRICE_INPUT_PER_MIL, PRICE_OUTPUT_PER_MIL)
        if cost_2 is not None:
            print(f"\nCost for Turn 2:")
            print(
                f"  Prompt Tokens: {usage_2.prompt_tokens}, Completion Tokens: {usage_2.completion_tokens}"
            )
            print(f"  Total Cost: ${cost_2:.8f}")
    else:
        print("\nSkipping Turn 2 cost calculation (usage_2 not found).")

    # Calculate total conversation cost
    if (
        "cost_1" in locals()
        and "cost_2" in locals()
        and cost_1 is not None
        and cost_2 is not None
    ):
        total_conversation_cost = cost_1 + cost_2
        print(
            f"\nTotal Conversation Cost (Turn 1 + Turn 2): ${total_conversation_cost:.8f}"
        )

except NameError as e:
    print(f"\nCould not calculate costs, a required variable is missing: {e}")
except Exception as e:
    print(f"An error occurred during cost calculation: {e}")
