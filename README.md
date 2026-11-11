# Country Explorer

A small command-line tool that fetches live data about every country in the
world and lets you explore it from a menu.

## What it does

When you start the program it downloads the country list once, then shows a
menu with three actions:

1. **List countries in a region** - pick a region by number or name (for
   example `Europe` or `3`) and see every country in it in a table.
2. **Look up a country** - type a country name (case-insensitive) to see its
   details.
3. **Compare two countries** - type two names to see them one above the other
   in the same table.

Each table shows the country's flag and name, capital, region, population,
area, languages and currencies. Missing data is shown as `N/A`.

Bad input never crashes the program. Empty input, unknown regions or country
names, an invalid menu choice, and network problems all produce a clear red
message instead.

## API

Data comes from the free [countries.dev](https://countries.dev/docs) API
(`https://countries.dev/countries`). It needs no API key.

## Requirements

- Python 3.9 or newer
- The packages in `requirements.txt`: `requests` (HTTP) and `rich`
  (formatted tables and colors)

## How to run

```bash
git clone https://github.com/guzel/countries-api-py.git
cd countries-api-py
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.
Choose `4` in the menu to quit.

## Example session

```text
╭──────── Country Explorer ─────────╮
│                                   │
│   1. List countries in a region   │
│   2. Look up a country            │
│   3. Compare two countries        │
│   4. Quit                         │
│                                   │
╰───────────────────────────────────╯

Choose an option (1-4): 2
Enter a country name: canada
                                          Details of canada
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃  Name        ┃  Capital  ┃  Region    ┃  Population  ┃       Area  ┃  Languages        ┃  Currencies       ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│  🇨🇦  Canada  │  Ottawa   │  Americas  │  38,005,238  │  9,984,670  │  English, French  │  Canadian dollar  │
└──────────────┴───────────┴────────────┴──────────────┴─────────────┴───────────────────┴───────────────────┘
```

Wide tables look best in a terminal that is at least about 110 columns wide.

## Project layout

| File               | Purpose                                         |
|--------------------|-------------------------------------------------|
| `main.py`          | The program: fetching, processing and display   |
| `requirements.txt` | Python dependencies                             |
| `README.md`        | This file                                       |

Inside `main.py`, fetching (`fetch_countries`), data handling
(`filter_by_region`, `find_country_by_name`, `format_value_by_key`) and display
(`show_menu`, `show_countries_table`, `print_error`) live in separate
functions.
