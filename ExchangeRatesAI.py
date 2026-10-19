'''
FINE 3300 - Assignment 1 Part 2 (the AI code)
Name: Eden Johannes
Student number: 221214440
Date: October 19, 2026

'''
import csv
import os

class ExchangeRates:
    def __init__(self, filepath):
        """Initializes the ExchangeRates class by loading the CSV and extracting the latest rate."""
        self.filepath = filepath
        self.rate = self._load_latest_rate()

    def _load_latest_rate(self):
        """
        Opens the CSV file, locates the USD/CAD exchange rate column, 
        and extracts the value from the last row.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"The file '{self.filepath}' was not found. Please ensure it is in the correct directory.")

        with open(self.filepath, mode='r', encoding='utf-8') as file:
            reader = list(csv.reader(file))
            
            if not reader:
                raise ValueError("The exchange rate file is empty.")

            # Find the header row containing currency information
            header_index = -1
            for i, row in enumerate(reader):
                if any('USDCAD' in cell.upper().replace('/', '').replace('-', '') for cell in row):
                    header_index = i
                    break

            # If header is found, locate the specific column index
            if header_index != -1:
                header = reader[header_index]
                col_idx = -1
                for idx, col_name in enumerate(header):
                    if 'USDCAD' in col_name.upper().replace('/', '').replace('-', ''):
                        col_idx = idx
                        break
                
                # Search backwards from the last row to find the most recent valid numeric rate
                for row in reversed(reader[header_index + 1:]):
                    if row and len(row) > col_idx:
                        try:
                            rate_val = float(row[col_idx])
                            return rate_val
                        except ValueError:
                            continue

            # Fallback: if specific structure isn't matched, check the last row for the last numeric value
            last_row = reader[-1]
            for val in reversed(last_row):
                try:
                    return float(val)
                except ValueError:
                    continue

            raise ValueError("Could not locate a valid USD/CAD exchange rate in the file.")

    def convert(self, amount, from_currency, to_currency):
        """
        Converts an amount between USD and CAD using the loaded exchange rate.
        Assumes the rate represents: 1 USD = rate CAD.
        """
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        if from_currency not in ['USD', 'CAD'] or to_currency not in ['USD', 'CAD']:
            raise ValueError("Invalid currency. Please specify either 'USD' or 'CAD'.")

        if from_currency == to_currency:
            return amount

        # Conversion logic
        if from_currency == 'USD' and to_currency == 'CAD':
            return amount * self.rate
        elif from_currency == 'CAD' and to_currency == 'USD':
            return amount / self.rate


# --- User Interaction / Prompt ---
if __name__ == "__main__":
    file_name = "BankOfCanadaExchangeRate.2026.csv"
    
    print("--- Currency Exchange Converter ---")
    try:
        # Initialize the exchange rates class
        exchange_system = ExchangeRates(file_name)
        print(f"Successfully loaded exchange rate. Latest USD/CAD rate: {exchange_system.rate}\n")

        # Prompt user for inputs
        amount = float(input("Enter the amount to convert: "))
        
        from_curr = input("Enter 'from' currency (USD or CAD): ").strip().upper()
        to_curr = input("Enter 'to' currency (USD or CAD): ").strip().upper()

        # Perform conversion
        converted_amount = exchange_system.convert(amount, from_curr, to_curr)
        
        print("\n--- Result ---")
        print(f"{amount:,.2f} {from_curr} = {converted_amount:,.2f} {to_curr}")

    except Exception as e:
        print(f"\nError: {e}")