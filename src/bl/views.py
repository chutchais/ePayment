from django.shortcuts import render
import urllib3
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.
def index(request,bl=''):
	context = {}
	bl_url = f"{reverse_lazy('bl:home')}"
	# print(bl_url)
		# print (f"{reverse_lazy('order:list')}booking/")
	context['import_bl_url'] = f'{bl_url}api/bl/'
	context['bl'] = bl
	return render(request, 'bl/index.html', context=context)

def container(request):
	context = {}
	bl_url = f"{reverse_lazy('bl:home')}"
	# print(bl_url)
		# print (f"{reverse_lazy('order:list')}booking/")
	context['import_container_url'] = f'{bl_url}api/container/'
	return render(request, 'bl/container.html', context=context)


def get_bl_info(request,bl):
	import json
	http = urllib3.PoolManager()
	# print ('get_booking_info')
	r = http.request('GET', f'http://192.168.10.16:5000/bl/{bl}')
	# return json.loads(r.data.decode('utf-8'))
	response = JsonResponse(json.loads(r.data.decode('utf-8')), safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response

# Added on Oct 16,2020 -- To support Import container info API
def get_container_info(request,container):
	import json
	http = urllib3.PoolManager()
	# print ('get_booking_info')
	r = http.request('GET', f'http://192.168.10.16:5000/container/{container}')
	# return json.loads(r.data.decode('utf-8'))
	response = JsonResponse(json.loads(r.data.decode('utf-8')), safe=False)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Headers'] = '*'
	return response
