from django.apps import AppConfig


class OperateConfig(AppConfig):
    name = 'operate'
    verbose_name = '操作'

    def ready(self):
        import operate.signals