# Получаем уже существующее направление (Рязань должна быть создана ранее)
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
    time.sleep(3)   # пауза, чтобы не получить HTTP 429


# Получаем уже существующее направление (Рязань должна быть создана ранее)
try:
    destination = Destination.objects.get(slug="ryazan")
except Destination.DoesNotExist:
    print("ERROR: Направление Рязань не найдено. Сначала выполните seed-скрипт для Рязани.")
    exit()


# =================== МАРШРУТ 2 ===================
route, route_created = Route.objects.update_or_create(
    slug="ryazan-na-2-dnya",
    defaults={
        "destination": destination,
        "title": "Рязань на 2 дня: погружение в историю",
        "short_description": (
            "Двухдневный маршрут для тех, кто хочет увидеть не только кремль, но и "
            "окрестности: Константиново, музей леденца, прогулки по вечернему городу и местная кухня."
        ),
        "estimated_time": "2 дня",
        "route_includes": (
            "Рязанский кремль (Успенский собор, обзорная площадка)\n"
            "Пешеходная улица Почтовая и памятник Евпатию Коловрату\n"
            "Музей истории рязанского леденца\n"
            "Обед с блюдами рязанской кухни\n"
            "Поездка в село Константиново (родина Сергея Есенина)\n"
            "Прогулка по набережной Оки на закате\n"
            "Ночёвка в гостинице в центре\n"
            "На второй день — Рязанский художественный музей или прогулка по городу\n"
            "Сувениры и возвращение в Москву"
        ),
        "suitable_for": (
            "Для тех, кто хочет провести выходные с пользой\n"
            "Для любителей литературы и русской деревни\n"
            "Для семей с детьми\n"
            "Для спокойного и размеренного отдыха\n"
            "Для тех, кто хочет попробовать местную гастрономию"
        ),
        "route_image_1_caption": (
            "<strong>Село Константиново</strong><br>Дом-музей Сергея Есенина с видом на Оку — трогательное место силы."
        ),
        "route_image_2_caption": (
            "<strong>Музей рязанского леденца</strong><br>Интерактивный музей с историей и дегустацией сахарной сладости."
        ),
        "route_image_3_caption": (
            "<strong>Вечерняя Рязань</strong><br>Набережная и старый город, подсвеченные огнями, — идеальное завершение дня."
        ),
        "content": (
            "День 1.\n"
            "Приезжайте в Рязань утром на «Ласточке» или автомобиле. Оставьте вещи в гостинице "
            "и сразу отправляйтесь в кремль. Проведите там около двух часов, поднимитесь на "
            "колокольню (если работает), полюбуйтесь панорамой.\n\n"
            "После кремля прогуляйтесь по Почтовой улице к памятнику Евпатию Коловрату. "
            "К обеду выберите кафе с местной кухней — обязательно попробуйте рязанский калач "
            "и рыбные блюда из Оки.\n\n"
            "После обеда посетите Музей истории рязанского леденца (записываться заранее!). "
            "Это очень душевное место, где вы узнаете о традициях и сможете купить сладкие "
            "сувениры.\n\n"
            "Вечером прогуляйтесь по набережной Оки. Закаты здесь потрясающие. В тёплое время "
            "года можно даже спуститься к воде. Ужин — в одном из ресторанов с видом на реку.\n\n"
            "День 2.\n"
            "Утром отправляйтесь в Константиново (40 минут на такси или автобусе). "
            "Там находится дом-музей Сергея Есенина, от которого открывается захватывающий "
            "вид на заливные луга и Оку. Место очень поэтичное и умиротворяющее. "
            "Вернувшись в Рязань, можно посетить Рязанский художественный музей или "
            "просто прогуляться по центру. К вечеру возвращайтесь в Москву.\n\n"
            "Совет.\n"
            "Лучшее время для поездки — май-сентябрь, когда цветут сады и открываются "
            "великолепные виды. Бронируйте жильё заранее, особенно в выходные."
        ),
        "is_published": True,
    },
)

# =================== ЗАГРУЗКА ФОТО ДЛЯ МАРШРУТА 2 ===================
# Внимание: названия файлов могут отличаться, проверьте на Commons или замените.
save_image_if_empty(
    route,
    "route_image_1",
    "Дом, где родился С.А. Есенин. Константиново..JPG",   # Константиново
    "ryazan_route2_1.jpg",
)


save_image_if_empty(
    route,
    "route_image_2",
    "Музей Истории Рязанского Леденца вывеска.jpg",               # музей леденца
    "ryazan_route2_2.jpg",
)

save_image_if_empty(
    route,
    "route_image_3",
    "Trubezh Embankment 1.jpg",               # вечерняя набережная
    "ryazan_route2_3.jpg",
)

print("OK: маршрут «Рязань на 2 дня» добавлен или обновлён.")
print(f"Route created: {route_created}")