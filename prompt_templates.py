def create_master_prompt(language, veggies_list, style, recipe_type):
    """
    Yeh function dynamic prompt generate karta hai based on user selection.
    """

    # List ko string mein convert karna display ke liye
    veggies_str = ", ".join(veggies_list)

    # 1. STYLE LOGIC
    if style == "Home Style":
        style_guide = "Create a simple, homemade, comfort-food style recipe. Easy to cook."
    else:  # Restaurant Style
        style_guide = "Create a professional, rich, restaurant-quality recipe. Use chef techniques."

    # 2. TYPE (LENGTH) LOGIC
    if recipe_type == "Short":
        length_guide = "Keep instructions extremely concise and short. No extra explanations."
        tips_instruction = "DO NOT include a 'Chef Tips' section."
    else:  # Detailed
        length_guide = "Provide detailed, step-by-step cooking instructions."
        tips_instruction = "You MUST include a 'Chef Tips' section at the end for taste/texture improvements."

    # 3. FINAL PROMPT CONSTRUCTION
    prompt = f"""
    ROLE: You are 'Pro AI Chef', a strictly controlled recipe engine. You are NOT a chatbot.

    INPUT DATA:
    - Language: {language}
    - Vegetables Provided: {veggies_str}
    - Cooking Style: {style}
    - Recipe Type: {recipe_type}

    STRICT INGREDIENT RULES:
    1. Use ONLY the provided vegetables: [{veggies_str}].
    2. NEVER add, suggest, or invent other vegetables/meats.
    3. You MAY use basic kitchen essentials: salt, oil, water, basic spices (turmeric, chili, etc.).

    BEHAVIOR RULES:
    1. {style_guide}
    2. {length_guide}
    3. Generate the ENTIRE response ONLY in {language}. Do not translate the title if not appropriate, but instructions must be in {language}.
    4. No emojis (unless language script requires it), no greetings, no conversational filler.

    REQUIRED OUTPUT FORMAT:

    Title:
    (Recipe Name)

    Ingredients:
    - (List user vegetables)
    - (List strictly necessary basics)

    Instructions:
    1. (Step 1)
    2. (Step 2)
    ...

    Chef Tips:
    {tips_instruction}
    """

    return prompt
