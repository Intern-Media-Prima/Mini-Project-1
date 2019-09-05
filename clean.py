import re

DAYS_IN_MONTH = list(map(lambda x:(31 if x % 2 == 0 else 30) if x != 1 else 28, range(12))) # [31, 28, 31, 30, 31, 30]

def reduce(arr, func, start=None):
	i = 0
	if start == None:
		start = arr[0]
		i = 1
	for j in range(i, len(arr)):
		start = func(start,arr[j])
	return start

def read_csv(path):
	lines = []
	with open(path,'r') as file:
		ln = 1
		for line in file.read().split('\n'):
			if ln == 593:
				print(line)
			ln += 1
			cols = line.split(',')
			if len(cols) > 1 and cols[0] != '':
				cols = cols[1:]
				if reduce(cols, lambda a,b: '{}{}'.format(a,b), '') == '':
					continue
				lines.append(cols)
	return lines

def group_by_client(data):
	row = len(data)
	col = len(data[0])
	clients = {}
	client = 'Unknown'
	for i in range(row):
		if data[i][0] != '':
			client = data[i][0]
		elif client != 'Unknown':
			if not client in clients:				
				clients[client] = {'columns' : [data[i][1:]]}
			else:
				clients[client]['columns'].append(data[i][1:])
	return clients

def process_client_no(data):
	clients = group_by_client(data)
	for client in clients:
		row = 0
		for item in clients[client]['columns']:
			if reduce(item[1:], lambda a,b : a + b, '') == '':
				clients[client]['client_no'] = item[0]
				del clients[client]['columns'][row]
			elif item[0] == '':
				del clients[client]['columns'][row]
				continue
			row += 1
	return clients

def remove_total_row(data):
	clients = process_client_no(data)
	for client in clients:
		row = 0
		for item in clients[client]['columns']:
			if item[1] == 'Total:':
				del clients[client]['columns'][row]
			row += 1
	return clients

def clean_data(data, company):
	clients = remove_total_row(data)
	rows = []
	last_client = []
	for client in clients:
		for item in clients[client]['columns']:
			args = item[1].split('/')
			date_created = '{}-{}-{}'.format(args[2], args[1], DAYS_IN_MONTH[int(args[1])-1])

			client_no = '*None'
			try:
				client_no = clients[client]['client_no']
			except KeyError:
				error = False
				try:
					while not error:
						client = last_client.pop()
						client_no = clients[client]['client_no']
				except IndexError:
					error = True

			# print('Current Client: {}'.format(client))
			cols = [company, client, client_no, item[0], item[2], item[3], item[4], date_created]
			rows.append(cols)
		last_client.append(client)
	return rows

def write_csv(lines, path, headers=None):
	s = ''
	if headers != None:
		for header in headers:
			s += '{},'.format(header)
		s = '{}\n'.format(s[:-1])
	for line in lines:
		l = ''
		for col in line:
			l += '{},'.format(col)
		s += '{}\n'.format(l[:-1])
	with open(path,'w') as file:
		file.write(s[:-1])

def read_excel(path, f=0, t=0, sheet=None):
	import pandas as pd
	letters = re.split('', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')[1:-1]
	if sheet == None:
		sheet = pd.read_excel(path)
	else:
		sheet = pd.read_excel(path, sheet_name=sheet)
	sheet = sheet[f:t] if t != 0 else sheet[f:]
	sheet.columns = letters[:len(sheet.columns)]
	sheet = sheet.drop(columns=['A','F','G','H','I'])
	return sheet.reset_index(drop=True)

def write_text(text, path):
	with open(path, 'w') as file:
		file.write(text)

# data = read_csv('data.csv')
companies = {
	'BTO'    : 'BIG TREE OUTDOOR SDN BHD',
	'BTP'    : 'BIG TREE PRODUCTION SDN BHD',
	'BTSJ'   : 'BIG TREE SENI JAYA SDN BHD',
	'Gotcha' : 'GOTCHA SDN BHD',
	'KOP'    : 'KURNIA OUTDOOR PRODUCTIONS SDN BHD',
	'KOSB'   : 'KURNIA OUTDOOR SDN BHD',
	'TRC'    : 'THE RIGHT CHANNEL SDN BHD',
	'UPD'    : 'UPD SDN BHD'
}
headers = ['Company', 'Client Name', 'Client No', 'Invoice No', 'Total Due', 'Customer', 'Customer Category', 'Date Created']

rows = []
nrow = 0
nrow_cleaned = 0
for sheet in companies:
	if sheet != 'UPD':
		continue
	print('In sheet "{}"'.format(sheet))
	data = read_excel('data.xlsx', sheet=sheet, f=10, t=-10)
	filename = 'data.csv'
	write_text(data.to_csv(), filename)
	data = read_csv(filename)
	# cleaned = clean_data(data, companies[sheet])
	data = remove_total_row(data)
	# crow = len(data)
	# print('Total Row: {}'.format(crow))
	# print('Total Cleaned Row: {}'.format(len(cleaned)))
	# for row in cleaned:
	# 	rows.append(row)
	# 	nrow_cleaned += 1
	# nrow += crow
print('Total Combined Row: {}'.format(nrow))
print('Total Combined Cleaned Row: {}'.format(nrow_cleaned))
write_csv(rows, 'data_cleaned.csv', headers)