import csv

''' CSV UTILS '''


def read_csv(fn):
    with open(fn, 'r') as f:
        return list(csv.reader(f))


def append_row(file_name, row):
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def overwrite_rows(file_name, rows):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
