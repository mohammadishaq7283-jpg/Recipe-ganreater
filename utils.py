def print_header(title):
    """
    Console me header print karne ke liye helper function.
    """
    print("\n" + "="*40)
    print(f"   {title.upper()}")
    print("="*40 + "\n")


def clean_text(text):
    """
    Agar AI kabhi markdown symbols (**) bhej de to unhe hatana,
    taake plain text saaf nazar aaye.
    """
    if not text:
        return ""

    # Basic cleanup
    text = text.replace("**", "")  # Bold markers hatana
    text = text.replace("###", "")  # Headers hatana
    return text.strip()
