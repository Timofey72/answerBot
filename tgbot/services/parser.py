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
        blocks = soup.find('div', class_='block-tasks').find_all('div', class_='block-tasks_task')

        questions_lst = []
        answers_lst = []
        for block in blocks:
            # Вопросы
            question_title = block.find('vim-instruction').text
            questions_lst.append(question_title)

            # Ответы
            ans_lst = [i.text for i in block.find('vim-input-answers').find_all('vim-input-item')]
            # for text in block.find_all('li'):
            #     for ans in text.find_all('vim-select-item', correct='true'):
            #         ans_lst.append(ans.find('vim-select-item-title').text)
            answers_lst.append(ans_lst)

        return [questions_lst, answers_lst]
    except Exception:
        pass


def create_url_and_start_parser(url: str):
    lst = url.split('/')
    [lst.remove(i) for i in lst if i == '']

    title_test = lst[-1]
    if title_test in 'start':
        title_test = lst[-2]

    return get_content(url=f'https://qixanswers.ru/cdz/skysmart/{title_test}')
