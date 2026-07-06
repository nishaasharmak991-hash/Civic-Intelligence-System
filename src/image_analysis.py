import tempfile
import json
from google.genai import types

def analyze_image(client, uploaded_image, language):

    # Save image temporarily
    suffix = "." + uploaded_image.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(
        suffix=suffix,
        delete=False
    ) as temp_file:

        temp_file.write(uploaded_image.getvalue())

        image_path = temp_file.name

    # Upload image
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_part = types.Part.from_bytes(
         data=image_bytes,
        mime_type=uploaded_image.type
    )

    prompt = f"""
You are an expert Civic Decision Intelligence AI.

Analyze ONLY the uploaded image.

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

If no civic issue is visible,

return:

{{
  "issue_type":"No Issue Detected",
  "problem_summary":"No visible civic issue detected.",
  "severity":"Low",
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
        contents=[
             prompt,
            image_part
        ]
    )

    text = response.text.strip()

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