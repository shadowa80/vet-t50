#-*- coding: utf-8 -*-
'''
Получение данных с сайта 
https://vet-t50.mart-info.ru/ - адрес сервера для теста выгрузки \ обмена по API.


https://vet-t50.mart-info.ru/api/v2/doc  - Документация

Аутентификация
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
{
	"access_token": "MmYzM2ZkZmZlZjY2ZjkxZmQ1ZmNiNmQ0MmU2NWY3ZTcwNjI4YzNj...",
	"expires_in": 1209600,
"token_type": "bearer",
	"scope": null,
	"refresh_token": "ZmY4MzJkMTMwOWE5NzI3NWU2NGU5ZmNkOTczOWFiNzYxZmI3NmU..."
}
Значение access_token из данного ответа необходимо указывать в запросах в заголовке Authorization.
Authorization: Bearer MmYzM2ZkZmZlZjY2ZjkxZmQ1ZmNiNmQ0MmU2NWY3ZTcwNjI4YzNj...


Обновление токена авторизации
Для обновления токена авторизации отправляется POST запрос на адрес **/oauth/v2/token
в запросе указываются следующие параметры
grant_type: refresh_token
client_id: id клиентской системы, выдает ТП
client_secret: секретный ключ, выдает ТП
refresh_token: "ZmY4MzJkMTMwOWE5NzI3NWU2NGU5ZmNkOTczOWFiNzYxZmI3NmU..."


Получение данных
API документация находится по адресу **/api/v2/doc
1. Получение справочников
**/api/v2/dictionary/breed?page=10&page_limit=50
page - номер страницы
page_limit - количество элементов в ответе максимум 50
в ответ будет отправлен json со списком пород животных:
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
Остальные справочники запрашиваются аналогично.


2. Добавление адреса

Для добавления адреса формируется запрос POST **/api/v2/location/create
в теле запроса добавляется поле address с значением адреса

В ответ будет получен идентификатор адреса

{
	"status": true,
	"status_code": 200,
	"message": "Success",
	"data": {
		"id": "21611c3f-042d-4150-b68a-b32d77300c70",
"address": "Тестовый адрес добавления животного"
	}
}

3. Добавление вакцинации

Для добавления вакцинации отправляется POST запрос по адресу **/api/v2/vaccination/add
В тело запроса добавляется модель данных

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
			"animal_stamps": [
				"маркер"
			],
			"owner": {
				"name": "Иван",
				"surname": "Иванов",
				"patronymic": "Иванович"
			}
		},
		"vaccination": {

			"vaccine_serial": {
				"id": "57badfe4-6ffb-4c81-820f-c681ca1022e4"
			},
			"doctor": {
				"name": "Иван",
				"surname": "Иванов",
"patronymic": "Иванович"
			},
			"vaccination": {
				"date":"01.01.2021"
			}
		}
	}
]

В ответ будет отправлен идентификаторы записей и их статус
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



4. Получение статуса

Для получения статуса отправляется запрос GET по адресу **/api/v2/vaccination/check?id=ae5dcd8c-a857-4aa1-a558-c9b47d9aa29a
с указанием id, для списка вакцинаций отправляется запрос POST, в запросе указывается массив идентификаторов
[
	"ae5dcd8c-a857-4aa1-a558-c9b47d9aa29a",
...
]

В ответ будут отправлены статусы записей

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
'''
import logging
logging.basicConfig()
logger = logging.getLogger('VetT50.py')
logger.setLevel(logging.DEBUG)

import datetime
import requests
# отключем вывод ошибок о сертификате
requests.urllib3.disable_warnings()

#from requests_oauthlib import OAuth2Session
import configparser

class MartInfo(object):
	''' Класс для работы с сайтом mart-info.ru '''

class VetT50(MartInfo):
	_URLS = {
		'domain': 			'https://vet-t50.mart-info.ru',
		'token':			'/oauth/v2/token',
		'breed':			'/api/v2/dictionary/breed',			# (GET) Список пород
		'colour':			'/api/v2/dictionary/colour',		# (GET) Список мастей
		'kind':				'/api/v2/dictionary/kind',			# (GET) Список типов животных
		'station':			'/api/v2/dictionary/station',		# (GET) Список станций
		'subdivision':		'/api/v2/dictionary/subdivision',	# (GET) Список клиник
		'vaccine-series':	'/api/v2/dictionary/vaccine-series',# (GET) Список вакцин
		#'location':			'/api/v2/dictionary/location',		# Для отладки

		'location_add':		'/api/v2/location/create',			# (POST) Добавление адреса животного

		'vaccination_add':	'/api/v2/vaccination/add',			# (POST) Эту модель отправляет клиентская система. * В animal заполняется или id или все остальные поля. * Тип, вид, масть заполняется или id или name.
		'vaccination':		'/api/v2/vaccination/check',		# (GET/POST) Проверка статуса обработки вакцины. 

		'animal':			'/api/v2/animal/list',				# (GET) 
		'animal_add':		'/api/v2/animal/create',			# (POST) 
		'animal_get':		'/api/v2/animal/get',				# (GET) 
		'animal_delete':	'/api/v2/animal/delete',			# (DELETE) 
	}

	_SESSION = requests.Session()
	_USER_AGENT = None
	client_id=		''
	client_secret=	''
	username=		''
	password=		''
	_auth_status = False
	def __init__(self):
		''' Инициация приложения '''
		self._SESSION.headers.update({'User-Agent':self._USER_AGENT})
		self._SESSION.headers.update({'Content-Type':"application/x-www-form-urlencoded"})
		#
		config = configparser.ConfigParser()
		config.read('../VetT50.ini')
		self._USER_AGENT = config['vet-t50.mart-info.ru'].get('user_agent')
		self.client_id = config['vet-t50.mart-info.ru'].get('client_id')
		self.client_secret = config['vet-t50.mart-info.ru'].get('client_secret')
		self.username = config['vet-t50.mart-info.ru'].get('username')
		self.password = config['vet-t50.mart-info.ru'].get('password')
		
		self.auth()
	def getURL(self, key):
		''' Возвращаем полный урл по ключу '''
		#if not self._auth_status: return None
		return self._URLS.get('domain')+self._URLS.get(key)
	def auth(self):
		''' 
		Аутентификация клиента основана на протоколе OAuth 2.0 
		В POST запросе указываются следующие параметры:
			grant_type: password
			client_id: 	<ID клиентской системы, выдает ТП>
			client_secret: <секретный ключ, выдает ТП>
			username: имя пользователя  REST API в КАС (выдает ТП) <LOGIN>
			password: пароль пользователя REST API  в КАС (выдает ТП) <PASSWD>
		Возвращаем:
			{'access_token': '', 'expires_in': 3600, 'token_type': 'bearer', 'scope': None, 'refresh_token': ''}
		'''
		url = self.getURL('token')
		logger.debug('auth start: %s' % url)
		data = {
			'grant_type': 'password',
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'username': self.username,
			'password': self.password,
		}
		res = self._SESSION.post(url, data=data, verify=False)
		if res.status_code == 200:
			# Устанавливаем авторизацию в заголовок
			# Authorization: Bearer MmYzM2ZkZmZlZjY2ZjkxZmQ1ZmNiNmQ0MmU2NWY3ZTcwNjI4YzN
			self._SESSION.headers.update({'Authorization': 'Bearer '+res.json().get('access_token')})
			logger.debug('Установили header: %s' % self._SESSION.headers)
			# Если авторизация прошла успешно, устанавливаем тег
			self._auth_status = True
			return True
		else:
			logger.debug('Ошибка авторизации')
			return False
	def _getPages(self, url, page_limit=50, page=1, *args, **params):
		'''
		Получаем страницы
		'''
		result = []
		LIMIT = 3 		# Устанавливаем лимит для отладки.
		LIMIT_SET_FLAG = False	# Флаг, установки лимита
		#page = 540 		# Формируем начальную страницу для теста
		empty = False	# Ставим флаг, что данные не пустые
		#params={'page_limit':page_limit, 'page':current_page}
		#params = {}	# Параметры и фильтры
		#if kind_name: 	params['kind_name'] = kind_name
		#if breed_name: 	params['breed_name'] = breed_name
		#params['kind_name'] = 'собака'
		if args: logger.debug('_getPages args: %s' % args)
		if params: logger.debug('_getPages params: %s' % params)
		while self._auth_status and not empty:
			# Формируем параметры для запроса
			params['page_limit'] = page_limit
			params['page']  = page
			logger.debug("_getPages get from url: %s" % url)
			res = self._SESSION.get(url, params=params)
			logger.debug("_getPages res: %s" % res.status_code)
			if  res.status_code == 200:
				#logger.debug("_getPages res.json(): %s" % res.json())
				data = res.json()['data']
				# Наполняем данными
				result += data.get('items')
				# Если установлен LIMIT, значит получаем последнюю страницу и устанавливаем текущую меньше на указанное число
				if LIMIT>0 and not LIMIT_SET_FLAG:
					page = data['last_page'] - LIMIT + 1
					LIMIT_SET_FLAG = True 				# Устанавливаем флаг, что бы не сбрасывать страницу
				#print ("%s -> %s:" % (data.get('last_page'), data.get('current_page') ))
				page += 1 	# Увеличиваем страницу на единицу для получения следующей
				# Если 'current_page' == 'last_page' - значит это крайняя страница
				if data['current_page'] == data['last_page']: break
				# Если данные пустые - выходим
				if not data.get('items'): break
			else:
				logger.error("_getPages error getting page (status_code: %s)" % res.status_code)
				break
		logger.debug("_getPages len result = %s" % len(result))
		return result

	def getBreeds(self, **params):
		''' 
		Получаем список пород
			page_limit - Записей на странице
			page - Номер страницы
		ФИЛЬТР:
			breed_name	Поиск по наименованию записи. Фильтр не сработает если имеется поле breed_id. Либо breed_id, либо breed_name.
			breed_id	Поиск по ID записи. Фильтр не сработает если имеется поле breed_name. Либо breed_id, либо breed_name.
			kind_name	Поиск по типу животного. Фильтр не сработает если имеется поле kind_id. Либо kind_id, либо kind_name.
			kind_id		Поиск по ID типа животного. Фильтр не сработает если имеется поле kind_name. Либо kind_id, либо kind_name.
			page		Номер страницы
			page_limit	Количество возвращаемых элементов, максимально 50

		ВОЗВРАЩАЕМ:
			{'id', 'name', 'kind_id', 'kind_name'}
		}
		'''
		# Если передали ID и не передали breed_id, считаем что его и передали
		MAIN_FIELD_NAME = 'breed_id'
		if params.get('id') and not params.get(MAIN_FIELD_NAME):
			params[MAIN_FIELD_NAME] = params['id']
			# Удаляем ключ ID
			del (params['id'])
		url = self.getURL('breed')
		logger.debug('getBreed: %s' % url)
		result = []
		return self._getPages(url, **params)

	def getColour(self, **params):
		'''
		Получаем список мастей
		ФЛЬТР:
			name 		Поиск по наименованию записи. Фильтр не сработает если имеется поле name. Либо id, либо name.
			id			Поиск по ID записи. Фильтр не сработает если имеется поле id. Либо id, либо name.
			page		Номер страницы
			page_limit	Количество возвращаемых элементов, максимально 50
		ВОЗВРАЩАЕМ:
			{'id', 'name'}

		'''
		url = self.getURL('colour')
		logger.debug('getColour: %s' % url)
		result = self._getPages(url, **params)
		if params.get('full_match') and params.get('name'):
			# Полное сопоставление по полю name
			result = list(filter(lambda x: x['name'] == params.get('name'), result))
		return result

	def getKind(self, **params):
		'''
		Получаем список типов животных
		ФИЛЬТР:
			name		Поиск по наименованию записи. Фильтр не сработает если имеется поле name. Либо id, либо name.
			id			Поиск по ID записи. Фильтр не сработает если имеется поле id. Либо id, либо name.
			page		Номер страницы
			page_limit	Количество возвращаемых элементов, максимально 50
		ВОЗВРАЩАЕМ:
			{'id', 'name'}
		'''
		url = self.getURL('kind')
		logger.debug('getKind: %s' % url)
		result = self._getPages(url, **params)
		if params.get('full_match') and params.get('name'):
			# Полное сопоставление по полю name
			result = list(filter(lambda x: x['name'] == params.get('name'), result))
		return result

	def getStation(self, **params):
		'''
		Запрос списка станций
		{'id': '51a75803-d5b6-4a7e-b9c6-830d887ccb31', 'name': 'Ветеринарная станция по Ступинскому и Каширскому районам'}
		{'id': 'bbf8b31b-938a-4789-8103-3a36ffbb9615', 'name': 'Ступинская участковая ветеринарная лечебница'}
		ФИЛЬТР:
			name - Поиск по наименованию записи. Фильтр не сработает если имеется поле id. Либо id, либо name.
			breed_id - Поиск по ID записи. Фильтр не сработает если имеется поле name. Либо id, либо name.
			page - Номер страницы
			page_limit - Количество возвращаемых элементов, максимально 50
		ВОЗВРАЩАЕМ:
			array of objects ({id: 'uuid', name: 'string'})
		'''
		url = self.getURL('station')
		logger.debug('getStation: %s' % url)
		result = self._getPages(url, **params)
		return result

	def getSubdivision(self, **params):
		'''
		Запрос списка клиник
		{	'id': 'beaed9e0-1e29-11e4-b379-00215e28e44e', 
			'name': 'ИП Чистов Максим Сергеевич', 
			'station_id': '51a75803-d5b6-4a7e-b9c6-830d887ccb31', 
			'station_name': 'Ветеринарная станция по Ступинскому и Каширскому районам'
		}
		ФИЛЬТР:
			name		Поиск по наименованию записи. Фильтр не сработает если имеется поле id. Либо id, либо name.
			id			Поиск по ID записи. Фильтр не сработает если имеется поле name. Либо id, либо name.
			station_name Поиск по наименованию станции. Фильтр не сработает если имеется поле station_id. Либо station_id, либо station_name.
			station_id	Поиск по ID станции. Фильтр не сработает если имеется поле station_name. Либо station_id, либо station_name.
			page		Номер страницы
			page_limit	Количество возвращаемых элементов, максимально 50
		ВОЗВРАЩАЕМ:
			array of objects ({id: 'uuid', name: 'string', station_id: 'uuid', station_name: 'string'})
		'''
		url = self.getURL('subdivision')
		logger.debug('getSubdivision: %s' % url)
		result = self._getPages(url, **params)
		return result

		
	def getVaccineSeries(self, **params):
		'''
		Запрос списка вакцин
		ФИЛЬТР:
			serial_number	Поиск по наименованию записи. Фильтр не сработает если имеется поле serial_id. Либо serial_id, либо serial_number.
			serial_id		Поиск по ID записи. Фильтр не сработает если имеется поле serial_number. Либо serial_id, либо serial_number.
			vaccine_name	Поиск по наименованию вакцины. Фильтр не сработает если имеется поле vaccine_id. Либо vaccine_name, либо vaccine_id.
			vaccine_id		Поиск по ID вакцины. Фильтр не сработает если имеется поле vaccine_name. Либо vaccine_name, либо vaccine_id.
			page			Номер страницы
			page_limit		Количество возвращаемых элементов, максимально 50
		ВОЗВРАЩАЕМ:
			array of objects ({id: string, serialNumber: string, expires: dateTime, vaccine_name: string})
		'''
		url = self.getURL('vaccine-series')
		logger.debug('getVaccineSeries: %s' % url)
		result = self._getPages(url, **params)
		for i in result:
			# Получаем дату (срок действия вакцины)
			d = i.get('expires')
			try:
				date = datetime.datetime.strptime(d.split('+')[0], '%Y-%m-%dT%H:%M:%S')
				# Добавляем дату в нужном формате в вывод
				i['expires_date'] = date
			except:
				logger.error("Error getting date: <%s>" % d)
		return result

	def getLocation(self, **params):
		'''
		!!! Функция не работает
		ФИЛЬТР:
	
		ВОЗВРАЩАЕМ:
			array of objects ({id: 'uuid', name: 'string'})
		'''
		url = self.getURL('location')
		logger.debug('getLocation: %s' % url)
		result = self._getPages(url, **params)
		return result

	def getAnimal(self, **params):
		'''
		Получаем данные о животных
		Parameters
		'''
		url = self.getURL('animal')
		logger.debug('getAnimal: %s' % url)
		result = self._getPages(url, **params)
		return result

	def getVaccination(self):
		'''
		Проверяем статус обработки вакцины. GET с ID в запросе

		Parameters
			id	string	true	[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}	Идентификатор вакцинации, метод GET
		'''
		url = self.getURL('vaccination')
		logger.debug('getVaccination: %s' % url)
		result = self._getPages(url, **params)
		return result

	

	def addVaccination(self, data):
		'''
		POST /api/v2/vaccination/add
		Эту модель отправляет клиентская система. 
		* В animal заполняется или id или все остальные поля. 
		* Тип, вид, масть заполняется или id или name.
		vaccinations	json	true	
		[ 
			{ 	animal: 
					{ 	birthdate: 'datetime', name: 'string', chip: 'string', gender: 'MALE|FEMALE', kind_id: 'uuid', 
						breed_id: 'uuid', colour_id: 'uuid', location_id: 'uuid', animal_stamps: [ 'string' ], 
						owner: { name: 'string', surname: 'string', patronymic: 'string' },
					}, 
				vaccination: 
					{ 	vaccinationDate: 'datetime', vaccine_serial: { id: 'uuid' }, 
						doctor: { name: 'string', surname: 'string', patronymic: 'string' }, 
						vaccination: { date: 'datetime' } 
					}
			}
		]
		'''
		url = self.getURL('vaccination_add')
		logger.debug('addVaccination: %s' % url)
		logger.debug('addVaccination data: %s' % data)
		result = []
		



if __name__ == '__main__':
	vet = VetT50()
	kind = vet.getKind(name="Кошка", full_match=True)
	breed = vet.getBreeds(breed_name="Шотландская прямоухая", kind_id=kind[0]['id'])
	colour = vet.getColour(name="Серый", full_match=True)
	colour = vet.getColour(name="Серый")
	animal = vet.getAnimal()
	print ("A:", animal)
	vactinations = vet.getVaccineSeries(vaccine_name='Nobivac Rabies', serial_number="A551A02")
	print ("K:", kind)
	print ("B:", breed)
	print ("C:", colour)
	print ("V:", vactinations)
	for i in vactinations:
		print ("%s (%s) - %s" % (i['vaccine_name'], i['serialNumber'], i['expires_date'].strftime('%d.%m.%Y')))
	

	#print (len(breed))
	#help(vet)
	#help(requests.api)
	# Климовских Светлана Анатольевна	
	# Домодедово ,	
	# Кошка	
	# Тимофей	
	# Самец	
	# Серый	
	# Шотландская прямоухая			
	# 25.12.2021	
	# 30.03.2022	
	# Nobivac Rabies	
	# A551A02	
	# 20.08.2020	
	# 20.04.2024	
	# Ненашева Маргарита Сергеевна

	vacc_info = {
		"animal": {
			"birthdate": "25.12.2021",
			"name": "Тимофей",
			"chip": "643093330075051",
			"gender": "MALE",										# MALE|FEMALE
			"kind_id": "fe94d569-36b6-47bd-b2e8-fa5790945bc6",		# Тип животного (Кошка)
			"breed_id": "dee5c6a7-eae3-46e9-be4c-4541845bffa0",		# Порода животного (Шотландская прямоухая)
			"colour_id": "dfaa11ee-81f2-4cca-a053-f42bb8cf6389",	# Ограс животного (Серый)
			"location_id": "21611c3f-042d-4150-b68a-b32d77300c70",	# Адрес содержания
			"animal_stamps": ["MHR1171"],
			"owner": {
				"name": "Иван",
				"surname": "Иванов",
				"patronymic": "Иванович"
			}
		},
		"vaccination": {
			"vaccine_serial": {
				"id": "57badfe4-6ffb-4c81-820f-c681ca1022e4"		# Вакцина
			},
			"doctor": {
				"name": "Светлана",
				"surname": "Климовских",
				"patronymic": "Анатольевна"
			},
			"vaccination": {
				"date":"30.03.2022"
			}
		}
	}
	vaccination = vet.addVaccination(vacc_info)