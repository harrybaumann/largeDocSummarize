from together import Together
from configuration import load_config

def call_endpoint(system_prompt: str, prompt: str) -> str:
    api_key = load_config("api_key")
    model = load_config("model")

    client = Together(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
        ],
        # stream=True,
    )

    return response.choices[0].message.content
