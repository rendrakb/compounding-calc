import argparse
from tabulate import tabulate

def calculate_compound_growth(P, r, n, t):
    """
    P: Principal (initial investment)
    r: Annual interest rate (as a decimal, e.g., 0.05 for 5%)
    n: Number of times interest is compounded per year
    t: Number of years
    """
    amount = P * (1 + r / n) ** (n * t)
    return amount

def get_user_input():
    """Prompt user for input if not provided via CLI"""
    print("\nCompound Interest Calculator\n")
    principal = float(input("Principal amount (€): "))
    rate = float(input("Annual interest rate (%, e.g., 5 for 5%): ")) / 100
    compounds_per_year = int(input("Compounds per year (1=annual, 12=monthly, 365=daily): "))
    years = int(input("Number of years: "))
    return principal, rate, compounds_per_year, years

def display_results(principal, rate, compounds_per_year, years):
    """Display results in a formatted table"""
    final_balance = calculate_compound_growth(principal, rate, compounds_per_year, years)
    interest_earned = final_balance - principal
    
    print("\n" + "=" * 50)
    print("COMPOUND INTEREST SUMMARY")
    print("=" * 50)
    summary_data = [
        ["Principal", f"€{principal:,.2f}"],
        ["Annual Rate", f"{rate * 100:.2f}%"],
        ["Compounds", f"{compounds_per_year}x per year"],
        ["Time Period", f"{years} years"],
        ["Interest Earned", f"€{interest_earned:,.2f}"],
        ["Final Balance", f"€{final_balance:,.2f}"],
    ]
    print(tabulate(summary_data, tablefmt="simple"))
    
    print("\n" + "=" * 50)
    print("YEAR-BY-YEAR BREAKDOWN")
    print("=" * 50)
    breakdown = []
    for year in range(0, years + 1):
        balance = calculate_compound_growth(principal, rate, compounds_per_year, year)
        growth = balance - principal
        breakdown.append([year, f"€{balance:,.2f}", f"€{growth:,.2f}"])
    
    print(tabulate(breakdown, headers=["Year", "Balance", "Growth"], tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser(
        description="Calculate compound interest growth"
    )
    parser.add_argument("-p", "--principal", type=float, help="Principal amount (€)")
    parser.add_argument("-r", "--rate", type=float, help="Annual interest rate (%)")
    parser.add_argument("-n", "--compounds", type=int, help="Compounds per year")
    parser.add_argument("-t", "--years", type=int, help="Number of years")
    
    args = parser.parse_args()
    
    if all([args.principal, args.rate, args.compounds, args.years]):
        principal = args.principal
        rate = args.rate / 100
        compounds_per_year = args.compounds
        years = args.years
    else:
        principal, rate, compounds_per_year, years = get_user_input()
    
    display_results(principal, rate, compounds_per_year, years)

if __name__ == "__main__":
    main()