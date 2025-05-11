import requests

def ask_deepseek(prompt, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error calling DeepSeek API: {e}"

def build_quote_prompt(builder, sqft, thickness, piers, rebar_ft, dirt_yards, notes=""):
    prompt = f"""
You are a quoting assistant for a high-end concrete foundation contractor in Dallas, TX.

Generate a quote breakdown for the following project:

Builder: {builder}
Foundation Area: {sqft} sqft
Concrete Thickness: {thickness} inches
Number of Piers: {piers}
Rebar Required: {rebar_ft} feet
Dirt Work Volume: {dirt_yards} cubic yards
Notes: {notes}

Break the quote into major categories:
- Concrete
- Rebar
- Piers
- Dirt Work
- Labor (assume 3-man crew, 2 days unless otherwise noted)
- Equipment (Pump truck if needed)
- Total

Use realistic pricing but keep it flexible — do not assume fixed rates unless mentioned.
Include a total estimate at the bottom.
"""
    return prompt
