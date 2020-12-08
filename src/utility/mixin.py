from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render

class TimeLimitMixin(UserPassesTestMixin):
    def test_func(self):
        import datetime, pytz
        tz      = pytz.timezone('Asia/Bangkok')
        tx_now  =   datetime.datetime.now(tz=tz)
        if self.request.user.is_staff  :
            return True
        return False if tx_now.hour in [23,0] or tx_now.strftime("%A") == 'Sunday' else True

    def handle_no_permission(self):
        # raise Http404("ระบบกำลังปรับปรุง")
        # return redirect('users:create-profile')
        if not self.request.user.is_authenticated :
            return super(TimeLimitMixin,self).handle_no_permission()
        else :
            return render(self.request,'order/maintenance.html', {'message': 'ระบบกำลังปรับปรุง'})