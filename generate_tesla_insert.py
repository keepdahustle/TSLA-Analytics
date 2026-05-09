#!/usr/bin/env python
"""Generate SQL INSERT statements dari Tesla_stock_data.csv"""
import csv
import os
from datetime import datetime
from pathlib import Path

# Find CSV file - check parent directory first
current_dir = Path(__file__).parent
parent_dir = current_dir.parent

csv_files = {
    'Tesla_stock_data.csv': parent_dir / 'Tesla_stock_data.csv',
    'Alt location': current_dir / 'Tesla_stock_data.csv'
}

csv_file = None
for name, path in csv_files.items():
    if path.exists():
        csv_file = path
        print(f"Found CSV file at: {path}")
        break

if csv_file is None:
    print("Error: Tesla_stock_data.csv not found!")
    print(f"Checked: {csv_files}")
    exit(1)

output_file = current_dir / "tesla_stock_insert.sql"

insert_values = []

try:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            date_str = row['Date'].strip()
            close = float(row['Close'])
            high = float(row['High'])
            low = float(row['Low'])
            open_price = float(row['Open'])
            volume = int(float(row['Volume']))
            
            # Parse date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            year = date_obj.year
            quarter = (date_obj.month - 1) // 3 + 1
            month = date_obj.month
            
            # Format values for SQL
            insert_values.append(
                f"('{date_str}', {close}, {high}, {low}, {open_price}, {volume}, {year}, {quarter}, {month})"
            )
            
            # Every 100 rows, print progress
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1} rows...")
    
    print(f"\nTotal rows to insert: {len(insert_values)}")
    
    # Generate SQL file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- ============================================================================\n")
        f.write("-- Insert Tesla Stock Data dari Tesla_stock_data.csv\n")
        f.write(f"-- Total: {len(insert_values)} records\n")
        f.write("-- ============================================================================\n\n")
        
        f.write("INSERT INTO tesla_stock_data (date, close, high, low, open, volume, year, quarter, month)\n")
        f.write("VALUES\n")
        f.write(",\n".join(insert_values))
        f.write("\nON CONFLICT (date) DO NOTHING;\n")
    
    print(f"✓ Generated {output_file}")
    print(f"  File size: {len(insert_values) * 150} bytes (approx)")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
