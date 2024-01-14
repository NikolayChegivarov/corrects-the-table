from functions import visualization, anti_chaos

file_csv = 'phonebook_raw.csv'

visualization(file_csv)
anti_chaos(file_csv)

new_file = 'phonebook.csv'
visualization(new_file)
