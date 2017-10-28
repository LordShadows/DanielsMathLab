from itertools import groupby
import re
import math

class MathematicalModel(object):
	command_string = ""
	variables = []
	objective_function = ""
	constraints = []
	regions = []
	string_regions = []
	method = ""
	act = ""

	#Для генетического алгоритма
	individuals_number = 0
	generations_number = 0 
	survivors_number = 0 
	genetic_method = ""

	#Данные об ошибке
	is_command_correct = True
	error = ""

	#Полный список ключевых слов
	standard_fuctions = ['math', 'abs', 'factorial', 'exp', 'log', 'pow', 'sqrt', 'cos', 'sin', 'tan', 'degrees', 'radians']
	standard_comparison_signs = ['>=', '<=', '==', '<', '>', '!=']
	standard_operators = ['**', '+', '-', '/', '*', '=', '.']
	standard_symbols = ['(', ')']
	standard_commands = ['maximize', 'minimize', 'use', 'in', 'pass', 'and', 'from', 'to']
	standard_methods = ['simplex', 'genetic']
	genetic_details = ['crossing', 'mutation', 'hybrid']
	genetic_method_param = ['{', '}', 'individuals_number', 'generations_number', 'survivors_number',':']
	
	def __init__(self, command_string):
		print('Command string: ' + command_string)
		self.command_string = command_string
		if self.__is_correct(command_string):
			self.__parsing()
			if self.is_command_correct:
				print('Obj. function: ' + str(self.objective_function))
				print('Variables: ' + str(self.variables))
				print('Constraints: ' + str(self.constraints))
				print('Regions: ' + str(self.regions))
				print('Method: ' + self.method)
			else:
				print('Error: ' + self.error)
		else:
			print('Error: ' + self.error)
		
	def __is_correct(self, command_string):
		buf_string = command_string
		for x in self.standard_fuctions:
			buf_string = buf_string.replace(x, '')
		for x in self.standard_comparison_signs:
			buf_string = buf_string.replace(x, '')
		for x in self.standard_operators:
			buf_string = buf_string.replace(x, '')
		for x in self.standard_symbols:
			buf_string = buf_string.replace(x, '')
		for x in self.standard_commands:
			buf_string = buf_string.replace(x, '')
		for x in self.standard_methods:
			buf_string = buf_string.replace(x, '')
		for x in self.genetic_details:
			buf_string = buf_string.replace(x, '')
		for x in self.genetic_method_param:
			buf_string = buf_string.replace(x, '')
		buf_string = buf_string.replace(' ', '')
		print(buf_string)		
		if re.match(r'^[x0-9]+$', buf_string):
			if command_string.find('maximize ') == -1 and command_string.find('minimize ') == -1:
				self.is_command_correct = False
				self.error = "Отсутвует ключевое слово [maximize]([minimize])."
				return False
			if command_string.find(' in ') == -1:
				self.is_command_correct = False
				self.error = "Отсутвует ключевое слово [in], указывающее на ограничения."
				return False
			if command_string.find(' from ') == -1:
				self.is_command_correct = False
				self.error = "Отсутвует ключевое слово [from], указывающее на облать нахождения."
				return False
			if command_string.find(' using ') == -1:
				self.is_command_correct = False
				self.error = "Отсутвует ключевое слово [using], указывающее на метод."
				return False
			return True
		else:
			self.is_command_correct = False
			self.error = "В строке найдены посторонние символы или функции."
			return False
	
	def __is_correct_obj_funcrion(self):
		buf_string = self.objective_function
		buf_string_complite = self.objective_function
		for x in self.standard_fuctions:
			buf_string = buf_string.replace(x, '')
		for x in self.standard_operators:
			buf_string = buf_string.replace(x, '')
		for x in self.standard_symbols:
			buf_string = buf_string.replace(x, '')
		buf_string = buf_string.replace(' ', '')
		if re.match(r'^[x0-9]+$', buf_string) and buf_string != "":
			for i in range(len(self.variables) - 1, -1, -1):
				buf_string_complite = buf_string_complite.replace(self.variables[i], '1')
			try:
				if type(eval(buf_string_complite)) == int or type(eval(buf_string_complite)) == float:
					return True
				else:
					self.is_command_correct = False
					self.error = "Ошибка ввода целевой функции."
					return False
			except Exception as err:
				print(err)
				self.is_command_correct = False
				self.error = "Ошибка ввода целевой функции."
				return False
		else:
			self.is_command_correct = False
			self.error = "Ошибка ввода целевой функции."
			return False

	def __is_correct_constraints(self):
		for constraint in self.constraints:
			buf_string = constraint
			buf_string_complite = constraint
			for x in self.standard_fuctions:
				buf_string = buf_string.replace(x, '')
			for x in self.standard_comparison_signs:
				buf_string = buf_string.replace(x, '')
			for x in self.standard_operators:
				buf_string = buf_string.replace(x, '')
			for x in self.standard_symbols:
				buf_string = buf_string.replace(x, '')
			buf_string = buf_string.replace(' ', '')
			if re.match(r'^[x0-9]+$', buf_string) and buf_string != "":
				for i in range(len(self.variables) - 1, -1, -1):
					buf_string_complite = buf_string_complite.replace(self.variables[i], '1')
				try:
					if str(eval(buf_string_complite)) == "True" or str(eval(buf_string_complite)) == "False":
						return True
					else:
						self.is_command_correct = False
						self.error = "Ошибка ввода одного либо нескольких ограничений."
						return False
				except:
					self.is_command_correct = False
					self.error = "Ошибка ввода одного либо нескольких ограничений."
					return False
			else:
				self.is_command_correct = False
				self.error = "Ошибка ввода одного либо нескольких ограничений."
				return False

	def __parsing(self):
		if self.command_string.find('maximize') != -1:
			self.act = "maximize"
			self.objective_function = self.command_string[(self.command_string.find('maximize') + 8):(self.command_string.find(' in ')):1]
		else:
			self.act = "minimize"
			self.objective_function = self.command_string[(self.command_string.find('minimize') + 8):(self.command_string.find(' in ')):1]
		self.objective_function = self.objective_function.strip()
		
		self.variables = re.findall(r'x[0-9]+', self.objective_function)
		self.variables.sort()
		self.variables = [el for el, _ in groupby(self.variables)]
		
		if self.command_string.find('simplex') != -1:
			self.method = "simplex"
		else:
			self.method = "genetic"
		
		constraints = self.command_string[(self.command_string.find(' in ') + 4):(self.command_string.find(' from ')):1].split(' and ')
		self.constraints = []
		for constraint in constraints:
			self.constraints.append(constraint.strip())
		
		regions = self.command_string[(self.command_string.find(' from ') + 6):(self.command_string.find(' using ')):1].split(' and ')
		self.regions = []
		self.string_regions = []
		for region in regions:
			try:
				self.string_regions.append(region.strip())
				index = self.variables.index((re.search(r'x[0-9]+', region)).group(0).strip())
				pair = []
				for el in region[(region.rfind('=') + 1):len(region):1].split('to'):
					pair.append(float(el.strip()))
				self.regions.insert(index, pair)
			except:
				self.is_command_correct = False
				self.error = "Неправильно задана одлать определения."
				return
		if len(self.regions) != len(self.variables):
			self.is_command_correct = False
			self.error = "Не задана облать принимаемых значений для одной либо нескольких переменных."
			return
		if self.method == 'genetic':
			if self.command_string.find('crossing') != -1:
				self.genetic_method = 'crossing'
			elif self.command_string.find('mutation') != -1:
				self.genetic_method = 'mutation'
			elif self.command_string.find('hybrid') != -1:
				self.genetic_method = 'hybrid'
			buf_params = self.command_string[(self.command_string.rfind('(') + 1):(self.command_string.rfind(')')):1].split('and')
			if len(buf_params) == 3:
				if buf_params[0].strip().isdigit():
					self.generations_number = int(buf_params[0].strip())
				else:
					self.is_command_correct = False
					self.error = "Ошибка при выявлении количества поколений."
					return
				if buf_params[1].strip().isdigit():
					self.individuals_number = int(buf_params[1].strip())
				else:
					self.is_command_correct = False
					self.error = "Ошибка при выявлении количества особей."
					return
				if buf_params[2].strip().isdigit():
					self.survivors_number = int(buf_params[2].strip())
				else:
					self.is_command_correct = False
					self.error = "Ошибка при выявлении количества выживаемых."
					return
			else:
				self.is_command_correct = False
				self.error = "Неправильно указаны параметры генетического алгоритма."
				return
		if not self.__is_correct_obj_funcrion():
			return
		self.__is_correct_constraints()