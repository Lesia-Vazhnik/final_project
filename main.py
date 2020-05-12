from flask import Flask, request
import logging
import json
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}
card = {'карта': "1540737/3c5fad08bd419a235347"}


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
                    'title': 'Информация про количество заболевших',
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
                    'title': 'Самоизоляция',
                    'hide': True
                },
                {
                    'title': 'Посмотреть карту заражения',
                    'hide': True
                }
            ]
    else:
        if not sessionStorage[user_id]['information']:
            # запрос не поступил, значит мы ожидаем запрос.
            if "количество" in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                res['response']['text'] = "На официальном сайте есть вся информация!"
                res['response']['buttons'] = [
                    {
                        'title': 'Не переходить',
                        'hide': True
                    },
                    {
                        "title": "Перейти на официальный сайт",
                        "url": "https://koronavirustoday.ru/info/koronavirus-tablicza-po-stranam-mira-na-segodnya/",
                        "hide": True}
                ]
                if "переходить" in req['request']['nlu']['tokens']:
                    res['response']['text'] = "Что еще хочешь узнать?"
                    res['response']['buttons'] = [
                        {
                            'title': 'Информация про количество заболевших',
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
                            'title': 'Самоизоляция',
                            'hide': True
                        },
                        {
                            'title': 'Посмотреть карту заражения',
                            'hide': True
                        }
                    ]
            elif 'симптомы' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                symptomes(res, req)

            elif 'рекомендации' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                recomendation(res, req)

            elif 'самоизоляция' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                stay_home(res, req)
            elif 'карту' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                cards(res, req)
            else:
                res['response']['text'] = ('К сожалению у меня нет такого раздела. Выберите из перечисленных' +
                                           ' или перейдите на официальный сайт, где такая информация может быть.')
                res['response']['buttons'] = [
                    {
                        'title': 'Информация про количество заболевших',
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
                        'title': "Самоизоляция",
                        'hide': True
                    },
                    {
                        'title': 'Посмотреть карту заражения',
                        'hide': True
                    }
                ]
        else:
            if 'количество' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                res['response']['text'] = "На официальном сайте есть вся информация!"
                res['response']['buttons'] = [
                    {
                        'title': 'Не переходить',
                        'hide': True
                    },
                    {
                        "title": "Перейти на официальный сайт",
                        "url": "https://koronavirustoday.ru/info/koronavirus-tablicza-po-stranam-mira-na-segodnya/",
                        "hide": True}
                ]
                if "переходить" in req['request']['nlu']['tokens']:
                    res['response']['text'] = "Что еще хочешь узнать?"
                    res['response']['buttons'] = [
                        {
                            'title': 'Информация про количество заболевших',
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
                            'title': 'Самоизоляция',
                            'hide': True
                        },
                        {
                            'title': 'Посмотреть карту заражения',
                            'hide': True
                        }
                    ]
            elif 'симптомы' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                symptomes(res, req)
            elif 'рекомендации' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                recomendation(res, req)
            elif 'самоизоляция' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                stay_home(res, req)
            elif 'карту' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                cards(res, req)


def symptomes(res, req):
    user_id = req['session']['user_id']
    res['response']['text'] = "".join(['Основными признаками наличия коронавируса у человека являются:' +
                                       'слабость, усталость,',
                                       ' затрудненное дыхание,',
                                       ' высокая температура,',
                                       ' кашель (сухой или с небольшим количеством мокроты) и/или боль в горле,',
                                       'По симптоматике коронавирус схож с простудой' +
                                       ' и респираторными заболеваниями.',
                                       'Особое внимание стоит обратить на одышку:' +
                                       ' при ее наличии немедленно обратитесь к врачу.'])
    sessionStorage[user_id]['information'] = False
    res['response']['buttons'] = [
        {
            'title': 'Информация про количество заболевших',
            'hide': True
        },
        {
            'title': 'Рекомендации',
            'hide': True
        },
        {
            'title': 'Самоизоляция',
            'hide': True
        },
        {
            'title': 'Посмотреть карту заражения',
            'hide': True
        }
    ]


def recomendation(res, req):
    user_id = req['session']['user_id']
    res['response']['text'] = "\n".join(['Регулярно обрабатывайте руки спиртосодержащим средством' +
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
    sessionStorage[user_id]['information'] = False
    res['response']['buttons'] = [
        {
            'title': 'Информация про количество заболевших',
            'hide': True
        },
        {
            'title': 'Симптомы',
            'hide': True
        },
        {
            'title': 'Самоизоляция',
            'hide': True
        },
        {
            'title': 'Посмотреть карту заражения',
            'hide': True
        }
    ]


def stay_home(res, req):
    user_id = req['session']['user_id']
    res['response']['text'] = "\n".join(['Все по-разному проводят время на карантине, но есть несколько полезных' +
                                             ' советов, как получить от самоизляции удовольствие и пользу.',
                                             '1)Первым делом, не стоит забывать про учебу или работу. Во время' +
                                             ' карантина мы советуем регулярно укреплять или усовершенствовать свои' +
                                             ' навыки или знания. Многие обучающие площадки устраивают бесплатные' +
                                             ' тренинги и курсы. почему бы не воспользоваться этим?',
                                             "2)Займитесь своим любимым хобби! Ничто не поможет" +
                                             " провести карантин лучше, чем приятное сердцу дело!",
                                             "3) Займитесь спортом и своим здоровьем. Отличный шанс улучшить свое" +
                                             " физическое состояние и не испортить фигуру за время карантина!",
                                             "4)Помогите окружающим! Многие в сложившейся ситуации нуждаются в помощи" +
                                             " и поддержке, если у вас есть возможность, совершите доброе дело!"])
    sessionStorage[user_id]['information'] = False
    res['response']['buttons'] = [
        {
            'title': 'Информация про количество заболевших',
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
            'title': 'Посмотреть карту заражения',
            'hide': True
        }
    ]


def cards(res, req):
    user_id = req['session']['user_id']
    res['response']['card'] = {}
    res['response']['card']['type'] = 'BigImage'
    res['response']['card']['title'] = 'Карта коронавируса в мире'
    res['response']['card']['image_id'] = card["карта"]
    res['response']['text'] = 'Изучай!'
    sessionStorage[user_id]['information'] = False
    res['response']['buttons'] = [
        {
            'title': 'Информация про количество заболевших',
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
            'title': 'Самоизоляция',
            'hide': True
        }
    ]


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
