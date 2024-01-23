import json

from classes import Vacancy


class Connector:
    """Сохранение необходимых для работы данных в файл json, выбранных по ключевому слову
    Функции сортировки"""

    def __init__(self, keyword, vacancies_json):
        self.user_input = None
        self.keyword = keyword
        self.__filename = f"{self.keyword.title()}.json"
        self.insert(vacancies_json)

    def insert(self, vacancies_json):  # сохранение данных в формате json
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, ensure_ascii=False, indent=4)

    def select(self):  # чтение файла json и формирование экземпляра класса Vacancy
        with open(self.__filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        vacancies = [Vacancy(x["id"], x["title"], x["url"], x["salary_from"], x["salary_to"], x["employer"], x["api"])
                     for x in data]
        return vacancies

    def sorted_by_salary_max(self):  # сортировка по минимальной з/п от большего к меньшему
        vacancies = self.select()
        vacancies = sorted(vacancies, reverse=True)
        return vacancies

    def sorted_by_salary_min(self):  # сортировка по минимальной з/п от меньшего к большему
        vacancies = self.select()
        vacancies = sorted(vacancies)
        return vacancies

    def delete_vacancy(self, user_input):  # удаление вакансии
        self.user_input = user_input
        with open(f"{self.keyword.title()}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            index = 0
            for vacancy in data:
                if vacancy["id"] in self.user_input:
                    data.pop(index)
                    print(f"Вакансия '{vacancy['title']}' удалена!")
                elif self.user_input not in vacancy:
                    pass
                index += 1
            self.insert(data)
        return self.select()
