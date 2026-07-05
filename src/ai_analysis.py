import json


def analyze_text_complaint(
    client,
    category,
    location,
    complaint,
    language
):

    prompt = f"""
You are an expert Civic Decision Intelligence AI.

Analyze the following citizen complaint.

Category:
{category}

Location:
{location}

Complaint:
{complaint}

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT use ```json.
Do NOT write explanations.

Use exactly this structure:

{{
  "issue_type":"",
  "problem_summary":"",
  "severity":"",
  "priority_score":0,
  "department":[],
  "root_causes":[],
  "immediate_actions":[],
  "short_term_actions":[],
  "long_term_actions":[],
  "community_benefits":[]
}}

Write every value in {language}.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini adds it
    text = text.replace("```json", "")
    text = text.replace("```", "").strip()

    try:
        return json.loads(text)

    except Exception:

        return {

            "issue_type": "Unknown",

            "problem_summary": text,

            "severity": "Unknown",

            "priority_score": 0,

            "department": [],

            "root_causes": [],

            "immediate_actions": [],

            "short_term_actions": [],

            "long_term_actions": [],

            "community_benefits": []

        }