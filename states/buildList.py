import csv

# Read the CSV file and count lines
with open('city_names.csv', 'r') as file:
    reader = csv.reader(file)
    total_lines = sum(1 for row in reader)

# Perform integer division
result = total_lines // 660

print(f"Total number of lines: {total_lines}")
print(f"Integer portion after dividing by 660: {result}")
