from django.db import models

class PageVisit(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    path = models.CharField(max_length=500, db_index=True)
    # +++ Новые поля +++
    referrer = models.CharField(max_length=2000, blank=True, null=True)
    user_agent_string = models.CharField(max_length=500, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    # Детали устройства (заполняются позже)
    device_type = models.CharField(max_length=50, blank=True, null=True)  # mobile, tablet, pc, bot
    browser_family = models.CharField(max_length=100, blank=True, null=True)
    os_family = models.CharField(max_length=100, blank=True, null=True)
    # +++ Конец новых полей +++
    first_seen = models.DateTimeField(auto_now_add=True)
    country_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['session_key', 'path']),
        ]

    def __str__(self):
        return f"{self.session_key} - {self.path}"