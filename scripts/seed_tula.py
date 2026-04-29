from urllib.parse import quote
from urllib.request import Request, urlopen

from django.core.files.base import ContentFile

from destinations.models import Destination
from routes.models import Route


COMMONS_FILE_URL = "https://commons.wikimedia.org/wiki/Special:Redirect/file/"


def download_commons_file(filename):
    url = COMMONS_FILE_URL + quote(filename)

    request = Request(
        url,
        headers={"User-Agent": "weekend-msk-content-seed/1.0"},
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


destination, created = Destination.objects.update_or_create(
    slug="tula",
    defaults={
        "name": "Тула",
        "short_description": (
            "Тула — удобное направление на выходные из Москвы: кремль, музеи, "
            "исторический центр, гастрономия и насыщенный маршрут на один день."
        ),
        "description": (
            "Тула — один из самых интересных городов для однодневной поездки из Москвы. "
            "Сюда едут за хорошо сохранившимся историческим центром, Тульским кремлём, "
            "музеями оружия и пряника, а также за атмосферой старого русского города.\n\n"
            "Город отлично подходит для маршрута на один день: основные достопримечательности "
            "расположены компактно, между ними удобно перемещаться пешком, а программа получается "
            "насыщенной, но не перегруженной.\n\n"
            "Тула сочетает историю, гастрономию и современную городскую среду, поэтому поездка "
            "получается разнообразной и интересной в любое время года."
        ),
        "how_to_get": (
            "Самый удобный способ добраться до Тулы — скоростной поезд или электричка с Курского вокзала. "
            "Дорога занимает около двух часов.\n\n"
            "На машине поездка тоже удобна, но в выходные возможны пробки на выезде из Москвы. "
            "Для однодневного маршрута поезд обычно оказывается самым комфортным вариантом."
        ),
        "what_to_see": (
            "Главная точка маршрута — Тульский кремль. Здесь стоит начать прогулку, осмотреть стены, "
            "соборы и центральную площадь.\n\n"
            "После кремля можно посетить Музей оружия или Музей пряника, а затем прогуляться по "
            "пешеходным улицам исторического центра.\n\n"
            "Маршрут хорошо дополняют кафе, локальные гастрономические точки и прогулка по набережной Упы."
        ),
        "budget": (
            "Бюджет на 1 день: дорога, обед, музеи и небольшие покупки. "
            "Поездка остаётся комфортной и доступной."
        ),
        "days_count": "1 день",
        "transport_type": "train",
        "is_published": True,
    },
)

route, route_created = Route.objects.update_or_create(
    slug="tula-na-1-den",
    defaults={
        "destination": destination,
        "title": "Тула на 1 день",
        "short_description": (
            "Готовый маршрут на один день: кремль, музеи, исторический центр и тульская гастрономия."
        ),
        "estimated_time": "1 день",
        "route_includes": (
            "Тульский кремль\n"
            "Казанская набережная\n"
            "Музей оружия или Музей пряника\n"
            "Прогулка по историческому центру\n"
            "Обед в центре города\n"
            "Покупка тульских пряников\n"
            "Возвращение в Москву вечером"
        ),
        "suitable_for": (
            "Для поездки на один день из Москвы\n"
            "Для маршрута без машины\n"
            "Для любителей истории и музеев\n"
            "Для гастрономического путешествия\n"
            "Для спокойного выходного дня"
        ),
        "route_image_1_caption": (
            "Тульский кремль — историческое сердце города и начало маршрута."
        ),
        "route_image_2_caption": (
            "Музей оружия — одна из главных современных достопримечательностей Тулы."
        ),
        "route_image_3_caption": (
            "Казанская набережная — отличное место для прогулки во второй половине дня."
        ),
        "content": (
            "Утро.\n"
            "Лучше выехать из Москвы утром, чтобы приехать в Тулу к началу дня. После прибытия удобно сразу "
            "направиться к Тульскому кремлю — это логичная отправная точка маршрута.\n\n"
            "Первая половина дня.\n"
            "Осмотрите территорию кремля, его стены, соборы и центральную площадь. Затем можно прогуляться "
            "по прилегающим улицам исторического центра.\n\n"
            "Обед.\n"
            "Лучше сделать остановку в одном из кафе или ресторанов в центре города. Это хороший момент, "
            "чтобы отдохнуть перед второй частью маршрута.\n\n"
            "Вторая половина дня.\n"
            "После обеда стоит выбрать один из музеев: Музей оружия или Музей пряника. Затем можно выйти "
            "на Казанскую набережную и завершить прогулку у реки.\n\n"
            "Вечер.\n"
            "Перед отъездом можно купить тульские пряники или сувениры, после чего спокойно возвращаться "
            "на вокзал и ехать обратно в Москву."
        ),
        "is_published": True,
    },
)

save_image_if_empty(
    route,
    "route_image_1",
    "Tula Kremlin aerial view.jpg",
    "tula_route_1.jpg",
)

save_image_if_empty(
    route,
    "route_image_2",
    "Muzey oruzhiya Tula.jpg",
    "tula_route_2.jpg",
)

save_image_if_empty(
    route,
    "route_image_3",
    "Kazan Embankment Tula.jpg",
    "tula_route_3.jpg",
)

print("OK: Тула добавлена или обновлена.")
print("OK: маршрут «Тула на 1 день» добавлен или обновлён.")
print(f"Destination created: {created}")
print(f"Route created: {route_created}")
