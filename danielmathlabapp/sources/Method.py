import math

class Method(object):
	list_result_history = []
	result = []
	
	def __init__(self, mathematical_model):
		self.mathematical_model = mathematical_model

	def get_function_value(self, variable_values):
		if len(self.mathematical_model.variables) == len(variable_values):
			obj_function = self.mathematical_model.objective_function
			for i in range(0, len(variable_values)):
				if self.__isfloat(variable_values[i]):
					obj_function = obj_function.replace(self.mathematical_model.variables[i], str(variable_values[i]))
			return eval(obj_function)
		else:
			print('Error >>> Количество переменных не совпадает.')
			return False

	def is_satisfies_constraints(self, variable_values):
		if len(self.mathematical_model.variables) == len(variable_values):
			constraints = self.mathematical_model.constraints
			for constraint in constraints:
				for i in range(0, len(variable_values)):
					if self.__isfloat(variable_values[i]):
						constraint = constraint.replace(self.mathematical_model.variables[i], str(variable_values[i]))
				if eval(constraint) == False:
					return False
			return True
		else:
			print('Error >>> Количество переменных не совпадает.')
			return False

	def get_constraints_function_value(self, variable_values):
		if self.is_satisfies_constraints(variable_values):
			return self.get_function_value(variable_values)
		else:
			return False 

	def __isfloat(self, value):
		try:
			float(value)
			return True
		except ValueError:
			return False

	def print_history(self):
		for line in self.list_result_history:
			print(line)

	def generate_result(self):
		point_string = ""
		for j in range(0, len(self.mathematical_model.variables)):
			point_string = point_string + self.mathematical_model.variables[j] + " = %.2f, " % self.result[j]
		point_string = point_string + "f = %.3f" % self.result[len(self.result) - 1]
		return point_string
