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


def calculate_compound_growth(P, r, n, t, pmt=0, inflation=0, contribution_timing='end'):
    """
    Calculate compound growth with contributions.
    
    Parameters:
    - P: principal
    - r: annual interest rate (as decimal, e.g., 0.05 for 5%)
    - n: compounds per year
    - t: number of years
    - pmt: annual contribution amount
    - inflation: annual inflation rate (as decimal)
    - contribution_timing: 'start' or 'end' of year (default: 'end')
    
    Returns tuple: (nominal_balance, inflation_adjusted_balance)
    """
    
    periodic_rate = r / n
    total_periods = n * t
    
    principal_future_value = P * (1 + periodic_rate) ** total_periods
    
    contribution_future_value = 0
    if pmt > 0 and t > 0:
        effective_annual_rate = (1 + periodic_rate) ** n - 1
        
        if contribution_timing == 'start':
            contribution_future_value = pmt * (((1 + effective_annual_rate) ** t - 1) / effective_annual_rate) * (1 + effective_annual_rate)
        else:
            contribution_future_value = pmt * (((1 + effective_annual_rate) ** t - 1) / effective_annual_rate)
    
    nominal_balance = principal_future_value + contribution_future_value
    
    inflation_adjusted_balance = nominal_balance
    if inflation > 0 and t > 0:
        inflation_adjusted_balance = nominal_balance / ((1 + inflation) ** t)
    
    return nominal_balance, inflation_adjusted_balance


def get_user_input():
    """Prompt user for input if not provided via CLI"""
    print("\nCompound Interest Calculator\n")

    while True:
        try:
            principal = float(input("Principal amount (IDR): "))
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
            contributions = float(input("Annual contributions (IDR) [0 for none]: "))
            if contributions < 0:
                print("Contributions cannot be negative. Try again.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        try:
            inflation_input = input("Annual inflation rate (%, 0 to ignore) [0]: ")
            if inflation_input.strip() == "":
                inflation = 0.0
                break
            inflation = float(inflation_input) / 100
            if inflation < 0 or inflation >= 1:
                print("Inflation rate must be between 0 and 100%. Try again.")
                continue
            break
        except ValueError:
            inflation = 0.0
            break

    while True:
        timing = input("Contributions made at (start/end) of year [end]: ").strip().lower()
        if timing == "":
            timing = "end"
        if timing in ["start", "end"]:
            break
        print("Please enter 'start' or 'end'.")

    return principal, rate, compounds_per_year, years, contributions, inflation, timing


def display_results(principal, rate, compounds_per_year, years, contributions=0, inflation=0, contribution_timing='end'):
    """Display results in a formatted table"""
    final_nominal, final_real = calculate_compound_growth(
        principal, rate, compounds_per_year, years, contributions, inflation, contribution_timing
    )
    
    total_contributed = principal + (contributions * years)
    
    nominal_interest = final_nominal - total_contributed
    
    total_real_contributions = principal
    if contributions > 0 and years > 0:
        for year in range(1, years + 1):
            if contribution_timing == 'start':
                years_ago = year
            else:
                years_ago = year - 1 if year > 0 else 0
            
            real_value = contributions / ((1 + inflation) ** years_ago)
            total_real_contributions += real_value
    
    real_interest = final_real - total_real_contributions

    print("\n" + "=" * 60)
    print("COMPOUND INTEREST SUMMARY")
    print("=" * 60)
    summary_data = [
        ["Principal", f"IDR {principal:,.2f}"],
        ["Annual Contributions", f"IDR {contributions:,.2f}" if contributions > 0 else "None"],
        ["Contribution Timing", contribution_timing.capitalize() + " of year"],
        ["Total Contributed (nominal)", f"IDR {total_contributed:,.2f}"],
        ["Annual Rate", f"{rate * 100:.2f}%"],
        ["Compounds", f"{compounds_per_year}x per year"],
        ["Time Period", f"{years} years"],
    ]
    if inflation > 0:
        summary_data.append(["Inflation Rate", f"{inflation * 100:.2f}%"])
        summary_data.append(["Total Contributed (real)", f"IDR {total_real_contributions:,.2f}"])
    
    summary_data.extend([
        ["Interest Earned (nominal)", f"IDR {nominal_interest:,.2f}"],
        ["Final Balance (nominal)", f"IDR {final_nominal:,.2f}"],
    ])
    
    if inflation > 0:
        summary_data.extend([
            ["Interest Earned (real)", f"IDR {real_interest:,.2f}"],
            ["Final Balance (real)", f"IDR {final_real:,.2f}"],
        ])
    
    print(tabulate(summary_data, tablefmt="simple"))

    print("\n" + "=" * 60)
    print("YEAR-BY-YEAR BREAKDOWN")
    print("=" * 60)
    breakdown = []
    
    for year in range(0, years + 1):
        nominal, real = calculate_compound_growth(
            principal, rate, compounds_per_year, year, contributions, inflation, contribution_timing
        )
        
        total_nominal_contrib = principal + (contributions * year)
        nominal_interest = nominal - total_nominal_contrib
        
        total_real_contrib = principal
        if contributions > 0 and year > 0:
            for y in range(1, year + 1):
                if contribution_timing == 'start':
                    years_ago = y
                else:
                    years_ago = y - 1 if y > 0 else 0
                total_real_contrib += contributions / ((1 + inflation) ** years_ago)
        
        real_interest = real - total_real_contrib
        
        if inflation > 0:
            breakdown.append([
                year,
                f"IDR {nominal:,.2f}",
                f"IDR {real:,.2f}",
                f"IDR {nominal_interest:,.2f}",
                f"IDR {real_interest:,.2f}",
            ])
        else:
            breakdown.append([
                year,
                f"IDR {nominal:,.2f}",
                f"IDR {nominal_interest:,.2f}",
            ])
    
    if inflation > 0:
        headers = ["Year", "Balance (Nominal)", "Balance (Real)", "Interest (Nominal)", "Interest (Real)"]
    else:
        headers = ["Year", "Balance", "Interest Earned"]
    
    print(tabulate(breakdown, headers=headers, tablefmt="grid"))


def main():
    parser = argparse.ArgumentParser(
        description="Calculate compound interest growth with contributions and inflation"
    )
    parser.add_argument("-p", "--principal", type=float, help="Principal amount (IDR)")
    parser.add_argument("-r", "--rate", type=float, help="Interest rate (%)")
    parser.add_argument("-n", "--compounds", type=int, help="Compounds per year")
    parser.add_argument("-t", "--years", type=int, help="Number of years")
    parser.add_argument("-c", "--contributions", type=float, default=0, help="Annual contributions (IDR) [default: 0]")
    parser.add_argument("-i", "--inflation", type=float, default=0, help="Annual inflation rate (%) [default: 0]")
    parser.add_argument("--timing", type=str, default="end", choices=["start", "end"], 
                        help="Contribution timing: 'start' or 'end' of year [default: end]")

    args = parser.parse_args()

    if all([args.principal is not None, args.rate is not None, args.compounds is not None, args.years is not None]):
        principal = args.principal
        rate = args.rate / 100
        compounds_per_year = args.compounds
        years = args.years
        contributions = args.contributions
        inflation = args.inflation / 100
        contribution_timing = args.timing
    else:
        principal, rate, compounds_per_year, years, contributions, inflation, contribution_timing = get_user_input()

    if not validate_input(principal, rate, compounds_per_year, years, contributions, inflation):
        sys.exit(1)

    display_results(principal, rate, compounds_per_year, years, contributions, inflation, contribution_timing)


if __name__ == "__main__":
    main()