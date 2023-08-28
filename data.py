headers = {
    "Content-Type": "application/json"
}
user_body = {
    "firstName": "Анна",
    "phone": "+79161986203",
    "address": "г. Москва, ул. Погонная, д. 3"
}
kit_body = {
    "name": "Суп"
}
auth_token = {"Authorization": "Bearer {authToken}",
              "Content-Type": "application/json"
} #В этот хедер добавлено Content-Type": "application/json