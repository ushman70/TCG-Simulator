import csv

# Writes an array or dictionary of float card price values to a CSV file.
def write_to_csv(prices_array, filename="card_prices.csv", delimiter=","):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=delimiter)

        # Handles dictionary input grouped by rarity
        if isinstance(prices_array, dict):
            # Prints header and rows
            writer.writerow(["Rarity", "Value ($)"])  
            total_items = 0
            for rarity, prices in prices_array.items():
                for price in prices:
                    writer.writerow([rarity, f"{price:.2f}"])
                    total_items += 1
            print(f"Exported {total_items} card prices to '{filename}'.")
        
        # List/array input
        else:
            # Prints header and rows
            writer.writerow(["Value ($)"])  
            for price in prices_array:
                writer.writerow([f"{price:.2f}"])
            print(f"Exported {len(prices_array)} card prices to '{filename}'.")

# Reads prices/values as floats from an external CSV file into an existing array or dictionary.
def read_from_csv(target_array, filename, delimiter=","):
    if isinstance(target_array, (list, dict)):
        target_array.clear()

    total_loaded = 0

    with open(filename, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file, delimiter=delimiter)
        
        for row in reader:
            if not row:
                continue

            # Extracts multi-column values (Rarity, Price)
            if len(row) >= 2:
                rarity_str = row[0].strip()
                val_str = row[1].strip().replace("$", "")
            
                # Converts values to floats
                try:
                    val = round(float(val_str), 2)

                    if isinstance(target_array, dict):
                        if rarity_str not in target_array:
                            target_array[rarity_str] = []
                        target_array[rarity_str].append(val)

                    elif isinstance(target_array, list):
                        target_array.append(val)

                    total_loaded += 1

                except ValueError:
                    # Skips header or non-numeric rows
                    continue

            # Extracts single-column value
            else:
                val_str = row[0].strip().replace("$", "")

                # Converts values to floats
                try:
                    val = round(float(val_str), 2)

                    if isinstance(target_array, dict):
                        target_array.setdefault("Unknown", []).append(val)

                    elif isinstance(target_array, list):
                        target_array.append(val)

                    total_loaded += 1

                except ValueError:
                    # Skips header or non-numeric rows
                    continue

    #print(f"Loaded {total_loaded} values from '{filename}'.")
    
    return target_array