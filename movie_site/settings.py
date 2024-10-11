from dotenv import load_dotenv
import os

load_dotenv('../.env')

DEBUG = os.getenv('DEBUG')

if DEBUG == 'True':
    from .deploy_settings.dev import *
else:
    print('aaaa')
    from .deploy_settings.prod import *
