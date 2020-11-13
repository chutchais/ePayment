from django_q.tasks import async_task

import urllib3
import json
from django.http import JsonResponse

# -----------Berth---------------
# Get from Autoberth (192.168.10.20:8003) for 2 weeks onward.
def get_berth_info_by_terminal(terminal,weeks=2):

    import datetime, pytz
    tz      = pytz.timezone('Asia/Bangkok')
    now_tz  = datetime.datetime.now(tz=tz)
    start_date = now_tz - datetime.timedelta(date.weekday()).strftime("%Y-%m-%d")
	end_date = start_week + datetime.timedelta(7*weeks).strftime("%Y-%m-%d")
    print(f'Pulling berth of {terminal} ,from {start_date} to {end_date}')

	import json
	# Redis KET , LCB1_BERTH , LCMT_BERTH
	key = f'{terminal}_BERTH'
	ttl = 60*60*4 #4 hours

	# 1) check Data exist in Redis
	# 2) if yes return json
	# 3) if No , get data from Auto berth
	# 4) Save to Redis
	# 5) return json
	# http = urllib3.PoolManager()
	# r = http.request('GET', f'http://192.168.10.20:8003/api/voy/?f=2020-08-01&t=2020-08-06&terminal={terminal}')
	# response = JsonResponse(json.loads(r.data.decode('utf-8')), safe=False)
	# response['Access-Control-Allow-Origin'] = '*'
	# response['Access-Control-Allow-Headers'] = '*'
	return True#response