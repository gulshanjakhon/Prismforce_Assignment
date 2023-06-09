import json

def calculate_balance_sheet(data):
    balance_sheet = {}
    
    # Iterate through expense data
    for expense in data['expenseData']:
        start_date = expense['startDate'][:7]  # Extract year and month
        
        if start_date not in balance_sheet:
            balance_sheet[start_date] = {'amount': -expense['amount'], 'startDate': expense['startDate']}
        else:
            balance_sheet[start_date]['amount'] -= expense['amount']
    
    # Iterate through revenue data
    for revenue in data['revenueData']:
        start_date = revenue['startDate'][:7]  # Extract year and month
        
        if start_date not in balance_sheet:
            balance_sheet[start_date] = {'amount': revenue['amount'], 'startDate': revenue['startDate']}
        else:
            balance_sheet[start_date]['amount'] += revenue['amount']
    
    # Fill in missing months with 0 amount
    earliest_date = min(balance_sheet.keys()) if balance_sheet else ''
    latest_date = max(balance_sheet.keys()) if balance_sheet else ''
    
    if earliest_date and latest_date:
        current_date = earliest_date
        
        while current_date < latest_date:
            next_date = (int(current_date[:4]), int(current_date[5:7]))  # Convert year and month to integers
            next_date = (next_date[0] + (next_date[1] % 12 + 1) // 12, (next_date[1] % 12 + 1) % 12)  # Increment month
            
            year = str(next_date[0])
            month = str(next_date[1]).zfill(2)
            new_date = f"{year}-{month}"
            # print(year+"  "+month)
            # print(new_date)
            if new_date not in balance_sheet:
                x=new_date+str('-01T00:00:00.000Z')
                balance_sheet[new_date] = {'amount': 0, 'startDate': x}
            
            current_date = new_date
    
    # Sort the balance sheet by timestamp
    sorted_balance_sheet = sorted(balance_sheet.items())
    
    return sorted_balance_sheet


# Read the input JSON file
with open('input.json') as file:
    input_data = json.load(file)

# Calculate the balance sheet
balance_sheet = calculate_balance_sheet(input_data)

# Output the balance sheet
output_data = {'balance': [entry[1] for entry in balance_sheet]}

# Write the output JSON file
with open('output.json', 'w') as file:
    json.dump(output_data, file, indent=4)
