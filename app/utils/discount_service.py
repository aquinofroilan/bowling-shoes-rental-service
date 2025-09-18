from google import genai

client = genai.Client()

def get_discount(age: int, is_disabled: bool, conditions: list[str]) -> float:
    prompt = f"""
        You are a discount engine for a bowling shoe rental service.
        Apply the following rules to determine a discount:

        - Age 0-12 → 20%
        - Age 13-18 → 10%
        - Age 65+ → 15%
        - Disabled → 25%
        - Medical Conditions:
          - Diabetes → 10%
          - Hypertension → 10%
          - Chronic Condition → 10%

        A customer may qualify for multiple discounts, but only the highest discount applies.

        Input:
        Age: {age}
        Disabled: {"Yes" if is_disabled else "No"}
        Medical Conditions: {", ".join(conditions) if conditions else "None"}

        Output: Just return the discount percentage as a number (e.g., 25).
        """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    try:
        return float(response.text.strip().replace("%", ""))
    except Exception:
        return 0.0  # fallback if parsing fails