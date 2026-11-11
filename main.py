import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markup import escape


API_URL = "https://countries.dev/countries"
console = Console(highlight=False)


def show_menu():
    menu = (
        "[bold]1.[/bold] List countries in a region\n"
        "[bold]2.[/bold] Look up a country\n"
        "[bold]3.[/bold] Compare two countries\n"
        "[bold]4.[/bold] Quit"
    )
    console.print(Panel(menu, title="Country Explorer", expand=False, padding=(1, 3)))

def print_error(message):
    console.print(f"[bold red]{message}[/bold red]")

def get_choice():
    return input("Choose an option (1-4): ").strip()

def fetch_countries():
    """Fetch all countries from the API. Returns a list of dicts, or None on failure."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print_error(f"Could not fetch country data: {escape(str(error))}")
        return None

def get_regions(countries):
    """Get a list of unique regions from the countries data."""
    return sorted({country.get("region") for country in countries if country.get("region")})

def filter_by_region(countries, region):
    """Filter countries by the specified region. Returns a list of dicts."""
    return [country for country in countries 
            if (country.get("region") or "").lower() == region.lower()]

def find_country_by_name(countries, name):
    """Find a country by its name. Returns a dict or None if not found."""
    for country in countries:
        if (country.get("name") or "").lower() == name.lower():
            return country
    return None

def compare_countries_by_name(countries, name1, name2):
    """Compare two countries by their names. Returns a tuple of dicts or (None, None) if not found."""
    country1 = find_country_by_name(countries, name1)
    country2 = find_country_by_name(countries, name2)
    return (country1, country2)

def format_value_by_key(country, key):
    """Format the value of a specific key in the country dict."""
    value = country.get(key)

    if value is None or value == [] or value == "":
        return "N/A"

    if ('languages' == key  or 'currencies' == key ) and isinstance(value, list):
        names = [escape(item.get("name", "N/A")) for item in value]
        return ", ".join(names)

    if isinstance(value, list):
        return ", ".join(escape(str(v)) for v in value)

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:,}"

    return escape(str(value))

def show_countries_table(countries):
    keys = ["capital", "region", "population", "area", "languages", "currencies"]

    table = Table(title="Countries")
    table.add_column("Name", style="bold cyan")
    for key in keys:
        table.add_column(key.capitalize(), justify="right" if key in ("population", "area") else "left")

    for c in countries:
        table.add_row(*get_country_row(c))

    console.print(table)

def get_country_row(country):
    keys = ["capital", "region", "population", "area", "languages", "currencies"]
    name_cell = f"{escape(country.get('flag') or '')}  {escape(country.get('name') or 'Unknown')}"
    return [name_cell] + [format_value_by_key(country, key) for key in keys]

def show_country_details(country):
    keys = ["capital", "region", "population", "area", "languages", "currencies"]
    table = Table(title=f"{escape(country.get('name', 'Country'))} Details")
    table.add_column("Field", style="bold")
    table.add_column("Value", style="cyan")

    for key in keys:
        table.add_row(
            key.capitalize(),
            format_value_by_key(country, key),
        )
    console.print(table)

def show_comparison_countries_table(country1, country2):
    table = Table(title="Country Comparison")
    table.add_column("Field", style="bold")

    for c in (country1, country2):
        table.add_row(*get_country_row(c))

    # table.add_column(escape(country1.get("name", "Country 1")), style="cyan")
    # table.add_column(escape(country2.get("name", "Country 2")), style="magenta")

    #keys = ["capital", "region", "population", "area", "languages", "currencies"]
    #for key in keys:
    #    table.add_row(
    #        key.capitalize(),
    #        format_value_by_key(country1, key),
    #        format_value_by_key(country2, key),
    #    )
    console.print(table)

def main():
    countries = fetch_countries()

    if not countries:
        print_error("No data available. Exiting.")
        return

    while True:
        show_menu()
        console.print()

        choice = get_choice()

        if choice == "1":
            console.print("Available regions:")
            regions = get_regions(countries)
            for i, region in enumerate(regions, 1): console.print(f"[bold]{i}[/bold] OR {region}")
            console.print("-------------------")
            region = input("Enter a number or region name: ").strip()

            if not region:
                print_error("Region cannot be empty.")
                continue
            elif region.isdigit():
                region_index = int(region) - 1
                if 0 <= region_index < len(regions):
                    region = regions[region_index]

            countries_in_region = filter_by_region(countries, region)
            if not countries_in_region:
                print_error(f"No countries found in region {escape(region)}.")
            else:
                console.print(f"Countries in region {escape(region)}:")
                show_countries_table(countries_in_region)
        elif choice == "2":
            name = input("Enter a country name: ").strip()
            if not name:
                print_error("Country name cannot be empty.")
                continue
            found_country = find_country_by_name(countries, name)

            if not found_country:
                print_error(f"Country {escape(name)} not found.")
            else:
                show_country_details(found_country)
            console.print()
        elif choice == "3":
            name1 = input("Enter the first country name: ").strip()
            name2 = input("Enter the second country name: ").strip()
            if not name1 or not name2:
                print_error("Both country names must be provided.")
                continue
            country1, country2 = compare_countries_by_name(countries, name1, name2)
            if country1 and country2:
                show_comparison_countries_table(country1, country2)
            else:
                print_error("One or both countries not found.")
            console.print()
        elif choice == "4":
            console.print("Goodbye!")
            break
        else:
            print_error("Invalid choice. Please enter 1, 2, 3, or 4.")

        console.print()


if __name__ == "__main__":
    main()