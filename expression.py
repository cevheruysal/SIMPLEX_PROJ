from distutils.log import error
from logging import exception
import re
  
class expr():

	def __init__(self, exp:str, ID:int=None):
		"""an expression is inputted in the form: 'lhs {operator} rhs' 
		rhs must only include a constant while all remaining monomials must be in the lhs
		{operator} must be one of the following: <=, >=, =
		lhs must be of the form lhs: '+/-{monomial} +/-{monomial} +/-....'
		"""

		self.exp = exp
		self.id = ID
		self.tip = None
		self.lhs_monos = []
		self.rhs_monos = []

    
	def parse2mono(self):
		monomial_pattern = r"([+-])?(\d+)?([a-z]_\d+)?"

		[lhs, rhs] = self.parse()

		for mono in re.split(" ", lhs):
			temp_mono = re.match(monomial_pattern, mono)
			monos = {'coef':None, 'vName':None, 'type':'VAR'}
			
			monos = self.monoms(temp_mono)

			self.lhs_monos.append(monos)

		for mono in re.split(" ", rhs):
			temp_mono = re.match(monomial_pattern, mono)

			monos = self.monoms(temp_mono)

			self.rhs_monos.append(monos)

		return True

	def parse(self):
		for oper in re.split(",", r" <= , >= , = , := "):

			if re.search(oper, self.exp):	
				self.tip = oper.strip()

				return re.split(oper, self.exp)

		raise Exception("please use one of the following operators in your equations/objective function: <=, >=, =, :=")

	def monoms(self, temp_mono):
		monos = {'coef':None, 'vName':None, 'type':'VAR'}

		if temp_mono.group(3) is not None:
			monos['vName'] = temp_mono.group(3)

			if temp_mono.group(2) is not None:
				if temp_mono.group(1) is not None:
					monos['coef'] = float(temp_mono.group(1)+temp_mono.group(2))

				else:
					monos['coef'] = float(temp_mono.group(2))
			else:
				if temp_mono.group(1) is not None:
					monos['coef'] = float(temp_mono.group(1)+'1')

				else:
					monos['coef'] = 1.0
		else:
			monos['type'] = 'CONS'

			if temp_mono.group(2) is not None:
				if temp_mono.group(1) is None:
					monos['coef'] = float(temp_mono.group(2))

				else:
					monos['coef'] = float(temp_mono.group(1)+temp_mono.group(2))

		return monos


	def canon_row(self):
		cnn_row = {}
		b_i = 0

		slck = {'coef':+1, 'vName':"s_"+str(self.id), 'type':'SLCK'}
		surp = {'coef':-1, 'vName':"e_"+str(self.id), 'type':'SURP'}

		if self.tip == "=":
			pass

		elif self.tip == "<=":
			self.lhs_monos.append(slck)

		elif self.tip == ">=":
			self.lhs_monos.append(surp)

		for item in self.lhs_monos:
			if item['type'] == 'VAR' and item['vName'] in cnn_row.keys():
				cnn_row[item['vName']] = cnn_row[item['vName']] + item['coef']

			elif item['type'] == 'VAR' or item['type'] == 'SLCK' or item['type'] == 'SURP':
				cnn_row[item['vName']] = item['coef']

			elif item['type'] == 'CONS':
				b_i = b_i - item['coef']

		for item in self.rhs_monos:
			if item['type'] == 'VAR' and item['vName'] in cnn_row.keys():
				cnn_row[item['vName']] = cnn_row[item['vName']] - item['coef']
				
			elif item['type'] == 'VAR':
				cnn_row[item['vName']] = -item['coef']

			elif item['type'] == 'CONS':
				b_i = b_i + item['coef']
			
		return cnn_row, b_i

    
	def canon_row_2phs(self):
		cnn_row, b_i = self.canon_row()
		new_tip = {"<=":">=" ,">=":"<=" ,"=":"="}

		artf = {'coef':+1, 'vName':"a_"+str(self.id), 'type':'ARTF'}

		if b_i < 0:
			b_i = -b_i
			self.tip = new_tip[self.tip]

			for item in cnn_row.items():
				cnn_row[item[0]] = -item[1]

		if self.tip == "=" or self.tip == ">=":
			self.lhs_monos.append(artf)
			cnn_row[artf['vName']] = artf['coef'] 

		return cnn_row, b_i
