from abc import ABC
from classes import Engine, ParsingError
import requests


class HeadHunter(Engine, ABC):
    """Получение данных с сайта hh.ru
    Обработка данных, приведение к необходимому, для дальнейшей работы, виду
    конвертация зарплаты в рубли"""

    def __init__(self, keyword):
        self.__header = {
            "User-Agent": "Mozila/5.0 (platform; rv:geckoversion) Gecko/gecotrail Firefox/firefoxversion"}
        self.__params = {
            "text": keyword,
            "page": 0,
            "per_page": 100,
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):  # статический метод для конвертации з/п в рубли в случае если она указана в валюте
        formatted_salary = [None, None]
        if salary and salary["from"] and salary["from"] != 0:
            formatted_salary[0] = salary["from"] if salary["currency"].lower() == "rur" else salary["from"] * 80
        if salary and salary["to"] and salary["to"] != 0:
            formatted_salary[1] = salary["to"] if salary["currency"].lower() == "rur" else salary["to"] * 80
        return formatted_salary

    def get_request(self) -> object:  # запрос данных непосредственно с сайта
        response = requests.get("https://api.hh.ru/vacancies",
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()["items"]

    def get_formatted_vacancies(self):  # отбор необходимых параметров и придание структуры данным
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy["salary"])
            formatted_vacancies.append({
                "id": vacancy["id"],
                "title": vacancy["name"],
                "url": vacancy["alternate_url"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "employer": vacancy["employer"]["name"],
                "api": "HeadHunter",
            })
        return formatted_vacancies

    def get_vacancies(self, pages_count=1):  # парсинг страниц и формирование отчета для пользователя
        while self.__params["page"] < pages_count:
            print(f"HeadHunter, парсинг страницы {self.__params['page'] + 1}", end=":")
            try:
                values = self.get_request()
            except ParsingError:
                print("Ошибка получения данных!")
                break
            print(f"Найдено ({len(values)}) вакансий")
            self.__vacancies.extend(values)
            self.__params["page"] += 1
