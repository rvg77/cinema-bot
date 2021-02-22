import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import credentials
import phrasebook
import kinopoisk
import keyboards
import logging
import typing as tp

# Configure logging
logging.basicConfig(level=logging.INFO)
# Extracting proxy info
login, password = credentials.PROXY_CREDS.split(':')
proxy_auth = aiohttp.BasicAuth(login=login, password=password)
# Creating bot
bot = Bot(
    token=credentials.API_TOKEN,
    # proxy=credentials.PROXY,
    # proxy_auth=proxy_auth
)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)


class FindFilm(StatesGroup):
    waiting_for_particular_film = State()


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, phrasebook.WELCOME)


@dp.message_handler(commands=['help'], state='*')
async def send_help(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, phrasebook.HELP)


@dp.callback_query_handler(state=FindFilm.waiting_for_particular_film)
async def film_choice_callback_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    code = callback_query.data.split()[-1]

    if code == 'cancel':
        await state.finish()
        await bot.send_message(callback_query.from_user.id, phrasebook.CANCEL)
    else:
        try:
            film_id = int(code)
        except ValueError:
            assert False, "invalid film id"

        data = await state.get_data()
        film_json = data['films'][film_id]

        await bot.send_photo(callback_query.from_user.id, film_json['posterUrl'])
        await bot.send_message(callback_query.from_user.id, phrasebook.construct_description(film_json))
        kb = keyboards.source_choice(film_json['nameRu'])
        await bot.send_message(callback_query.from_user.id, phrasebook.SOURCES, reply_markup=kb)
        await FindFilm.next()

    await callback_query.answer()


@dp.message_handler(state='*')
async def find_films_by_name(message: types.Message, state: FSMContext) -> None:
    film: str = message.text
    response_json: tp.Dict[str, tp.Any] = await kinopoisk.film2info(film)

    if response_json['pagesCount'] == 0:
        await bot.send_message(message.from_user.id, phrasebook.NOT_FOUND)
        return

    kb, films = keyboards.film_choice(response_json)
    await FindFilm.waiting_for_particular_film.set()
    await state.update_data(films=films)
    await bot.send_message(message.from_user.id, phrasebook.FOUND, reply_markup=kb)


if __name__ == '__main__':
    executor.start_polling(dp)
