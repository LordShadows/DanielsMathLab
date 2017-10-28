class BranchBoundaryMethod(object):
	matrix = []
	main_matrix = []
	results_vector = []
	path = ''
	INF = 1000000
	main_result = 0

	def __init__(self, POST):
		i = 1
		self.matrix = []
		while (True):
			if (i != 1):
				try:
					POST["i" + str(i) + "j1"]
				except KeyError:
					break
			j = 1
			buf = []
			while (True):
				try:
					if(i == j):
						buf.append(self.INF)
					else:
						if(POST["i" + str(i) + "j" + str(j)] == ''):
							buf.append(0)
						else:
							buf.append(int(POST["i" + str(i) + "j" + str(j)]))
					j = j + 1
				except KeyError:
					break
			self.matrix.append(buf)
			i = i + 1

	def console_print_matrix(self):
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[i])):
				if(self.matrix[i][j] == self.INF):
					print('inf', end=' ')
				else:
					print(self.matrix[i][j], end=' ')
			print()

	def console_print_temp_matrix(self, temp_matrix):
		for i in range(len(temp_matrix)):
			for j in range(len(temp_matrix)):
				print(temp_matrix[i][j], end=' ')
			print()

	def __get_main_matrix(self):
		self.main_matrix = []
		for i in range(len(self.matrix)):
			temp = []
			for j in range(len(self.matrix[i])):
				if(self.matrix[i][j] == self.INF):
					temp.append('∞')
				else:
					temp.append(self.matrix[i][j])
			self.main_matrix.append(temp)
	
	#Вычисляем минимальные элементы по строкам и вычитаем их из элементов строки
	def __delete_min_in_rows(self, temp_matrix):
		size = len(temp_matrix)
		tmp = 0
		result = 0
		while True:
			minimum = temp_matrix[tmp][0]
			for j in range(0, size):
				if (temp_matrix[tmp][j] < minimum):
					minimum = temp_matrix[tmp][j]
			result = result + minimum
			for j in range(0, size):
				if(temp_matrix[tmp][j] != self.INF):
					temp_matrix[tmp][j] = temp_matrix[tmp][j] - minimum
			tmp = tmp + 1
			if(not tmp < size):
				return result
				break

	#Вычисляем минимальные элементы по столбцам и вычитаем их из элементов столбца
	def __delete_min_in_columns(self, temp_matrix):
		size = len(temp_matrix)
		tmp = 0
		result = 0
		while True:
			minimum = temp_matrix[0][tmp]
			for j in range(0, size):
				if (temp_matrix[j][tmp] < minimum):
					minimum = temp_matrix[j][tmp]
			result = result + minimum
			for j in range(0, size):
				if(temp_matrix[j][tmp] != self.INF):
					temp_matrix[j][tmp] = temp_matrix[j][tmp] - minimum
			tmp = tmp + 1
			if(not tmp < size):
				return result
				break

	#Нахождение дополнительных чисел для 0
	def __additional_number_for_zero(self):
		size = len(self.matrix)
		additional_numbers = []
		for i in range(0, size):
			tmp = []
			for j in range(0, size):
				if (self.matrix[i][j] == 0):
					min_column = self.INF
					min_row = self.INF
					for m in range(0, size):
						if (m != i):
							if (min_column > self.matrix[m][j]):
								min_column = self.matrix[m][j]
					for m in range(0, size):
						if (m != j):
							if (min_row > self.matrix[i][m]):
								min_row = self.matrix[i][m]
					min_sum = min_column + min_row
					tmp.append(min_sum)
				else:
					tmp.append(-1)
			additional_numbers.append(tmp)
		return additional_numbers

	#Построение пути
	def __generate_path(self):
		if (len(self.results_vector) > 0):
			temp_index = 0
			temp_path = '(' + str(self.results_vector[0][0]) + ', ' + str(self.results_vector[0][1]) + ') '
			for i in range(1, len(self.results_vector)):
				for j in range(0, len(self.results_vector)):
					if(self.results_vector[j][0] == self.results_vector[temp_index][1]):
						temp_path = temp_path + '(' + str(self.results_vector[j][0]) + ', ' + str(self.results_vector[j][1]) + ') '
						temp_index = j
						break
			self.path = temp_path
			print(temp_path)



	#Основной метод вычисления
	def calculate(self):
		self.__get_main_matrix()
		self.results_vector = []
		self.main_result = 0
		size = len(self.matrix)
		count = len(self.matrix)

		row_numbers = []
		column_numbers = []

		for i in range (0, len(self.matrix)):
			row_numbers.append(i + 1)
			column_numbers.append(i + 1)

		self.main_result = self.main_result + self.__delete_min_in_rows(self.matrix)
		self.main_result = self.main_result + self.__delete_min_in_columns(self.matrix)

		print()
		self.console_print_matrix()
		print()

		while (count >= 2):
			count = count - 1 
			additional_numbers = self.__additional_number_for_zero()

			print()
			self.console_print_temp_matrix(additional_numbers)
			print()
			
			result = [0, 0]

			#Находим ноль с максимальным дополнительным числом
			maximum = additional_numbers[0][0]
			for i in range(0, size):
				for j in range(0, size):
					if (maximum < additional_numbers[i][j]):
						maximum = additional_numbers[i][j]
						result[0] = i
						result[1] = j

			#С включением дуги
			tmpmas1 = []
			tmpsum1 = 0
			for i in range(0, size):
				if (i != result[0]):
					tmp = []
					for j in range(0, size):
						if (j != result[1]):
							tmp.append(self.matrix[i][j])
					tmpmas1.append(tmp)
				

			row_position = -1
			column_position = -1
			for i in range(0,  len(row_numbers)):
				if (row_numbers[i] == column_numbers[result[1]]):
					row_position = i
					break
			for i in range(0,  len(column_numbers)):
				if (column_numbers[i] == row_numbers[result[0]]):
					column_position = i
					break

			print('[' + str(row_position) + ', ' + str(column_position) + '] = inf')
			
			if(row_position != -1 and column_position != -1):
				if(row_position > result[0]):
					row_position = row_position - 1
				if(column_position > result[1]):
					column_position = column_position - 1
				tmpmas1[row_position][column_position] = self.INF

			tmpsum1 = self.__delete_min_in_rows(tmpmas1)
			tmpsum1 = tmpsum1 + self.__delete_min_in_columns(tmpmas1)

			#Без включения дуги
			tmpmas2 = self.matrix[:]
			tmpsum2 = 0

			tmpmas2[result[0]][result[1]] = self.INF
			
			tmpsum2 = self.__delete_min_in_rows(tmpmas2)
			tmpsum2 = tmpsum1 + self.__delete_min_in_columns(tmpmas2)

			if(tmpsum1 <= tmpsum2):
				self.matrix = tmpmas1[:]
				point = []
				point.append(row_numbers[result[0]])
				point.append(column_numbers[result[1]])
				point.append(0)
				self.results_vector.append(point)
				self.main_result = self.main_result + tmpsum1
				print('(' + str(row_numbers[result[0]]) + ', ' + str(column_numbers[result[1]]) + ')')
				print()
				size = size - 1
				row_numbers.pop(result[0])
				column_numbers.pop(result[1])
			else:
				self.matrix = tmpmas2[:]
				point = []
				point.append(row_numbers[result[1]])
				point.append(column_numbers[result[0]])
				point.append(1)
				self.results_vector.append(point)
				self.main_result = self.main_result + tmpsum2
				print('(' + str(row_numbers[result[1]]) + ', ' + str(column_numbers[result[0]]) + ')')
				print()
			self.console_print_matrix()
			print()

		
		point = []
		point.append(row_numbers[0])
		point.append(column_numbers[0])
		point.append(0)
		self.results_vector.append(point)

		for point in self.results_vector:
			print('(' + str(point[0]) + ', ' + str(point[1]) + ')')
		
		print()
		self.__generate_path()
		
		print()
		print('Result:' + str(self.main_result))
			
