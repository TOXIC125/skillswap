import csv
import json
from datetime import datetime
from statistics import mean

CSV_FILE = "data/expenses.csv"
EXPORT_FILE = "exports/summary.json"

def load_expenses():
    expenses = []
    with open(CSV_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Amount"] = float(row["Amount"])
            row["Date"] = datetime.strptime(row["Date"], "%Y-%m-%d")
            expenses.append(row)
    return expenses

def summarize(expenses):
    total = sum(e["Amount"] for e in expenses)
    categories = {}
    for e in expenses:
        categories.setdefault(e["Category"], []).append(e["Amount"])
    avg_per_category = {k: mean(v) for k, v in categories.items()}
    return {"total": total, "avg_per_category": avg_per_category}

def export_summary(summary):
    with open(EXPORT_FILE, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"Summary exported to {EXPORT_FILE}")

def main():
    data = load_expenses()
    summary = summarize(data)
    print("Total spent: $", round(summary["total"], 2))
    print("\nAverage per category:")
    for k, v in summary["avg_per_category"].items():
        print(f"  {k}: ${round(v, 2)}")
    export_summary(summary)

if __name__ == "__main__":
    main()
