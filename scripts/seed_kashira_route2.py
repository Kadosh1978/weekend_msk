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


# Получаем уже существующее направление (Кашира должна быть создана ранее)
try:
    destination = Destination.objects.get(slug="kashira")
except Destination.DoesNotExist:
    print("ERROR: Направление Кашира не найдено. Сначала выполните seed-скрипт для Каширы.")
    exit()


# =================== МАРШРУТ 2 ===================
route, route_created = Route.objects.update_or_create(
    slug="kashira-na-2-dnya",
    defaults={
        "destination": destination,
        "title": "Кашира на 2 дня: неспешное знакомство",
        "short_description": (
            "Двухдневный маршрут для тех, кто хочет глубже узнать Каширу: "
            "усадьба Тарасково, старинные храмы, прогулки по набережной и вечерний город без спешки."
        ),
        "estimated_time": "2 дня",
        "route_includes": (
            "Введенская церковь и Хлебная площадь\n"
            "Никитский монастырь и смотровая площадка\n"
            "Успенский собор и прогулка по центру\n"
            "Усадьба Тарасково (загородная часть)\n"
            "Обед в местном кафе с рязанской кухней\n"
            "Вечерняя набережная Оки\n"
            "Ночёвка в гостинице или гостевом доме\n"
            "На второй день — Каширский краеведческий музей и сувениры\n"
            "Прогулка по старым улочкам и возвращение в Москву"
        ),
        "suitable_for": (
            "Для тех, кто хочет спокойный уикенд без спешки\n"
            "Для пар и семей с детьми\n"
            "Для любителей истории и усадебной архитектуры\n"
            "Для тех, кто хочет переночевать в старинном городе\n"
            "Для фотографов и любителей красивых закатов на Оке"
        ),
        "route_image_1_caption": (
            "<strong>Усадьба Тарасково</strong><br>Один из немногих сохранившихся усадебных комплексов под Каширой."
        ),
        "route_image_2_caption": (
            "<strong>Вечерняя набережная</strong><br>Тихий закат над Окой — ради этого стоит остаться на ночь."
        ),
        "route_image_3_caption": (
            "<strong>Каширский музей</strong><br>Экспозиция рассказывает о купеческом прошлом и знаменитых жителях города."
        ),
        "content": (
            "День 1.\n"
            "Приезжайте в Каширу утренней электричкой с Павелецкого вокзала. "
            "Поселитесь в гостинице или гостевом доме (лучше бронировать заранее). "
            "Начните с центра — Хлебной площади и Введенской церкви.\n\n"
            "После обеда отправляйтесь к Никитскому монастырю, откуда открывается лучшая панорама города. "
            "Если есть желание и позволяет транспорт, съездите в усадьбу Тарасково (10–15 минут на такси) — "
            "там сохранился усадебный дом и парк с прудами.\n\n"
            "Вечером обязательно прогуляйтесь по набережной Оки. Закаты здесь тихие и очень живописные. "
            "Поужинайте в одном из кафе в центре — вечерняя Кашира очаровательна своей тишиной.\n\n"
            "День 2.\n"
            "Посвятите вторую половину дня Каширскому краеведческому музею. Он расположен в здании бывшего "
            "городского училища и хранит интересные экспонаты о купеческом прошлом, природе и знаменитых людях "
            "(например, здесь бывал Чехов).\n\n"
            "Пройдитесь по старым улочкам, загляните в сувенирные лавки, купите местный каширский хлеб или мёд. "
            "Ближе к вечеру возвращайтесь к станции и уезжайте в Москву.\n\n"
            "Совет.\n"
            "Этот маршрут особенно хорош в тёплое время года, когда можно долго гулять у воды. "
            "Зимой тоже приятно, если хочется тишины и заснеженных храмов."
        ),
        "is_published": True,
    },
)

# =================== ЗАГРУЗКА ФОТО ДЛЯ МАРШРУТА 2 ===================
# Важно: названия файлов могут отличаться, проверьте на Commons или замените на свои.
save_image_if_empty(
    route,
    "route_image_1",
    "Kashira Uspenskaya 44.JPG",
    "kashira_route2_1.jpg",
)

save_image_if_empty(
    route,
    "route_image_2",
    "Kashira-vid.jpg",
    "kashira_route2_2.jpg",
)

save_image_if_empty(
    route,
    "route_image_3",
    "Kashira museum 02 1.jpg",
    "kashira_route2_3.jpg",
)

print("OK: маршрут «Кашира на 2 дня» добавлен или обновлён.")
print(f"Route created: {route_created}")