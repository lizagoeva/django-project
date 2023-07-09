from django.http import HttpRequest, HttpResponseForbidden
from datetime import datetime, timedelta


class RequestsThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.latest_requests = {}

    def __call__(self, request: HttpRequest):
        now = datetime.now()
        min_req_interval = timedelta(seconds=5)
        req_ip = request.META['REMOTE_ADDR']
        if req_ip in self.latest_requests:
            ip_interval = now - self.latest_requests[req_ip]
            if ip_interval < min_req_interval:
                time_to_wait = min_req_interval - ip_interval
                print('слишком частые запросы, подождите ещё {}.{} секунд'.format(
                    time_to_wait.seconds, str(time_to_wait.microseconds)[:2]
                ))
                return HttpResponseForbidden('''
                IP {} is sending too many requests, latest at {}.
                Minimum request interval is {}, wait {}.{} more seconds please
                '''.format(
                    req_ip,
                    self.latest_requests[req_ip].strftime('%H:%M:%S, %d.%m.%Y'),
                    min_req_interval.seconds,
                    time_to_wait.seconds,
                    str(time_to_wait.microseconds)[:2],
                ))
            else:
                self.latest_requests[req_ip] = now
                print('Теперь последний запрос с ip {} был сделан {}'.format(
                    req_ip,
                    self.latest_requests[req_ip].strftime('%d.%m.%Y, %H:%M:%S')
                ))
        else:
            self.latest_requests[req_ip] = now
            print('добавили ip {} со временем {}'.format(
                req_ip,
                self.latest_requests[req_ip].strftime('%d.%m.%Y, %H:%M:%S')
            ))
        request.latest_request = self.latest_requests[req_ip].strftime('%d.%m.%Y, %H:%M:%S')
        response = self.get_response(request)
        return response
