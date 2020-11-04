import typing as tp

WELCOME = "Просто напиши мне название фильма на русском или английском языке"
HELP = "Ты — пишешь название фильма, остальное я беру на себя!"
FOUND = "Смотри, что нашел:"
NOT_FOUND = "Давай что-нибудь попроще😉"
CANCEL = "Окей, подыщем что-нибудь другое"
SOURCES = """Доступно несколько вариантов просмотра:

💰 Платно или по подписке
🆓 Бесплатно, но может понадобится VPN или прокси"""


def construct_description(film_json: tp.Dict[str, tp.Any]) -> str:
    name_ru = film_json['nameRu']
    name_en = film_json['nameEn']
    description = film_json['description']
    year = film_json['year']
    countries = ', '.join([c['country'] for c in film_json['countries']])
    length = film_json['filmLength']
    genres = ', '.join([g['genre'] for g in film_json['genres']])
    rating = film_json['rating']

    return f"""{name_ru}, {name_en}

📅 {year}
📈 {rating}
⌛ {length}
🎬 {description}
🗺 {countries}
ℹ️ {genres}"""
