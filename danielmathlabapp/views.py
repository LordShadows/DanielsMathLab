from django.shortcuts import render
from danielmathlabapp.sources.MathematicalModel import *
from danielmathlabapp.sources.GeneticMethod import *

def main(request):
    return render(request, 'danielmathlabapp/main.html', {})

def calculate(request):
	if request.method == 'POST':
		mm = MathematicalModel(request.POST['search'])
		if mm.is_command_correct:
			gm = GeneticMethod(mm)
			gm.run()
	return render(request, 'danielmathlabapp/calculate-results.html', { 'objective_function' : mm.objective_function,
	'constraints' : mm.constraints, 'regions' : mm.string_regions, 'result' : gm.generate_result(),
	'last_generation' : gm.generate_result_genetic, 'other_points' : gm.generate_other_points(), 'value_points' : gm.value_points })