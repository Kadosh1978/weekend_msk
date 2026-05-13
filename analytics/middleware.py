import geoip2.database
from django.conf import settings
from .models import PageVisit
from django_user_agents.utils import get_user_agent

class PageVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(('/admin', '/static', '/media')):
            session_key = request.session.session_key
            if session_key is None:
                request.session.save()
                session_key = request.session.session_key

            referrer = request.META.get('HTTP_REFERER', '')
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')[:500]
            user_agent = get_user_agent(request)
            device_type = 'pc'
            if user_agent.is_mobile:
                device_type = 'mobile'
            elif user_agent.is_tablet:
                device_type = 'tablet'
            elif user_agent.is_bot:
                device_type = 'bot'
            browser_family = user_agent.browser.family[:100] if user_agent.browser.family else ''
            os_family = user_agent.os.family[:100] if user_agent.os.family else ''

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR', '')

            # Определение страны по IP
            country_name = ''
            geoip_reader = None
            try:
                geoip_reader = geoip2.database.Reader(settings.GEOIP_PATH)
                response = geoip_reader.country(ip_address)
                country_name = response.country.name
            except Exception:
                pass
            finally:
                if geoip_reader:
                    geoip_reader.close()

            PageVisit.objects.update_or_create(
                session_key=session_key,
                path=request.path,
                defaults={
                    'referrer': referrer,
                    'user_agent_string': user_agent_string,
                    'ip_address': ip_address,
                    'device_type': device_type,
                    'browser_family': browser_family,
                    'os_family': os_family,
                    'country_name': country_name,
                }
            )
        response = self.get_response(request)
        return response