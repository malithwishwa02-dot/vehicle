"""Preview utility: prints summaries and samples of extracted CSV files."""
import csv
from pathlib import Path
EXPORT = Path(r"d:\vehicle\reproduce_profile\exports")

def sample_csv(name, n=5):
    p = EXPORT / name
    if not p.exists():
        print(f"Missing {p}")
        return
    with open(p,'r',encoding='utf-8',errors='replace') as fh:
        reader = csv.reader(fh)
        rows = list(reader)
        print('-'*40)
        print(p.name, ' | rows approx:', len(rows)-1)
        for r in rows[:n+1]:
            print(r)

if __name__ == '__main__':
    print('Preview of extracted CSVs:')
    sample_csv('cookies.csv', 5)
    sample_csv('logins.csv', 10)
    sample_csv('autofill.csv', 5)
    sample_csv('credit_cards.csv', 5)
    sample_csv('addresses.csv', 5)
    print('\nInventory:', Path(r'd:/vehicle/inventory.json').exists())
    print('Dumps dir exists:', Path(r'd:/vehicle/reproduce_profile/dumps').exists())
