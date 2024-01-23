from clsConnector import Connector
from SJcls import Superjob
from HHcls import HeadHunter


def main():
	vacancies_json = []
	keyword = input("Здравствуйте! Введите ключевое слово для поиска вакансии: ")
	# keyword = "Python"

	hh = HeadHunter(keyword)
	sj = Superjob(keyword)
	for api in (hh, sj):
		api.get_vacancies(pages_count=1)
		vacancies_json.extend(api.get_formatted_vacancies())

	connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

	while True:
		command = input(
			"1 - Вывести список вакансий; \n"
			"2 - Сортировка по зарплате от большего к меньшему:\n"
			"3 - Сортировка по зарплате от меньшего к большему:\n"
			"4 - Удалить вакансию:\n"
			"exit - для сохранения результатов поиска и выхода.\n"
		)
		if command.lower() == "exit":
			break
		elif command == "1":
			vacancies = connector.select()

		elif command == "2":
			vacancies = connector.sorted_by_salary_max()

		elif command == "3":
			vacancies = connector.sorted_by_salary_min()

		elif command == "4":

			user_input = str(input("Введите название вакансии: "))
			vacancies = connector.delete_vacancy(user_input)

		else:
			print("Некорректный ввод!\n")

		for vacancy in vacancies:
			print(vacancy, end='\n\n')


if __name__ == "__main__":
	main()
