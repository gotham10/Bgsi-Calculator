# BGS Infinity Value Calculator

A command-line tool to calculate total pet value based on pet names and variants using data from the BGS Infinity API.

## Features

- Supports multiple pet names and variants.
- Parses and converts values like `1.2T`, `500M`, etc.
- Interactive CLI with reset and exit commands.
- Automatically fetches latest value data via API.

## How to Use

1. Run the program.
2. Enter one or more pet names.
3. Enter one or more variant types (Normal, Shiny, Mythic, etc).
4. View your pet value summary.

### Variant Codes

- `0` or `All`
- `1` or `Normal`
- `2` or `Shiny`
- `3` or `Mythic`
- `4` or `ShinyMythic`

### Commands

- `reset`: Clear current list and total.
- `exit`: Close the app.
- `mainmenu`: Return to main menu.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt