from django.http import JsonResponse
import json, os

def estados(request):
	PROJECT_DIR = os.path.dirname(__file__)
	json_data = open(PROJECT_DIR + '/static/Estados.json')
	data = json.load(json_data)
	return JsonResponse(data, safe=False)

def estado(request, id):
	PROJECT_DIR = os.path.dirname(__file__)
	json_data = open(PROJECT_DIR + '/static/Estados.json')
	data = json.load(json_data)
	filtered_dict = [x for x in data if x['ID'] == id]
	return JsonResponse(filtered_dict, safe=False)

def cidades(request, id):
	PROJECT_DIR = os.path.dirname(__file__)
	json_data = open(PROJECT_DIR + '/static/Cidades.json')
	data = json.load(json_data)
	filtered_dict = [x for x in data if x['Estado'] == id]
	return JsonResponse(filtered_dict, safe=False)

def cidade(request, id):
	PROJECT_DIR = os.path.dirname(__file__)
	json_data = open(PROJECT_DIR + '/static/Cidades.json')
	data = json.load(json_data)
	filtered_dict = [x for x in data if x['ID'] == id]
	return JsonResponse(filtered_dict, safe=False)	


