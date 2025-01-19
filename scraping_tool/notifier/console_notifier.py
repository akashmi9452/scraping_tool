from scraping_tool.notifier.base_notifier import BaseNotifier

class ConsoleNotifier(BaseNotifier):
    def notify(self, message: str):
        print(message)