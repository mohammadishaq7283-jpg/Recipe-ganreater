import sys

from validator import validate_veggies
from recipe_engine import generate_recipe


def get_veggies_input():
    """
    Yeh function App ke '+ Icon' feature ko simulate karta hai.
    User ek ek karke sabzi add karega.
    """
    veggies = []
    print("\n--- INGREDIENT INPUT ---")
    print("Type a vegetable name and press ENTER.")
    print("To stop adding, type 'done'.")

    while True:
        # User input (Yeh text box hai)
        item = input(f"\nAdd Vegetable #{len(veggies) + 1}: ").strip()

        if item.lower() == "done":
            if not veggies:
                print("(!) You haven't added any vegetables yet.")
                continue
            break

        if item:
            veggies.append(item)
            print(f"   [+] Added '{item}' successfully.")  # Visual confirmation like a UI
        else:
            print("(!) Please type a name.")

    return veggies


def main():
    print("--- PRO AI CHEF APP: LOGIN SUCCESSFUL ---")

    # Step 2: Language Selection
    language = input("Enter Preferred Language (e.g., English, Hindi, Urdu): ").strip()
    if not language:
        language = "English"

    # Step 3: Add Vegetables (Updated with + logic)
    veggies_list = get_veggies_input()

    # Step 4: VALIDATION
    # (Ab hum ne 5 ki limit hata di hai, bas empty check hoga)
    is_valid, message = validate_veggies(veggies_list)

    if not is_valid:
        print(f"\n[SYSTEM RESPONSE]: {message}")
        sys.exit()

    # Step 5: Cooking Style
    print("\n--- COOKING STYLE ---")
    print("1. Home Style")
    print("2. Restaurant Style")
    style_input = input("Select Style (1 or 2): ").strip()
    cooking_style = "Restaurant Style" if style_input == "2" else "Home Style"

    # Step 6: Recipe Type
    print("\n--- RECIPE TYPE ---")
    print("1. Short")
    print("2. Detailed")
    type_input = input("Select Type (1 or 2): ").strip()
    recipe_type = "Detailed" if type_input == "2" else "Short"

    # Step 7: Execution
    print(f"\nGenerating {recipe_type} {cooking_style} recipe in {language}...")

    final_output = generate_recipe(language, veggies_list, cooking_style, recipe_type)

    print("\n================ RECIPE OUTPUT ================")
    print(final_output)
    print("===============================================")


if __name__ == "__main__":
    main()
