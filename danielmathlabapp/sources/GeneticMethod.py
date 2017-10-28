from danielmathlabapp.sources.Method import *
import random
import math

class GeneticMethod(Method):
	value_points = []
	other_points = []
	min_parental_interest = 0.6
	max_parental_interest = 0.8
	mutation = 0.5

	def __init__(self, mathematical_model):
		Method.__init__(self, mathematical_model)

	def sort_function(self, inputStr):
		return inputStr[2]
	
	def run(self):
		self.list_result_history = []
		self.value_points = []
		self.grafic_points = []
		generation = []
		for i in range(0, self.mathematical_model.individuals_number):
			while True:
				point = []
				for j in range(0, len(self.mathematical_model.variables)):
					x = random.uniform(self.mathematical_model.regions[j][0], self.mathematical_model.regions[j][1])
					point.append(x)
				fun = self.get_constraints_function_value(point)
				if str(fun) != 'False':
					point.append(fun)
					generation.append(point)
					break
		if self.mathematical_model.act == 'maximize':
			generation.sort(key=self.sort_function, reverse=True)
		else:
			generation.sort(key=self.sort_function)
		if self.mathematical_model.survivors_number < len(generation):
			self.other_points = self.other_points + generation[self.mathematical_model.survivors_number :: 1]
			generation = generation[0 : self.mathematical_model.survivors_number : 1]
		self.value_points.append(generation)
		self.result = generation[0]

		for i in range(1, self.mathematical_model.generations_number + 1):
			generation = []
			for old_point in self.value_points[i - 1]:
				for k in range(0, self.mathematical_model.individuals_number):
					while True:
						point = []
						second_parent_point = random.randint(0, self.mathematical_model.survivors_number - 1)
						parental_interest = random.uniform(self.min_parental_interest, self.max_parental_interest)
						print(second_parent_point)
						print(parental_interest)
						for j in range(0, len(self.mathematical_model.variables)):
							x = old_point[j] * parental_interest + self.value_points[i - 1][second_parent_point][j] * (1 - parental_interest)
							x = x + random.uniform(-1.0 * self.mutation, self.mutation)
							point.append(x)
						fun = self.get_constraints_function_value(point)
						if str(fun) != 'False':
							point.append(fun)
							generation.append(point)
							break
			if self.mathematical_model.act == 'maximize':
				generation.sort(key=self.sort_function, reverse=True)
			else:
				generation.sort(key=self.sort_function)
			if self.mathematical_model.survivors_number < len(generation):
				self.other_points = self.other_points + generation[self.mathematical_model.survivors_number :: 1]
				generation = generation[0 : self.mathematical_model.survivors_number : 1]
			self.value_points.append(generation)
			self.result = generation[0]

		self.generate_history_genetic()
		self.print_history()

	def generate_history_genetic(self):
		self.list_result_history = []
		i = 0
		for generation in self.value_points:
			self.list_result_history.append("Поколение " + str(i) + ":")
			i = i + 1
			for point in generation:
				point_string = ""
				for j in range(0, len(self.mathematical_model.variables)):
					point_string = point_string + self.mathematical_model.variables[j] + " = %.2f " % point[j]
				point_string = point_string + "f = %.3f" % point[len(point) - 1]
				self.list_result_history.append(point_string)

	def generate_other_points(self):
		other_results = []
		for point in self.other_points:
			new_point = []
			for j in range(0, len(self.mathematical_model.variables)):
				new_point.append("%.4f" % point[j])
			new_point.append("%.6f" % point[len(point) - 1])
			other_results.append(new_point)
		return other_results

	def generate_result_genetic(self):
		list_result_history = []
		generation = self.value_points[len(self.value_points) - 1]
		for point in generation:
			point_string = ""
			for j in range(0, len(self.mathematical_model.variables)):
				point_string = point_string + self.mathematical_model.variables[j] + " = %.3f " % point[j]
			point_string = point_string + "f = %.5f" % point[len(point) - 1]
			list_result_history.append(point_string)
		return list_result_history