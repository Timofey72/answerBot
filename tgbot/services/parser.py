import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

useragent = UserAgent()
headers = {
    'user-agent': useragent.random
}


def get_content(url: str) -> list:
    try:
        s = requests.Session()
        response = s.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        answers = soup.find('div', class_='block-tasks').find_all('div', class_='block-tasks_task')

        lst = []
        for id, answer in enumerate(answers):
            question = answer.find('div', class_='block-tasks-question_text').find('p', id='quest').text
            ans = answer.find('div', class_='block-tasks-answer_text').find('p', id='ans').text
            lst.append([id + 1, question, ans])
        return lst
    except Exception:
        pass


def create_url_and_start_parser(url: str):
    lst = url.split('/')
    [lst.remove(i) for i in lst if i == '']

    title_test = lst[-1]
    if title_test in 'start':
        title_test = lst[-2]

    return get_content(url=f'https://qixanswers.ru/cdz/skysmart/{title_test}')
