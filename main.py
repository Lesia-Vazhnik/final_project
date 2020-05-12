from flask import Flask, request
import logging
import json
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}
# подключаем картинки
card = {'карта': "1540737/3c5fad08bd419a235347"}


@app.route('/post', methods=['POST'])
# основная функция
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


# функция с условиями вызова других функций
def handle_dialog(res, req):
    # проверка первого вхождение пользователя
    user_id = req['session']['user_id']
    if req['session']['new']:
        # узнаем имя нового пользователя
        res['response']['text'] = 'Привет! Как тебя зовут?'
        sessionStorage[user_id] = {
            'first_name': None,
            # здесь будет храниться имя
            'information': False
            # здесь информация о том, что пользователь запросил информацию. По умолчанию False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        # проферка на правильность ввода имени
        # и если нет то переспрашиваем
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = f'Приятно познакомиться, {first_name.title()}. Я Алиса. Что ты хочешь узнать?'
            # создание кнопок на экране
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
                    'title': 'Распространение',
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
    # если пользователь уже известен
    # то переходим к запросам
    else:
        if not sessionStorage[user_id]['information']:
            # запрос не поступил, значит мы ожидаем запрос.
            if "количество" in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                res['response']['text'] = "На официальном сайте есть вся информация!"
                # даем пользователю выбор для действия
                res['response']['buttons'] = [
                    {
                        'title': 'Не переходить',
                        'hide': True
                    },
                    {
                        # переход на сайт
                        "title": "Перейти на официальный сайт",
                        "url": "https://koronavirustoday.ru/info/koronavirus-tablicza-po-stranam-mira-na-segodnya/",
                        "hide": True}
                ]
                # предложение узнать еще что-то, после возвращения к диалогу с сайта
                if "переходить" in req['request']['nlu']['tokens']:
                    res['response']['text'] = "Что еще хочешь узнать?"
                    # создание кнопок на экране
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
                            'title': 'Распространение',
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
            # вызов нужной пользователю функции
            elif 'симптомы' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                symptomes(res, req)
                # переход к функции

            elif 'рекомендации' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                recomendation(res, req)
                # переход к функции

            elif 'самоизоляция' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                stay_home(res, req)
                # переход к функции
            elif 'карту' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                cards(res, req)
                # переход к функции
            elif 'распространение' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                raspr(res, req)
                # переход к функции

            # если нужной функции не нашлось,сообщаем об ошибке
            else:
                res['response']['text'] = ('К сожалению у меня нет такого раздела. Выберите из перечисленных' +
                                           ' или перейдите на официальный сайт, где такая информация может быть.')
                # создание кнопок на экране
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
                        'title': 'Распространение',
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
                # предложение перейти по ссылке с информацией
                # предоставляем пользователю выбор дальнейших действий
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
                    # создание кнопок на экране
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
                            'title': 'Распространение',
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
            # вызов нужной пользователю функции
            elif 'симптомы' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                symptomes(res, req)
                # переход к функции
            elif 'рекомендации' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                recomendation(res, req)
                # переход к функции
            elif 'самоизоляция' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                stay_home(res, req)
                # переход к функции
            elif 'карту' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                cards(res, req)
            elif 'распространение' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['information'] = True
                raspr(res, req)
                # переход к функции


# ункция, отвечающая за вывод информации о симптомах заболевания
def symptomes(res, req):
    user_id = req['session']['user_id']
    # вывод информации по запросу пользователя
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
    # создание кнопок на экране
    res['response']['buttons'] = [
        {
            'title': 'Информация про количество заболевших',
            'hide': True
        },
        {
            'title': 'Распространение',
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


# функция, отвечающая за вывод информации о рекомендациях врачей
def recomendation(res, req):
    user_id = req['session']['user_id']
    # вывод информации
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
    # создание кнопок на экране
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
            'title': 'Распространение',
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


# функция, отвечающая за вывод информации о досуге на самоизоляции
def stay_home(res, req):
    user_id = req['session']['user_id']
    # вывод информации по запросу пользователя
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
    # создание кнопок на экране
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
            'title': 'Распространение',
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


# функция, отвечающая за вывод карты заражения
def cards(res, req):
    # вывод картинки по запросу
    user_id = req['session']['user_id']
    res['response']['card'] = {}
    res['response']['card']['type'] = 'BigImage'
    # вывод текста и карты
    res['response']['card']['title'] = 'Карта коронавируса в мире'
    res['response']['card']['image_id'] = card["карта"]
    res['response']['text'] = 'Изучай!'
    sessionStorage[user_id]['information'] = False
    # создание кнопок на экране
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
            'title': 'Распространение',
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


# функция, отвечающая за вывод информации о распространении заболевания
def raspr(res, req):
    user_id = req['session']['user_id']
    # вывод информации по запросу пользователя
    res['response']['text'] = "\n".join(['Короновирус может передаваться:',
                                         'воздушно-капельным путем (при кашле или чихании)',
                                         'контактным путем (поручни в транспорте,' +
                                         ' дверные ручки и другие загрязненные поверхности и предметы)',
                                         'Как и другие респираторные вирусы, коронавирус распространяется' +
                                         ' через капли, которые образуются, когда инфицированный человек' +
                                         ' кашляет или чихает.', 'Кроме того, он может распространяться,' +
                                         ' когда инфицированный человек касается любой загрязненной поверхности,' +
                                         ' например, дверной ручки.',
                                         'Люди заражаются, когда они касаются загрязненными руками рта, носа или глаз.'])
    sessionStorage[user_id]['information'] = False
    # создание кнопок на экране
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


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name', то возвращаем её значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


# запуск
if __name__ == '__main__':
    app.run()
