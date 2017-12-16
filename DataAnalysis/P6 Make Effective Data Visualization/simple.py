


import csv

with open("prosperLoanData.csv", 'rb') as origin:
    reader = csv.reader(origin)
    headers = reader.next()
    print headers

headers = [
    "LoanOriginalAmount",
    "LoanOriginationDate",
    "ListingCreationDate"
]

with open("prosper.csv", 'wb') as simple:
    writer = csv.DictWriter(simple, fieldnames=headers)
    writer.writeheader()
    with open("prosperLoanData.csv", 'rb') as origin:
        dict_reader = csv.DictReader(origin)
        for row in dict_reader:
            data = {k:row[k] for k in headers}
            writer.writerow(data)
