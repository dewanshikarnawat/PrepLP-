from django.apps import AppConfig
from transformers import BartTokenizer, BartForConditionalGeneration



class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    # def ready(self):
    #     BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    #     BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
