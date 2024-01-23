from abc import ABC, abstractmethod
""""Абстрактный класс, класс улавливающий ошибку, класс формирующий то как пользователь будет видеть отчет с сайта"""


class ParsingError(Exception):
    """Срабатывает в случае получения ошибки при попытке получать данные с сайта"""

    def __init__(self):
        pass


class Vacancy:
    """Формирует полученные данные и выдает необходимую пользователю информацию по каждой вакансии  """
    __slots__ = ("id", "title", "url", "salary_from", "salary_to", "employer", "api")

    def __init__(self, vacancy_id, title, url, salary_from, salary_to, employer, api):
        self.id = vacancy_id
        self.title = title
        self.url = url
        self.salary_to = salary_to
        self.salary_from = salary_from
        self.employer = employer
        self.api = api

    def __gt__(self, other):
        if not other.salary_from:
            return True
        elif not self.salary_from:
            return False
        return self.salary_from >= other.salary_from

    def __str__(self):
        salary_from = f"от {self.salary_from}" if self.salary_from else "Не указана"
        salary_to = f"До {self.salary_to}" if self.salary_to else "Не указана"
        if self.salary_from is None and self.salary_to is None:
            salary_from = "Не указана"
            salary_to = "Не указана"
        return f'Вакансия:\"{self.title}"(id: "{self.id}") \n Компания: \"{self.employer}\' \n Зарплата: {salary_from} - {salary_to} \nURL: {self.url}'


class Engine(ABC):
    """Абстрактный класс"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass
