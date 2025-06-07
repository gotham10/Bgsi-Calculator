import requests
import html
import json
import re
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_screen():
    clear_screen()
    print("."*50)
    print("||" + " BGS Infinity Value Calculator ".center(46) + "||")
    print("'"*50)
    print("\nWelcome! This tool allows you to calculate the total value of your pets.")
    print("\n----- HOW TO USE -----")
    print("1. Enter one or more pet names separated by commas if you would like or just put one pet name..")
    print("2. Enter the desired variants, also separated by commas if you would like or just put one variant.")
    print("3. The tool will fetch the data and update your total.")
    print("\n----- VARIANTS -----")
    print("- You can either enter the variant number or the variant name or multipul useing commas.")
    print("1. All = 0")
    print("2. Normal = 1")
    print("3. Shiny = 2")
    print("4. Mythic = 3")
    print("5. ShinyMythic = 4")
    print("\n----- COMMANDS -----")
    print(" - Type 'reset' at the pet prompt to clear your current list and total.")
    print(" - Type 'exit' at any prompt to close the application.")
    print(" - Type 'mainmenu' at any prompt to return to the main menu.")
    input("\nPress Enter to begin...")

def parse_value(value_str):
    value_str = str(value_str).strip().upper()
    if not value_str:
        return 0
    multipliers = {
        'SX': 1e21, 'QI': 1e18, 'QA': 1e15, 'Q': 1e15,
        'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3
    }
    for suffix in sorted(multipliers.keys(), key=len, reverse=True):
        if value_str.endswith(suffix):
            number_part = value_str[:-len(suffix)]
            multiplier = multipliers[suffix]
            try:
                value = float(number_part) * multiplier
                return int(value)
            except ValueError:
                return 0
    try:
        return int(float(value_str))
    except ValueError:
        return 0

def pad_lines(lines):
    width = max(len(line.split(":")[0]) for line in lines)
    return "\n".join([f"{k.strip():<{width}}: {v.strip()}" for k, v in (line.split(":", 1) for line in lines)])

def normalize_variant(v):
    v = v.lower()
    variants = { "0": "All", "all": "All", "1": "Normal", "normal": "Normal", "2": "Shiny", "shiny": "Shiny", "3": "Mythic", "mythic": "Mythic", "4": "ShinyMythic", "shinymythic": "ShinyMythic" }
    return variants.get(v, None)

def fetch_data(search, variant):
    tries = [search.lower(), search.title(), search]
    for term in tries:
        s = term.replace(" ", "+")
        url = f"https://bgsi-kyc3.onrender.com/api/items?search={s}&variant={variant}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            raw = res.text
            pre_data = raw.split("<pre>")[1].split("</pre>")[0]
            pre_data = html.unescape(pre_data)
            data = json.loads(pre_data)
            if "pets" in data and data["pets"]:
                return data["pets"], url
        except:
            continue
    return None, None

def main():
    while True:
        total_value = 0
        added_pets = []
        print_welcome_screen()
        while True:
            clear_screen()
            print("--- CURRENT DATA ---")
            if not added_pets:
                print("  (None)")
            else:
                for pet_info in added_pets:
                    print(f"  - {pet_info}")
            print(f"\nCURRENT TOTAL VALUE: {total_value:,}")
            print("-"*25)
            search_input = input("\nEnter pet name(s)... \n> ").strip()
            if not search_input:
                input("\nPet name cannot be blank. Press Enter to try again.")
                continue
            if search_input.lower() == "exit":
                return
            if search_input.lower() == "reset":
                total_value = 0
                added_pets = []
                input("\n>>> Data has been reset. Press Enter to continue.")
                continue
            if search_input.lower() == "mainmenu":
                break
            variant_input = input("\nEnter variant(s)... \n> ").strip()
            if not variant_input:
                input("\nVariant cannot be blank. Press Enter to try again.")
                continue
            if variant_input.lower() == "exit":
                return
            if variant_input.lower() == "mainmenu":
                break
            searches = [s.strip() for s in search_input.split(',')]
            raw_variants = [v.strip() for v in variant_input.split(',')]
            valid_variants, invalid_variants = [], []
            for v_raw in raw_variants:
                norm_v = normalize_variant(v_raw)
                if norm_v:
                    if norm_v == "All":
                        valid_variants.extend(["Normal", "Shiny", "Mythic", "ShinyMythic"])
                    else:
                        valid_variants.append(norm_v)
                else:
                    invalid_variants.append(v_raw)
            variants_to_try = list(dict.fromkeys(valid_variants))
            if invalid_variants:
                print(f"\nInvalid variants ignored: {', '.join(invalid_variants)}")
            if not variants_to_try:
                input("\nNo valid variants were entered. Press Enter to try again.")
                continue
            for search_term in searches:
                print(f"\n\n--- Searching for: {search_term.upper()} ---")
                found_any_for_this_pet = False
                for v in variants_to_try:
                    pets, link = fetch_data(search_term, v)
                    if pets:
                        found_any_for_this_pet = True
                        for pet in pets:
                            pet_value_raw = pet.get('value', '0')
                            pet_value = parse_value(pet_value_raw)
                            total_value += pet_value
                            pet_display_name = f"{pet.get('name', 'Unknown')} ({pet.get('variant', 'N/A')})"
                            display_value_str = ""
                            if pet_value == 0 and str(pet_value_raw).strip().upper() not in ['0', '0.0']:
                                display_value_str = str(pet_value_raw)
                            else:
                                display_value_str = f"{pet_value:,}"
                            pet_info_str = f"{pet_display_name} | Value: {display_value_str}"
                            added_pets.append(pet_info_str)
                            lines = [
                                f"Name: {pet.get('name', 'N/A')}",
                                f"Description: {pet.get('description', 'N/A')}",
                                f"Chance: {pet.get('chance', 'N/A')}",
                                f"Demand: {pet.get('demand', 'N/A')}",
                                f"Owners: {pet.get('owners', 'N/A')}",
                                f"Value: {pet_value_raw} ({pet_value:,})",
                                f"Status: {pet.get('status', 'N/A')}",
                                f"Variant: {pet.get('variant', 'N/A')}",
                                f"Link: {link or 'N/A'}"
                            ]
                            print("\n" + pad_lines(lines))
                            print(f"\n>>> Added '{display_value_str}' to total. <<<")
                if not found_any_for_this_pet:
                    print(f"No pets found for '{search_term}' with the specified variants.")

if __name__ == "__main__":
    main()