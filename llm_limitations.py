# https://academy.towardsai.net/courses/take/beginner-to-advanced-llm-dev/multimedia/59791078-limitations-and-weaknesses-of-llms

import requests

from common import headers, url

# The data payload with your prompt and other parameters
data = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "{prompt}"},
    ],
    "max_tokens": 256,
    "temperature": 0.0,
}


def generate(prompt):
    # Set the prompt
    data["messages"][1]["content"] = prompt

    # Sending the POST request to the API
    response = requests.post(url, json=data, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        # Print the text part of the response
        return response.json()["choices"][0]["message"]["content"]
    else:
        return response.text

generate( "What is the name of the Towards AI developed largest open-source model and what is its size?" )

# Translate from English to Italian.
generate( "Translate the following from English to Italy: A Nurse saved the situation yesterday." )

# Translate from English to Italian.
generate( "Translate the following from English to Italy: An engineer saved the situation yesterday." )

generate("Who won the last super bowl?")

generate( "What is last Mission Impossible movie?" )
