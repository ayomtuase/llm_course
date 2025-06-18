from common import openai_client

prompt_generation = """
Generate a table with the 5 most popular pharmaceutical companies and their foundation years.
The response should include only the table, with no additional text.
Use the following example format:
---
Company | Foundation Year
Microsoft | 1975
Apple | 1976
Google | 1998
Amazon | 1994
Meta | 2004
---"""

# Making the API call
response = openai_client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt_generation},
    ],
)
generated_response = response.choices[0].message.content
print("LLM response:", generated_response)

prompt_check_table_new = """Your task is to verify if a given table matches the exact format and structure of a provided example table.

Here's an example of the format that the table should have:
---
Company | Foundation Year
Microsoft | 1975
Apple | 1976
Google | 1998
Amazon | 1994
Meta | 2004
---

Table to Check:
{table_to_check}

Instructions:
- The table to check should match the structure, headers, and format of the Example Table exactly.
- The column names must be "Company" and "Foundation Year".
- The values in each row should have the company names and their corresponding foundation years.
- If the given table matches the example table in all these aspects, write "Yes".
- Write "No" if there are any differences in structure, headers, or if any company/year is missing or incorrect.

Only respond with "Yes" or "No".

"""

formatted_prompt = prompt_check_table_new.format(table_to_check=generated_response)
print("LLM Judge prompt:", formatted_prompt)

response = openai_client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": "You are a strict judge. Evaluate inputs based on the given criteria and provide only the required response.",
        },
        {"role": "user", "content": formatted_prompt},
    ],
    temperature=0,
)
print("Judgement for LLM response:", response.choices[0].message.content)

# Example Badly Formatted Table

badly_formatted_table = """
Company | Foundation Year

Microsoft | 1975

Apple | 1976
Google | 1998
Amazon | 1994

Meta | 2004
"""

# Formatted prompt with badly formatted table
formatted_prompt = prompt_check_table_new.format(table_to_check=badly_formatted_table)


# using LLM as a Judge to check the format
response = openai_client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": "You are a strict judge. Evaluate inputs based on the given criteria and provide only the required response",
        },
        {"role": "user", "content": formatted_prompt},
    ],
    temperature=0,
)
print("Judgement for badly formatted table:", response.choices[0].message.content)

prompt_check_company_type = """
Your task is to verify if a given table contains only companies from the pharmaceutical industry.

Here's an example of the format that the table should have:
---
Company | Foundation Year
Microsoft | 1975
Apple | 1976
Google | 1998
Amazon | 1994
Meta | 2004
---

Here's the table to check:
{table_to_check}

Instructions:
- The table to check should include only companies from the pharmaceutical industry.
- The column names will be "Company" and "Foundation Year".
- Evaluate whether each company in the table is part of the pharmaceutical sector.
- If all companies in the table are from the pharmaceutical industry, write "Yes".
- Write "No" if any company in the table is not from the pharmaceutical industry.

Only respond with "Yes" or "No".

"""

formatted_prompt_company_type = prompt_check_table_new.format(
    table_to_check=generated_response
)

# API Call
response = openai_client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": "You are a strict judge. Evaluate inputs based on the given criteria and provide only the required response",
        },
        {"role": "user", "content": formatted_prompt_company_type},
    ],
    temperature=0,
)
print("Company type judgement for LLM response:", response.choices[0].message.content)
