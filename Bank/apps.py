from django.apps import AppConfig


class BankConfig(AppConfig):
    name = 'Bank'

    def ready(self):
        import Bank.signals

