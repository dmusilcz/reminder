from django.apps import AppConfig
import vinaigrette


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        # Import the model requiring translation
        ReminderChoice = self.get_model("ReminderChoice")

        # Register fields to translate
        vinaigrette.register(ReminderChoice, ['field', ])
