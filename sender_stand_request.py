import configuration
import requests

#Создание нового набора
def post_new_client_kit (kit_body,auth_token):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_KITS_PATH,
                         json=kit_body,
                         headers=auth_token)
#Удален отладочный код (строки 10-12)