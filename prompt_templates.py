def create_master_prompt(language, user_input, style):
    prompt = f"""
    ROLE: You are a Master Chef.
    TASK: Write a recipe for: "{user_input}"
    STYLE: {style}
    LANGUAGE preference: {language}
    
    === RULES ===
    1. Reply in the requested language (English, Urdu, Hindi, Roman Urdu).
    2. Write COMPLETE sentences (No missing words).
    3. Format:
       - Title
       - Ingredients (Bulleted)
       - Instructions (Numbered Steps)
       - Chef's Tip
    
    Generate full recipe now.
    """
    return prompt
