import csv

with open('bank_account_info.csv', 'w') as bank_account_csv:
    csv_writer = csv.writer(bank_account_csv, delimiter = ',')

    csv_writer.writerow(['Name', 'Username', 'Password', 'Balance', 'Savings', 'Minimum', 'Rate'])
    csv_writer.writerow(['Jane Doe', 'jane_doe10', '802j6_4aT2e', '2096.0', 'True', '100', '.02'])
    csv_writer.writerow(['John Doe', 'JohnDoe33', 'Happy-Birthday33!', '1095.0', 'False'])