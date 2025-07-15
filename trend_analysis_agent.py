# agents/trend_analysis_agent.py

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_trends(businesses):
    if not businesses:
        return "No business data available for trend analysis."

    # Format data
    trend_text = "\n".join(
        f"{b['business_name']} - Census Tract: {b['census_tract']}, Category: {b.get('category', 'Unknown')}"
        for b in businesses
    )

    prompt = f"""
You are a market trend analyst. Analyze the following businesses and identify any patterns, emerging trends, or notable insights across census tracts:\n{trend_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful geospatial market analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating trend insights: {e}"
