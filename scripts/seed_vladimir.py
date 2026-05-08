from urllib.parse import quote
from urllib.request import Request, urlopen
import time

from django.core.files.base import ContentFile

from destinations.models import Destination
from routes.models import Route


COMMONS_FILE_URL = "https://commons.wikimedia.org/wiki/Special:Redirect/file/"


def download_commons_file(filename):
    url = COMMONS_FILE_URL + quote(filename)
    request = Request(
        url,
        headers={
            "User-Agent": "weekend-msk-content-seed/1.0"
        },
    )
    with urlopen(request, timeout=40) as response:
        return response.read()


def save_image_if_empty(obj, field_name, commons_filename, local_filename):
    field = getattr(obj, field_name)

    if field:
        print(f"SKIP: {field_name} уже заполнено: {field.name}")
        return

    try:
        image_data = download_commons_file(commons_filename)
    except Exception as error:
        print(f"WARNING: не удалось скачать фото {commons_filename}: {error}")
        return

    field.save(local_filename, ContentFile(image_data), save=True)
    print(f"OK: добавлено фото {field_name}: {local_filename}")
    time.sleep(3)


# =================== НАПРАВЛЕНИЕ ===================
destination, created = Destination.objects.update_or_create(
    slug="vladimir",
    defaults={
        "name": "Владимир",
        "short_description": (
            "Владимир — один из самых красивых городов Золотого кольца: "
            "древние соборы, панорамы Клязьмы и идеальный маршрут на выходные."
        ),
        "description": (
            "Владимир — классическое направление для поездки на выходные из Москвы. "
            "Город известен своими белокаменными соборами, старинными улицами и "
            "атмосферой древней Руси.\n\n"
            "Здесь удобно гулять пешком: основные достопримечательности находятся "
            "рядом друг с другом, а сам центр отлично подходит для спокойного "
            "маршрута без спешки.\n\n"
            "Во Владимир едут ради архитектуры, красивых видов на Клязьму, "
            "истории Золотого кольца и уютных прогулок по старому городу."
        ),
        "how_to_get": (
            "Из Москвы удобнее всего ехать на «Ласточке» с Курского вокзала — "
            "дорога занимает около 2 часов.\n\n"
            "Также можно добраться на автомобиле по трассе М7. "
            "Внутри города основные точки удобно обходить пешком."
        ),
        "what_to_see": (
            "Главные достопримечательности — Успенский собор, Дмитриевский собор "
            "и Золотые ворота.\n\n"
            "Также стоит пройтись по Большой Московской улице, выйти к смотровым "
            "площадкам над Клязьмой и посетить местные музеи.\n\n"
            "Если останется время, можно съездить в Суздаль — он находится совсем рядом."
        ),
        "budget": (
            "Поездка во Владимир остаётся относительно бюджетной: основные расходы — "
            "дорога, питание, музеи и при необходимости гостиница."
        ),
        "days_count": "1–2 дня",
        "transport_type": "train",
        "is_published": True,

        "hero_image_caption": (
            "<strong>Владимир</strong><br>Один из главных городов Золотого кольца России."
        ),
        "gallery_image_1_caption": (
            "<strong>Успенский собор</strong><br>Белокаменный символ Владимира и объект ЮНЕСКО."
        ),
        "gallery_image_2_caption": (
            "<strong>Дмитриевский собор</strong><br>Знаменит своей древней каменной резьбой."
        ),
        "gallery_image_3_caption": (
            "<strong>Панорамы Клязьмы</strong><br>Лучшие виды открываются со смотровых площадок."
        ),
    },
)


# =================== ФОТО НАПРАВЛЕНИЯ ===================
save_image_if_empty(
    destination,
    "hero_image",
    "Виды на нижнюю часть города - panoramio.jpg",
    "vladimir_hero.jpg",
)

save_image_if_empty(
    destination,
    "gallery_image_1",
    "Dormition of the Theotokos Cathedral Vladimir 2016-06-23 6389.jpg",
    "vladimir_gallery_1.jpg",
)

save_image_if_empty(
    destination,
    "gallery_image_2",
    "Dmitrievsky Cathedral. Vladimir city. (3820966540).jpg",
    "vladimir_gallery_2.jpg",
)

save_image_if_empty(
    destination,
    "gallery_image_3",
    "Vladimir Road bridge over Klyazma IMG 9864 1725.jpg",
    "vladimir_gallery_3.jpg",
)


# =================== МАРШРУТ ===================
route, route_created = Route.objects.update_or_create(
    slug="vladimir-na-1-den",
    defaults={
        "destination": destination,
        "title": "Владимир за 1 день",
        "short_description": (
            "Маршрут по главным достопримечательностям Владимира: "
            "соборы, старый центр и лучшие виды на Клязьму."
        ),
        "estimated_time": "1 день",
        "route_includes": (
            "Золотые ворота\n"
            "Успенский собор\n"
            "Дмитриевский собор\n"
            "Большая Московская улица\n"
            "Смотровые площадки\n"
            "Обед в центре города\n"
            "Прогулка по историческому центру"
        ),
        "suitable_for": (
            "Для первого знакомства с Золотым кольцом\n"
            "Для спокойной поездки на выходные\n"
            "Для любителей древнерусской архитектуры\n"
            "Для самостоятельного путешествия"
        ),
        "route_image_1_caption": (
            "<strong>Успенский собор</strong><br>Главная архитектурная доминанта Владимира."
        ),
        "route_image_2_caption": (
            "<strong>Золотые ворота</strong><br>Один из символов древнего города."
        ),
        "route_image_3_caption": (
            "<strong>Виды на Клязьму</strong><br>Финальная точка прогулки с лучшими панорамами."
        ),
        "content": (
            "Утро.\n"
            "Лучше приехать во Владимир утром на «Ласточке», чтобы спокойно "
            "провести в городе весь день. Начните прогулку с Золотых ворот — "
            "это исторический символ Владимира и удобная стартовая точка маршрута.\n\n"

            "Первая половина дня.\n"
            "Двигайтесь по Большой Московской улице в сторону Успенского собора. "
            "По пути стоит обратить внимание на старинные здания, смотровые площадки "
            "и атмосферу центра. После Успенского собора обязательно осмотрите "
            "Дмитриевский собор — один из самых красивых памятников белокаменной архитектуры.\n\n"

            "Обед.\n"
            "Сделайте паузу в одном из ресторанов или кафе в центре города. "
            "Во Владимире много мест с русской кухней и уютными интерьерами.\n\n"

            "Вторая половина дня.\n"
            "После обеда прогуляйтесь к смотровым площадкам над Клязьмой. "
            "Это одна из самых приятных частей маршрута: отсюда открываются "
            "широкие панорамы на реку и окрестности.\n\n"

            "Вечер.\n"
            "Неспешно завершите прогулку по историческому центру, купите сувениры "
            "или местные сладости и отправляйтесь обратно в Москву."
        ),
        "is_published": True,
    },
)


# =================== ФОТО МАРШРУТА ===================
save_image_if_empty(
    route,
    "route_image_1",
    "Dormition of the Theotokos Cathedral Vladimir 2016-06-23 6310.jpg",
    "vladimir_route_1.jpg",
)

save_image_if_empty(
    route,
    "route_image_2",
    "Golden Gate Vladimir 2016-06-23 6326.jpg",
    "vladimir_route_2.jpg",
)

save_image_if_empty(
    route,
    "route_image_3",
    "Bridge over the Klyazma river - Vladimir, Russia - panoramio.jpg",
    "vladimir_route_3.jpg",
)


print("OK: Владимир добавлен или обновлён.")
print("OK: маршрут «Владимир за 1 день» добавлен или обновлён.")
print(f"Destination created: {created}")
print(f"Route created: {route_created}")