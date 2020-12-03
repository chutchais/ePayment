from django_q.tasks import async_task

import urllib3
import requests
import json
from django.http import JsonResponse


def update_invoice_by_order(order_obj):

	print(f'Update invoice of {order_obj}')

	import json
	invoice_url = 'http://192.168.10.16:5002/order/'
	# invoice_url = 'http://127.0.0.1:5002/order/'
	r = requests.get(f'{invoice_url}{order_obj.booking}')
	json_obj = r.json()
	# jsondata = '[{"container":"BEAU2601651","invoice":"1234"}]'
	# json_obj = json.loads(jsondata)

	for container in order_obj.containers.all():
		inv = get_invoice(json_obj,container.container)
		if inv != '':
			# Update Container
			container.invoice = inv
			container.save()
			print(f'Update invoice of {container} -- Success')
	# for inv in r.json():
		# Only vessel type Vessel or Barge

	return True#response

def get_invoice(json_object, container_number):
	invoice_list = [obj['invoice'] for obj in json_object if obj['container']==container_number]
	return invoice_list[0] if len(invoice_list) > 0 else ''