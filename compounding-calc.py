import argparse
import sys
from tabulate import tabulate


def validate_input(principal, rate, compounds_per_year, years, contributions=0, inflation=0):
    """Validate all input parameters"""
    errors = []

    if principal < 0:
        errors.append("Principal cannot be negative")
    if rate < 0:
        errors.append("Interest rate cannot be negative")
    if compounds_per_year <= 0:
        errors.append("Compounds per year must be greater than 0")
    if years <= 0:
        errors.append("Years must be greater than 0")
    if contributions < 0:
        errors.append("Annual contributions cannot be negative")
    if inflation < 0 or inflation >= 100:
        errors.append("Inflation rate must be between 0 and 100%")

    if errors:
        print("\nInput Validation Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    return True


def calculate_compound_growth(P, r, n, t, pmt=0, inflation=0):
    """
    Return a tuple (raw, inflation_adjusted).

    raw: nominal balance after t years including annual contributions
    inflation_adjusted: real value after adjusting raw by inflation
    """

    raw = P * (1 + r / n) ** (n * t)

    if pmt > 0:
        contribution_growth = pmt * (((1 + r / n) ** (n * t) - 1) / (r / n))
        raw += contribution_growth

    adj = raw
    if inflation > 0:
        adj = raw / ((1 + inflation) ** t)

    return raw, adj


def get_user_input():
    """Prompt user for input if not provided via CLI"""
    print("\nCompound Interest Calculator\n")

    while True:
        try:
            principal = float(input("Principal amount (€): "))
            if principal < 0:
                print("Principal cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            rate = float(input("Interest rate (%, e.g., 5 for 5%): ")) / 100
            if rate < 0:
                print("Interest rate cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            compounds_per_year = int(input("Compounds per year (1=annual, 12=monthly, 365=daily): "))
            if compounds_per_year <= 0:
                print("Compounds per year must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            years = int(input("Number of years: "))
            if years <= 0:
                print("Years must be greater than 0. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            contributions = float(input("Annual contributions (€) [0 for none]: "))
            if contributions < 0:
                print("Contributions cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            inflation = float(input("Annual inflation rate (%, 0 to ignore) [0]: ")) / 100
            if inflation < 0 or inflation >= 1:
                print("Inflation rate must be between 0 and 100%. Try again.")
                continue
            break
        except ValueError:
            inflation = 0.0
            break

    return principal, rate, compounds_per_year, years, contributions, inflation


def display_results(principal, rate, compounds_per_year, years, contributions=0, inflation=0):
    """Display results in a formatted table"""
    final_raw, final_adj = calculate_compound_growth(principal, rate, compounds_per_year, years, contributions, inflation)
    total_contributed = principal + (contributions * years)
    interest_earned = final_adj - total_contributed

    print("\n" + "=" * 60)
    print("COMPOUND INTEREST SUMMARY")
    print("=" * 60)
    summary_data = [
        ["Principal", f"€{principal:,.2f}"],
        ["Annual Contributions", f"€{contributions:,.2f}" if contributions > 0 else "None"],
        ["Total Contributed", f"€{total_contributed:,.2f}"],
        ["Interest Rate", f"{rate * 100:.2f}%"],
        ["Compounds", f"{compounds_per_year}x per year"],
        ["Time Period", f"{years} years"],
    ]
    if inflation > 0:
        summary_data.append(["Inflation Rate", f"{inflation * 100:.2f}%"])
    summary_data.extend([
        ["Interest Earned (real)", f"€{interest_earned:,.2f}"],
        ["Final Balance (nominal)", f"€{final_raw:,.2f}"],
        ["Final Balance (inflation-adjusted)", f"€{final_adj:,.2f}"],
    ])
    print(tabulate(summary_data, tablefmt="simple"))

    print("\n" + "=" * 60)
    print("YEAR-BY-YEAR BREAKDOWN")
    print("=" * 60)
    breakdown = []
    for year in range(0, years + 1):
        raw, adj = calculate_compound_growth(principal, rate, compounds_per_year, year, contributions, inflation)
        total_contrib = principal + (contributions * year)
        growth = adj - total_contrib
        breakdown.append([year, f"€{raw:,.2f}", f"€{adj:,.2f}", f"€{growth:,.2f}"])

    print(tabulate(breakdown, headers=["Year", "Balance", "Inflation Adjusted", "Growth"], tablefmt="grid"))


def main():
    parser = argparse.ArgumentParser(
        description="Calculate compound interest growth with contributions and inflation"
    )
    parser.add_argument("-p", "--principal", type=float, help="Principal amount (€)")
    parser.add_argument("-r", "--rate", type=float, help="Interest rate (%)")
    parser.add_argument("-n", "--compounds", type=int, help="Compounds per year")
    parser.add_argument("-t", "--years", type=int, help="Number of years")
    parser.add_argument("-c", "--contributions", type=float, default=0, help="Annual contributions (€) [default: 0]")
    parser.add_argument("-i", "--inflation", type=float, default=0, help="Annual inflation rate (%) [default: 0]")

    args = parser.parse_args()

    if all([args.principal is not None, args.rate is not None, args.compounds is not None, args.years is not None]):
        principal = args.principal
        rate = args.rate / 100
        compounds_per_year = args.compounds
        years = args.years
        contributions = args.contributions
        inflation = args.inflation / 100
    else:
        principal, rate, compounds_per_year, years, contributions, inflation = get_user_input()

    if not validate_input(principal, rate, compounds_per_year, years, contributions, inflation):
        sys.exit(1)

    display_results(principal, rate, compounds_per_year, years, contributions, inflation)


if __name__ == "__main__":
    main()
