import requests
from pprint import pprint


class HhVacancyParsing:
    def __init__(self, name=None):
        self.name = name

    @property
    def get_request_employers(self):
        """
        Метод, возвращающий json по умолчанию 10 компаний
        """
        list_employers = []
        if self.name is None:
            params = {
                "per_page": 10,
                "sort_by": "by_vacancies_open"
            }
            response = requests.get("http://api.hh.ru/employers/", params)
            return response.json()["items"]
        else:
            for i in self.name:
                params = {
                    "per_page": 10,
                    "sort_by": "by_vacancies_open",
                    "text": i
                }
                response = requests.get("http://api.hh.ru/employers/", params)
                list_employers.extend(response.json()["items"])
        return list_employers

    def get_employers_sort(self):
        """
        Метод сортировки 10 компаний, возвращается список с id компании, название вакансии
        """
        result = self.get_request_employers
        employers = []
        for employer in result:
            employers.append({"id": int(employer["id"]), "name": employer["name"]})
        return employers

    @classmethod
    def get_vacancies_from_company(cls, id_company):
        """
        Метод возвращающий json вакансий
        """
        params = {
            "per_page": 20,
            "employer_id": id_company,
            'only_with_salary': "true"
        }
        response = requests.get("http://api.hh.ru/vacancies/", params)
        return response.json()["items"]

    def get_all_vacancies(self):
        """
        Метод забирает список с метода get_employers_sort, и список get_vacancies_from_company
        и сортирует все вакансии по определенному id компании и складывает все в список
        """
        employers = self.get_employers_sort()
        vacancies = []
        for employer in employers:
            vacancies.extend(self.get_vacancies_from_company(employer["id"]))
        return vacancies

    def filter_vacancies(self):
        """
        Метод фильтрации вакансий по нужному нам формату, id, name, salary_from, salary_to, url, emloyer
        """
        vacancies = self.get_all_vacancies()
        filter_vacancy = []
        for vacancy in vacancies:
            if vacancy["salary"]["from"] is None:
                vacancy["salary"]["from"] = 0
            if vacancy["salary"]["to"] is None:
                vacancy["salary"]["to"] = 0
            filter_vacancy.append({
                "id": int(vacancy["id"]),
                "name": vacancy["name"],
                "salary_from": vacancy["salary"]["from"],
                "salary_to": vacancy["salary"]["to"],
                "url": vacancy["alternate_url"],
                "employer": int(vacancy["employer"]["id"]),
                "employer_name": vacancy["employer"]["name"]
            })
        return filter_vacancy


if __name__ == '__main__':
    hh = HhVacancyParsing()
    pprint(hh.filter_vacancies())