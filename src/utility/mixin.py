from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    # check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

class TimeLimitMixin(UserPassesTestMixin):
    def test_func(self):
        from datetime import time
        import datetime, pytz
        tz      = pytz.timezone('Asia/Bangkok')
        tx_now  =   datetime.datetime.now(tz=tz)
        time_start = time(23,15)
        time_stop = time(0,15)
        if self.request.user.is_staff  :
            return True
        # return False if tx_now.hour in [23,0] or tx_now.strftime("%A") == 'Sunday' else True
        return False if is_time_between(time_start,time_stop,tx_now.time()) or tx_now.strftime("%A") == 'Sunday' else True

    def handle_no_permission(self):
        # raise Http404("ระบบกำลังปรับปรุง")
        # return redirect('users:create-profile')
        if not self.request.user.is_authenticated :
            return super(TimeLimitMixin,self).handle_no_permission()
        else :
            return render(self.request,'order/maintenance.html', {'message': 'ระบบกำลังปรับปรุง'})