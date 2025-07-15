# agents/business_summary_agent.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_business_insights(businesses):
    if not businesses:
        return "No business data available for summarization."

    # Format businesses into a readable string
    business_info = "\n".join(
        f"{b['business_name']} - Census Tract: {b['census_tract']}, Lat: {b['latitude']}, Lon: {b['longitude']}"
        for b in businesses
    )

    prompt = f"""You are a data analyst. Analyze the following business locations and provide a concise summary of insights:\n{business_info}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful business analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error generating summary: {e}"
