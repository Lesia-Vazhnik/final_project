from flask import Flask, request
import logging
import json
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Как тебя зовут?'
        sessionStorage[user_id] = {
            'first_name': None,  # здесь будет храниться имя
            'information': False  # здесь информация о том, что пользователь запросил информацию. По умолчанию False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name

            res['response']['text'] = f'Приятно познакомиться, {first_name.title()}. Я Алиса. Что ты хочешь узнать?'
            res['response']['buttons'] = [
                {
                    'title': 'Информация про конкретный город',
                    'hide': True
                },
                {
                    'title': 'Информация про страну',
                    'hide': True
                },
                {
                    'title': 'Информация по миру',
                    'hide': True
                },
                {
                    'title': 'Симптомы',
                    'hide': True
                },
                {
                    'title': 'Рекомендации',
                    'hide': True
                },
                {
                    'title': "Чем заняться в карантин?",
                    'hide': True
                }
            ]
    else:
        if not sessionStorage[user_id]['information']:
            # запрос не поступил, значит мы ожидаем запрос.
            if '' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            elif '' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            elif '' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            elif '' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            elif '' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            elif '' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            else:
                res['response']['text'] = ('К сожалению у меня нет такого раздела. Выберите из перечисленных' +
                                           ' или перейдите на официальный сайт, где такая информация может быть.')
                res['response']['buttons'] = [
                    {
                        'title': 'Информация про конкретный город',
                        'hide': True
                    },
                    {
                        'title': 'Информация про страну',
                        'hide': True
                    },
                    {
                        'title': 'Информация по миру',
                        'hide': True
                    },
                    {
                        'title': 'Симптомы',
                        'hide': True
                    },
                    {
                        'title': 'Рекомендации',
                        'hide': True
                    },
                    {
                        'title': "Чем заняться в карантин?",
                        'hide': True
                    }
                ]
        else:
            if 'Информация про конкретный город' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функц
            elif 'Информация про страну' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            elif 'Информация по миру' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию

            elif 'Симптомы' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию
                symptomes(res, req)
            elif 'Рекомендации' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию
                recomendation(res, req)
            elif 'Чем заняться в карантин?' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                # вызываем необходимую функцию


def symptomes(res, req):
    user_id = req['session']['user_id']
    res['response']['text'] = "sep=\n".join(['Основными признаками наличия коронавируса у человека являются:',
                                             '— слабость, усталость',
                                             '— затрудненное дыхание',
                                             '— высокая температура',
                                             '— кашель (сухой или с небольшим количеством мокроты) и/или боль в горле',
                                             'По симптоматике коронавирус схож с простудой' +
                                             ' и респираторными заболеваниями.',
                                             'Особое внимание стоит обратить на одышку:' +
                                             ' при ее наличии немедленно обратитесь к врачу.'])


def recomendation(res, req):
    user_id = req['session']['user_id']
    res['response']['text'] = "sep=\n".join(['Регулярно обрабатывайте руки спиртосодержащим средством' +
                                             ' или мойте их с мылом. ',
                                             'Держитесь от людей на расстоянии как минимум 1 метра, особенно если у' +
                                             ' них кашель, насморк и повышенная температура.',
                                             'По возможности, не трогайте руками глаза, нос и рот.',
                                             'При кашле и чихании прикрывайте рот и нос салфеткой или сгибом локтя;' +
                                             ' сразу выкидывайте салфетку в контейнер для мусора с крышкой и' +
                                             ' обрабатывайте руки спиртосодержащим антисептиком или мойте их' +
                                             ' водой с мылом.',
                                             'При повышении температуры, появлении кашля и затруднении дыхания как' +
                                             ' можно быстрее обращайтесь за медицинской помощью.',
                                             'По симптоматике коронавирус схож с простудой' +
                                             ' и респираторными заболеваниями.',
                                             'Следите за новейшей информацией и выполняйте рекомендации медицинских' +
                                             ' специалистов.'])



def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name', то возвращаем её значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()
