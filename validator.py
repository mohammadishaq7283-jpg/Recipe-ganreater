def validate_veggies(veggies_list):
    """
    Yeh function check karta hai ke user ne valid input diya hai.
    Rule: List khali nahi honi chahiye. (5 ki limit ab nahi hai)
    """

    # Check: Kya list khali hai?
    if not veggies_list:
        return False, "Please add at least one vegetable to generate a recipe."

    # Agar 1 bhi sabzi hai to Valid hai
    return True, "Validation Successful"
