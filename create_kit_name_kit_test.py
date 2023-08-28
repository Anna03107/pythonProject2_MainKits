import sender_stand_request
import data
import requests
import configuration

# Функция для получения токена
def get_new_user_token(): #Изменила функцию в согласно комментариям ревью, табуляцию привела в соответствие. Добавила в функции для позитивных и негативных проверок
    response_user = requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=data.user_body,
                         headers=data.headers)
    return response_user.json()["authToken"]

#Функция, которая заменяет значение параметра name
def get_kit_body(name):
    current_kit_body = data.kit_body.copy()
    current_kit_body["name"] = name
    return current_kit_body

# Функция для позитивной проверки
def positive_assert(name):
    data.auth_token["Authorization"] = "Bearer " + get_new_user_token() #Добавила строку
    kit_body = get_kit_body(name)
    response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
# Передает хедер, в котором есть  "Content-Type" и "Authorization"
    assert response.status_code == 201
# Проверяется, что поле "name" в ответе и запросе совпадают
    assert response.json()["name"] == name

# Функция для негативной проверки
def negative_assert_code_400(kit_body):
    data.auth_token["Authorization"] = "Bearer " + get_new_user_token() #Добавила строку
    response = sender_stand_request.post_new_client_kit(kit_body, data.auth_token)
# Передает хедер, в котором есть "Content-Type" и "Authorization"
# Проверяется, что код ответа равен 400
    assert response.status_code == 400
    assert response.json()["code"] == 400

#Тест №1: Допустимое количество символов (1)
def test_create_kit_1_letter_success():
    positive_assert("a")

#Тест №2: Допустимое количество символов (511)
def test_create_kit_511_success():
    positive_assert("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab\
    cdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcda\
    bcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcd\
    abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc\
    dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdab\
    cdabcdabcdabcdabcdabcdabcdabcdabC")

#Тест №3: Количество символов меньше допустимого (0)
def test_create_kit_0_failed():
    kit_body = get_kit_body("")
    negative_assert_code_400(kit_body)

#Тест №4: Количество символов больше допустимого (512)
def test_create_kit_512_failed():
    kit_body = get_kit_body("Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc\
        dabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabc\
        abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
        abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd\
        abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")
    negative_assert_code_400(kit_body)

#Тест №5: Разрешены английские буквы
def test_create_kit_english_success():
    positive_assert("QWErty")

#Тест №6: Разрешены русские буквы
def test_create_kit_rus_success():
    positive_assert("Мария")

#Тест №7: Разрешены спецсимволы
def test_create_kit_symbol_success():
    positive_assert("\"№%@\",")

#Тест №8: Разрешены пробелы
def test_create_kit_space_success():
    positive_assert("Человек и КО")

#Тест №9: Разрешены цифры
def test_create_kit_numbers_success():
    positive_assert("123")

#Тест №10: Параметр не передан в запросе
def test_create_kit_no_name_failed():
    data.kit_body = {} #пустой запрос
    response = sender_stand_request.post_new_client_kit(data.kit_body, data.auth_token) #передаем информацию на сервер
    assert response.status_code == 400 #проверяем код ответа

#Тест №11: Передан другой тип параметра (число)
def test_create_kit_wrong_type_failed():
    kit_body = get_kit_body(123)
    negative_assert_code_400(kit_body)