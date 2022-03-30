# vet-t50
vet-t50.mart-info.ru

Pythhon модуль для получение данных с сайта, для отправки информации о вакцинации животных в СББЖ (Станция по Борьбе с Болезнями Животных) 
https://vet-t50.mart-info.ru/ - адрес сервера для теста выгрузки\обмена по API.
https://vet-t50.mart-info.ru/api/v2/doc  - Документация

**Аутентификация**
Аутентификация клиента основана на протоколе OAuth 2.0.
Для получения ключа доступа клиентская система отправляет POST запрос на адрес введитеадресснужногосервера**/oauth/v2/token 
( пример - https://vet-t50.mart-info.ru/oauth/v2/token )
В запросе указываются следующие параметры:
grant_type: password
client_id: id клиентской системы, выдает ТП
client_secret: секретный ключ, выдает ТП
username: имя пользователя  REST API в КАС (выдает ТП) 
password: пароль пользователя REST API в КАС (выдает ТП) 

Имя пользователя и пароль REST API создаются отдельно\индивидуально по запросу, и не являются данными для входа в КАС через web интерфейс.

В ответ сервер отправит json с токеном авторизации
```
{
    "access_token": "MmYzM2ZkZmZlZjY2ZjkxZmQ1ZmNiNmQ0MmU2NWY3ZTcwNjI4YzNj...",
    "expires_in": 1209600,
    "token_type": "bearer",
    "scope": null,
    "refresh_token": "ZmY4MzJkMTMwOWE5NzI3NWU2NGU5ZmNkOTczOWFiNzYxZmI3NmU..."
}
```
Значение access_token из данного ответа необходимо указывать в запросах в заголовке Authorization.
`Authorization: Bearer MmYzM2ZkZmZlZjY2ZjkxZmQ1ZmNiNmQ0MmU2NWY3ZTcwNjI4YzNj...`


**Обновление токена авторизации**
Для обновления токена авторизации отправляется POST запрос на адрес */oauth/v2/token
в запросе указываются следующие параметры
```
    grant_type: refresh_token
    client_id: id клиентской системы, выдает ТП
    client_secret: секретный ключ, выдает ТП
    refresh_token: "ZmY4MzJkMTMwOWE5NzI3NWU2NGU5ZmNkOTczOWFiNzYxZmI3NmU..."
```

**Получение данных**
API документация находится по адресу */api/v2/doc
1. Получение справочников
`*/api/v2/dictionary/breed?page=10&page_limit=50`
page - номер страницы
page_limit - количество элементов в ответе максимум 50
в ответ будет отправлен json со списком пород животных:
```
{
    "status": true,
    "status_code": 200,
    "data": {
        "total": 27561,
        "page_limit": 50,
        "current_page": 10,
        "last_page": 552,
        "items": [
            {
                "id": "4f8a807c-d9ce-4cb0-b76d-6e680bb3d2d6",
                "name": "русск0-европейская лайка",
                "isInvalid": false,
                "kind_id": "15d425f4-d021-4204-ba2e-4332ed214972",
                "kind_name": "Собака"
            },
            ...
            ]
    }
}
```

Остальные справочники запрашиваются аналогично.


**2. Добавление адреса**

Для добавления адреса формируется запрос POST */api/v2/location/create
в теле запроса добавляется поле address с значением адреса

В ответ будет получен идентификатор адреса
```
{
    "status": true,
    "status_code": 200,
    "message": "Success",
    "data": {
        "id": "21611c3f-042d-4150-b68a-b32d77300c70",
        "address": "Тестовый адрес добавления животного"
    }
}
```

**3. Добавление вакцинации**

Для добавления вакцинации отправляется POST запрос по адресу */api/v2/vaccination/add
В тело запроса добавляется модель данных

```
[
    {
        "animal": {
            "birthdate": "01.01.2020",
            "name": "test",
            "chip": "123",
            "gender": "MALE",
            "kind_id": "fe94d569-36b6-47bd-b2e8-fa5790945bc6",
            "breed_id": "dee5c6a7-eae3-46e9-be4c-4541845bffa0",
            "colour_id": "dfaa11ee-81f2-4cca-a053-f42bb8cf6389",
            "location_id": "21611c3f-042d-4150-b68a-b32d77300c70",
            "animal_stamps": ["маркер"],
            "owner": {
                "name": "Иван",
                "surname": "Иванов",
                "patronymic": "Иванович"
            }
        },
        "vaccination": {
            "vaccine_serial": { "id": "57badfe4-6ffb-4c81-820f-c681ca1022e4"},
            "doctor": {
                "name": "Иван",
                "surname": "Иванов",
                "patronymic": "Иванович"
            },
            "vaccination": { "date":"01.01.2021"}
        }
    }
]
```

В ответ будет отправлен идентификаторы записей и их статус
```
{
    "status": true,
    "status_code": 200,
    "message": "Success",
    "data": [
        {
            "index_array": 0,
            "record": {
                "id": "ae5dcd8c-a857-4aa1-a558-c9b47d9aa29a",
                "user_id": "a4734f20-3333-454f-84fd-4b7c6eabd68e",
                "status": "В ожидании обработки"
            }
        }
    ]
}
```


**4. Получение статуса**

Для получения статуса отправляется запрос GET по адресу */api/v2/vaccination/check?id=ae5dcd8c-a857-4aa1-a558-c9b47d9aa29a
с указанием id, для списка вакцинаций отправляется запрос POST, в запросе указывается массив идентификаторов
```
[
    "ae5dcd8c-a857-4aa1-a558-c9b47d9aa29a",
    ...
]
```

В ответ будут отправлены статусы записей

```
{
    "status": true,
    "status_code": 200,
    "message": [
        {
            "id": "ae5dcd8c-a857-4aa1-a558-c9b47d9aa29a",
            "status": true,
            "record": {
                "id": "ae5dcd8c-a857-4aa1-a558-c9b47d9aa29a",
		"user_id": "a4734f20-3333-454f-84fd-4b7c6eabd68e",
		"status": "Вожидании",
		"additional_info": []
	    }
	}
    ]
}
```
