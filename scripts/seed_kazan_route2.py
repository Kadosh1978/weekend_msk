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


# Получаем уже существующее направление (Казань должна быть создана ранее)
try:
    destination = Destination.objects.get(slug="kazan")
except Destination.DoesNotExist:
    print("ERROR: Направление Казань не найдено. Сначала выполните seed-скрипт для Казани.")
    exit()


# =================== МАРШРУТ 2 ===================
route, route_created = Route.objects.update_or_create(
    slug="kazan-za-1-den",
    defaults={
        "destination": destination,
        "title": "Казань за 1 день: максимальная программа",
        "short_description": (
            "Интенсивный маршрут для тех, кто хочет увидеть главное за один день: "
            "кремль, улица Баумана, татарская кухня, набережная и современные символы города."
        ),
        "estimated_time": "1 день",
        "route_includes": (
            "Казанский кремль (мечеть Кул-Шариф, Благовещенский собор)\n"
            "Панорама с Кремлёвской набережной\n"
            "Обед с национальной кухней на улице Баумана\n"
            "Старо-Татарская слобода\n"
            "Центр семьи «Казан» и Дворец земледельцев\n"
            "Вечерняя прогулка по набережной Казанки\n"
            "Ужин в одном из ресторанов с видом на город"
        ),
        "suitable_for": (
            "Тем, кто ограничен одним днём\n"
            "Для первого знакомства с Казанью\n"
            "Для энергичных путешественников\n"
            "Для самостоятельной поездки\n"
            "Для всех, кто хочет попробовать татарскую кухню"
        ),
        "route_image_1_caption": (
            "<strong>Мечеть Кул-Шариф</strong><br>Главный символ Казанского кремля и обязательное место для фотографии."
        ),
        "route_image_2_caption": (
            "<strong>Улица Баумана</strong><br>Пешеходный центр с кафе, сувенирами и атмосферой большого города."
        ),
        "route_image_3_caption": (
            "<strong>Центр семьи «Казан»</strong><br>Знаменитая смотровая площадка с футуристической архитектурой."
        ),
        "content": (
            "Утро.\n"
            "Прилетайте или приезжайте в Казань как можно раньше. Сразу направляйтесь "
            "в Казанский кремль — на его осмотр заложите не менее двух часов. Обойдите "
            "стены, посетите мечеть Кул-Шариф (внутри очень красиво), зайдите в "
            "Благовещенский собор и выйдите на смотровую площадку у набережной.\n\n"
            "Обед.\n"
            "К обеду вы окажетесь на улице Баумана. Здесь огромный выбор кафе и ресторанов: "
            "попробуйте эчпочмак, кыстыбый, манты и обязательно десерт — чак-чак. "
            "Отличное место, чтобы передохнуть перед второй половиной дня.\n\n"
            "Вторая половина дня.\n"
            "После обеда прогуляйтесь по Старо-Татарской слободе — это тихий район "
            "с деревянными домами, мечетями и особым колоритом. Затем возвращайтесь "
            "в сторону кремля и идите по Кремлёвской набережной до Центра семьи "
            "«Казан» (Чаша). Поднимитесь на смотровую площадку, откуда весь город "
            "как на ладони. Рядом — Дворец земледельцев, тоже очень эффектное здание.\n\n"
            "Вечер.\n"
            "Закончите день ужином в одном из ресторанов с видом на Казанку или "
            "в районе набережной. Если останутся силы, прогуляйтесь по вечерней "
            "набережной — она красиво подсвечена. После этого вам останется только "
            "добраться до аэропорта или вокзала.\n\n"
            "Совет.\n"
            "Этот маршрут очень насыщенный, но выполнимый. Одевайте удобную обувь "
            "и начинайте день пораньше. Если захотите остаться на второй день, "
            "у вас уже есть готовый двухдневный маршрут по Казани."
        ),
        "is_published": True,
    },
)

# =================== ЗАГРУЗКА ФОТО ДЛЯ МАРШРУТА 2 ===================
# Имена файлов взяты с Wikimedia Commons, актуальны на момент составления.
save_image_if_empty(
    route,
    "route_image_1",
    "Qolşärif Mosque in Kazan, Russia.jpg",
    "kazan_route2_1.jpg",
)

save_image_if_empty(
    route,
    "route_image_2",
    "Казань, улица Баумана, 68.jpg",
    "kazan_route2_2.jpg",
)

save_image_if_empty(
    route,
    "route_image_3",
    "Kazan family center 11.jpg",
    "kazan_route2_3.jpg",
)

print("OK: маршрут «Казань за 1 день» добавлен или обновлён.")
print(f"Route created: {route_created}")