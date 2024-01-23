import os
from abc import ABC
from classes import Engine, ParsingError
import requests
from dotenv import load_dotenv


class Superjob(Engine, ABC):
    """Получение данных с сайта superjob.ru
        Обработка данных, приведение к необходимому, для дальнейшей работы, виду
        конвертация зарплаты в рубли"""

    def __init__(self, keyword):
        load_dotenv()
        self.__header = {"X-Api-App-Id": os.getenv("SUPERJOB_API_KEY")}
        self.__params = {
            "keyword": keyword,
            "page": 0,
            "count": 100,
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary, currency):  # статический метод для конвертации з/п в рубли в случае если она указана в валюте
        formatted_salary = None
        if salary and salary != 0:
            formatted_salary = salary if currency == 'rub' else salary * 80
        return formatted_salary

    def get_request(self):  # запрос данных непосредственно с сайта
        response = requests.get('https://api.superjob.ru/2.0/vacancies',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()["objects"]

    def get_formatted_vacancies(self):  # отбор необходимых параметров и придание структуры данным
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            formatted_vacancies.append({
                'id': str(vacancy['id']),
                'title': vacancy['profession'],
                'url': vacancy['link'],
                'salary_from': self.get_salary(vacancy['payment_from'], vacancy['currency']),
                'salary_to': self.get_salary(vacancy['payment_to'], vacancy['currency']),
                'employer': vacancy['firm_name'],
                'api': 'Superjob',
            })
        return formatted_vacancies

    def get_vacancies(self, pages_count=1):  # парсинг страниц и формирование отчета для пользователя
        while self.__params['page'] < pages_count:
            print(f"Superjob, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print("Ошибка получения данных")
                break
            print(f"Найдено ({len(values)}) вакансий")
            self.__vacancies.extend(values)
            self.__params["page"] += 1
