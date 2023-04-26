import logging
from django.utils import timezone
from user_agents import parse


class UserLogsMiddleware:
    def __init__(self, get_response):
        self.response = get_response
        self.info_logger = logging.getLogger('info_logs')
        self.error_logger = logging.getLogger('error_logs')

    def __call__(self, request):
        response = self.response(request)

        log_data = {
            'time': timezone.now(),
            'status_code': response.status_code,
            "host": request.headers.get('Host', 'unknwon'),
            "request_method": request.method,
            "request_path": request.get_full_path(),
            "os": parse(request.META.get('HTTP_USER_AGENT', 'unknwon')).os.family,
            'data': response,
        }

        if response.status_code > 100 and response.status_code < 202:
            self.info_logger.info(log_data)
        else:
            self.error_logger.error(log_data)

        return response
