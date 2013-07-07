import sqlite3

class Database:

	def __init__(self):	
		self.con = sqlite3.connect("test.db")
		self.cur = self.con.cursor()
	
	def get_datasets(self):
		datasets = self.cur.execute('''select name from sqlite_master where type = 'table' ''')
		j={}
		j['identifier'] = 'id'
		j['label'] = 'name'
		items = []	
		counter = -1
		datasets = datasets.fetchall()
		for item in datasets:
			counter+=1
			td = {}
			td['name'] = item[0]
			td['id'] = counter
			items.append(td)
		j['data'] = items
		return j

	def colnames(self, table):
		return {str(item[1]):str(item[0]) for item in self.cur.execute("PRAGMA table_info("+table+")").fetchall()}

	def create_table(self, table, columns):
		columns_sql = ', '.join(columns)
		query = 'CREATE TABLE ' + table +'( ' + columns_sql + ' )'
		self.cur.execute(query)
		self.cur.close()
	
	def insert_records(self, table, records):
		wrap = lambda x: '"%s"' % str(x)	
		print 'look:'+table+str(records)
		for record in records:	
			record = map(wrap, record)
			record = ', '.join(record)
			query = 'INSERT INTO ' +table+' VALUES ( '+record+' )'
			self.cur.execute(query)
		self.con.commit()
		self.cur.close()

	def query(self, table, select, groupby=''):
		'To add where/filter'
		select = ', '.join(select)
		
		if len(groupby)>0:
			groupby = 'GROUP BY '+'( '+', '.join(groupby)+' )'
		else:
			groupby = ''

		query = 'SELECT '+select+' FROM '+table
		data = self.cur.execute(query).fetchall()
		return data


	def query_df(self, table, select='*', groupby=''):
		'Query the database and create a dataframe'
		select = ', '.join(select)
		
		if len(groupby)>0:
			groupby = 'GROUP BY '+'( '+', '.join(groupby)+' )'
		else:
			groupby = ''

		query = 'SELECT '+select+' FROM '+table
		data = self.cur.execute(query).fetchall()
		
		counter=-1
		for row in data:
			counter+=1
			d = dict(zip(self.colnames(table),row))
			data[counter] = d
		return data

class ImportCsv:

	def __init__(self, table, f=''):
		self.table = table
		self.data = self.csv_to_list(f)
		#self.import_tab_create(table)
		self.import_insert()

	def csv_to_list(self, f, sep=','):
		data = f.read()	
		data = data.split('\n')
		row_len = len(data[0].split(sep))
		data = [row.split(',') for row in data if len(row.split(','))==row_len]
		return data
	
	def import_tab_create(self, table):
		Database().create_table(table, columns = self.data.pop(0))

	def import_insert(self):
		Database().insert_records(records=self.data, table=self.table)

if __name__=='__main__':
	ImportCsv()
