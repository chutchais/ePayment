from django_q.tasks import async_task

import urllib3
import requests
import json
from django.http import JsonResponse
import redis
db = redis.StrictRedis('redis', 6379,db=0, charset="utf-8", decode_responses=True) #Production


# -----------Berth---------------
# Get from Autoberth (192.168.10.20:8003) for 2 weeks onward.
def get_berth_info_by_terminal(terminal,weeks=2):
	from datetime import date
	import datetime, pytz
	tz      = pytz.timezone('Asia/Bangkok')
	now_tz  = datetime.datetime.now(tz=tz)
	start_date = now_tz - datetime.timedelta(now_tz.weekday())
	end_date = start_date + datetime.timedelta(7*weeks)

	start_date_str 	= start_date.strftime("%Y-%m-%d")
	end_date_str	= end_date.strftime("%Y-%m-%d")

	print(f'Pulling berth of {terminal} ,from {start_date_str} to {end_date_str}')

	import json
	# Redis KET , LCB1_BERTH , LCMT_BERTH
	key = f'{terminal}_VOY'
	ttl = 60*60*4 #4 hours

	# 1) check Data exist in Redis
	# 2) if yes return json
	# 3) if No , get data from Auto berth
	# 4) Save to Redis
	# 5) return json
	voy_url = 'http://192.168.10.20:8003/api/voy/'
	r = requests.get(f'{voy_url}?f={start_date_str}&t={end_date_str}&terminal={terminal}')
	json_str = r.json()
	# Save Data to Redis
	# 1) Save JSON
	key = f'{terminal}_VOY_JSON'
	db.set(key,json.dumps(json_str)) 
	db.expire(key, ttl)

	#2) Save Vessel
	# 2.1) VESSEL:CODE:{code} -->Vessel Name (ttl=0)
	# 2.2) VESSEL:{code}:{voy-in} -->Voy Detail (ttl=2weeks)
	# 2.3) VESSEL:{code}:{voy-out} -->Voy Detail (ttl=2weeks)
	for voy in r.json():
		# Only vessel type Vessel or Barge
		
		if voy['vessel_type'] in ['VESSEL','BARGE']:
			#2.1) Vessel name
			vessel_code = voy['code']
			key = f'VESSEL:CODE:{vessel_code}'
			db.set(key,voy['vessel'])
			#2.2)Voy in
			voy_str = voy['voy']
			voy_arr = voy_str.split('-')
			voyin = voy_arr[0]
			key = f'VESSEL:{vessel_code}:{voyin}'
			db.set(key,json.dumps(voy))
			#2.3)Voy out
			voyout = voyin if len(voy_arr) == 1 else voy_arr[1]
			key = f'VESSEL:{vessel_code}:{voyout}'
			db.set(key,json.dumps(voy))



	return True#response