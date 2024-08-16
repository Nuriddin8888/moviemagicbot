from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import random

from buttons.inline import *
from database import *
from state import AddedMovie


logging.basicConfig(level=logging.INFO)

API_TOKEN = '7219600368:AAFXrydsxc_29P9C35OVNLovAjr0seDi2sI'
CHANNELS = ['@Mutalov_Nuriddin']

ADMINS_ID = [1921911753, 7149602547]

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


MOVIES = {}
MOVIEST = []

async def check_subscriptions(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ('member', 'administrator', 'creator'):
                return False
        except Exception as e:
            logging.error(f"Subscription status tekshirishda xato: {e}")
            return False
    return True


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    existing_full_name = get_user(full_name, user_id)

    if existing_full_name:
        if await check_subscriptions(user_id):
            await message.answer(f"Salom, Hurmatli <b>{full_name}</b>\nFilm kodini yuboring ✍️")
        else:
            await message.answer(f"Xurmatli <b>{full_name}</b>, kanallarga obuna bo'lmagan ko'rinasiz iltimos quyidagi kanallarga obuna bo'ling 👇", reply_markup=channels)
    else:
        add_user(full_name, username, user_id)
        await message.answer(f"Salom, Hurmatli <b>{full_name}</b>! Botimizga xush kelibsiz!\n\n<b>MovieMagic</b>🎥 boti orqali jahon filmlarni yuqori sifatda tomosha qilishingiz mumkin ✅\nIltimos botdan to'liq foydalanish uchun quyidagi kanallarga a'zo bo'ling 👇", reply_markup=channels)


@dp.callback_query_handler(text='check_subscribe')
async def process_callback_check_subscribe(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    full_name = callback_query.from_user.full_name

    if await check_subscriptions(user_id):
        update_subscription_status(user_id, 1)
        await callback_query.message.answer("Botimizdan bemalol foydalanishingiz mumkin! ✅\n\nFilm kodini yuboring 🎥", reply_markup=ReplyKeyboardRemove())
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=None)


    else:
        await callback_query.answer(f"Xurmatli {full_name}, kanallarga obuna bo'lmagansiz. Iltimos, obuna bo'ling", show_alert=True)
    await callback_query.answer()


@dp.message_handler(commands=['video'])
async def send_video(message: types.Message):
    full_name = message.from_user.full_name
    await message.answer(f"Salom <b>{full_name}</b> Video yuboring")
    await AddedMovie.send_video.set()


@dp.message_handler(content_types=types.ContentType.VIDEO, state=AddedMovie.send_video)
async def send_to_video(message: types.Message, state: FSMContext):
    file_id = message.video.file_id
    await message.answer_video(file_id)
    await state.finish()


@dp.message_handler(commands=['admin'])
async def send_admin_welcome(message: types.Message):
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    for admin_id in ADMINS_ID:
        if user_id == admin_id:
            await message.answer(f"Salom, Hurmatli <b>{full_name}</b>! Botimizga xush kelibsiz", reply_markup=admin_panel)
        else:
            pass


def get_users_page(page=1, page_size=4):
    offset = (page - 1) * page_size
    users = get_all_users()
    return users[offset:offset + page_size], len(users)

@dp.callback_query_handler(text='show_user')
async def view_users(callback_query: types.CallbackQuery):
    page = 1
    users_page, total_users = get_users_page(page)
    
    if users_page:
        await callback_query.answer()
        
        users_list = "\n".join([f"{i+1}. Ismi - {user[1]}\n{i+1}. User name - @{user[2]}\n{i+1}. Obuna - {user[3]}\n\n" for i, user in enumerate(users_page)])
        await send_user_list(callback_query.from_user.id, users_list, page, total_users)
    else:
        await bot.send_message(callback_query.from_user.id, "Hech qanday foydalanuvchi topilmadi.")


async def send_user_list(chat_id, users_list, page, total_users):
    keyboard = create_pagination_keyboard(page, total_users)
    await bot.send_message(chat_id, f"Foydalanuvchilar ro'yxati:\n\n{users_list}", reply_markup=keyboard)



@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('prev_page', 'next_page')))
async def pagination_callback(callback_query: types.CallbackQuery):
    current_page = int(callback_query.data.split(':')[1])
    if 'prev_page' in callback_query.data:
        page = current_page - 1
    else:
        page = current_page + 1
    
    users_page, total_users = get_users_page(page)
    
    if users_page:
        users_list = "\n".join([f"{i+1}. Ismi - {user[1]}\n{i+1}. User name - @{user[2]}\n{i+1}. Obuna - {user[3]}\n\n" for i, user in enumerate(users_page)])
        await bot.edit_message_text(f"Foydalanuvchilar ro'yxati:\n\n{users_list}",
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=create_pagination_keyboard(page, total_users))



@dp.callback_query_handler(text='add_movie')
async def add_movie(callback_query: types.CallbackQuery):
    for admin_id in ADMINS_ID:
        if callback_query.from_user.id == admin_id:
            await callback_query.answer()
            await callback_query.message.answer(f"Filmni qanday qo'shmoqchisiz", reply_markup=movie_insert_types)
        else:
            await callback_query.answer()
            pass



@dp.callback_query_handler(text='send_link')
async def add_movie_types(callback_query: types.CallbackQuery):
    await callback_query.answer("")
    await callback_query.message.answer("Film Havolasini yuboring")
    await AddedMovie.add_movie_link.set()



# def generate_unique_movie_code():
#     movie_code = str(random.randint(1, 300))
#     while movie_code in MOVIES:
#         movie_code = str(random.randint(1, 300))
#     return movie_code



async def generate_unique_movie_code():
    attempts = 0
    max_attempts = 300
    
    existing_codes = get_all_movie_codes()

    while attempts < max_attempts:
        movie_code = str(random.randint(1, 300))
        if movie_code not in existing_codes:
            return movie_code
        attempts += 1

    if attempts >= max_attempts:
        await bot.send_message(chat_id=ADMINS_ID, text="Yangi film kodi yaratib bo'lmadi. Iltimos, barcha kodlarni ko'rib chiqing yoki yangi oralik belgilang")
        return None


@dp.message_handler(content_types=types.ContentType.TEXT, state=AddedMovie.add_movie_link)
async def get_movie_link(message: types.Message):
    movie_link = message.text
    movie_code = await generate_unique_movie_code()

    MOVIES[movie_code] = {'link': movie_link, 'caption': ''}
    MOVIEST.append(movie_code)
    MOVIEST.append(movie_link)

    await message.answer("Film havolasini yubordingiz. Filmga ta'rif yuboring:", reply_markup=ReplyKeyboardRemove())
    await AddedMovie.add_movie_caption.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=AddedMovie.add_movie_caption)
async def get_movie_caption(message: types.Message, state: FSMContext):
    caption = message.text
    movie_code = MOVIEST[0]

    MOVIES[movie_code]['caption'] = caption

    await message.answer_video(video=MOVIES[movie_code]['link'], caption=f"Film kodi: {movie_code}\n{caption}", reply_markup=confirmation_buttons)
    await state.finish()



@dp.callback_query_handler(text='send_video')
async def add_movie_types(callback_query: types.CallbackQuery):
    await callback_query.answer("")
    await callback_query.message.answer("Film videosini yuboring")
    await AddedMovie.add_movie_video.set()



@dp.message_handler(content_types=types.ContentType.VIDEO, state=AddedMovie.add_movie_video)
async def get_movie_video(message: types.Message):
    movie_file = message.video.file_id
    movie_code = await generate_unique_movie_code()

    MOVIES[movie_code] = {'file': movie_file, 'caption': ''}
    MOVIEST.append(movie_code)
    MOVIEST.append(movie_file)

    await message.answer("Film videosini yubordingiz. Filmga ta'rif yuboring:", reply_markup=ReplyKeyboardRemove())
    await AddedMovie.add_movie_captionn.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=AddedMovie.add_movie_captionn)
async def get_movie_caption(message: types.Message, state: FSMContext):
    caption = message.text
    movie_code = MOVIEST[0]

    MOVIES[movie_code]['caption'] = caption

    await message.answer_video(video=MOVIES[movie_code]['file'], caption=f"Film kodi: {movie_code}\n{caption}", reply_markup=confirmation_buttons)
    await state.finish()




@dp.callback_query_handler(text='confirm')
async def confirm_movie(callback_query: types.CallbackQuery):
    await callback_query.answer()
    movie_code = MOVIEST[0]
    movie_data = MOVIES[movie_code]

    if 'link' in movie_data:
        movie_link = movie_data['link']
        caption = movie_data['caption']
        add_movie_to_db(movie_code, movie_link, caption)
        await callback_query.message.answer("Film saqlandi", reply_markup=ReplyKeyboardRemove())
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=None)
    
    elif 'file' in movie_data:
        movie_file = movie_data['file']
        caption = movie_data['caption']
        add_movie_to_db(movie_code, movie_file, caption)
        await callback_query.message.answer("Film saqlandi", reply_markup=ReplyKeyboardRemove())
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, reply_markup=None)


def get_movies_page(page=1, page_size=4):
    offset = (page - 1) * page_size
    movies = get_all_movies()
    return movies[offset:offset + page_size], len(movies)



@dp.callback_query_handler(text='show_movie')
async def show_movies(callback_query: types.CallbackQuery):
    await callback_query.answer()
    page = 1 
    movies_page, total_movies = get_movies_page(page)
    
    if movies_page:
        await callback_query.answer()
        
        movies_list = "\n".join([f"{i+1}. Kod - {movie[0]} Havola - {movie[1]}\n\n" for i, movie in enumerate(movies_page)])
        await send_movie_list(callback_query.from_user.id, movies_list, page, total_movies)
    else:
        await bot.send_message(callback_query.from_user.id, "Hech qanday film topilmadi.")

async def send_movie_list(chat_id, movies_list, page, total_movies):
    keyboard = create_movie_pagination_keyboard(page, total_movies)
    await bot.send_message(chat_id, f"Filmlar ro'yxati:\n\n{movies_list}", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('prev_movie_page', 'next_movie_page')))
async def movie_pagination_callback(callback_query: types.CallbackQuery):
    current_page = int(callback_query.data.split(':')[1])
    if 'prev_movie_page' in callback_query.data:
        page = current_page - 1
    else:
        page = current_page + 1
    
    movies_page, total_movies = get_movies_page(page)
    
    if movies_page:
        movies_list = "\n".join([f"{i+1}. Kod - {movie[0]} Havola - {movie[1]}\n\n" for i, movie in enumerate(movies_page)])
        await bot.edit_message_text(f"Filmlar ro'yxati:\n\n{movies_list}",
                                    callback_query.from_user.id,
                                    callback_query.message.message_id,
                                    reply_markup=create_movie_pagination_keyboard(page, total_movies))


pending_photo = {}
pending_video = {}

@dp.callback_query_handler(text='reklama')
async def show_ad_options(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Reklama turini tanlang:", reply_markup=add_rekmama)

@dp.callback_query_handler(text='send_photo')
async def request_photo(callback_query: types.CallbackQuery):
    await callback_query.answer()
    pending_photo.clear()
    pending_photo[callback_query.from_user.id] = {'status': 'awaiting_photo'}
    await bot.send_message(callback_query.from_user.id, "Rasm yuboring:")
    await AddedMovie.reklama_img.set()

@dp.callback_query_handler(text='send_videoo')
async def request_video(callback_query: types.CallbackQuery):
    await callback_query.answer()
    pending_video.clear()
    pending_video[callback_query.from_user.id] = {'status': 'awaiting_video'}
    await bot.send_message(callback_query.from_user.id, "Video yuboring:")
    await AddedMovie.reklama_video.set()


@dp.message_handler(content_types=['photo'], state=AddedMovie.reklama_img)
async def handle_photo(message: types.Message):
    if message.from_user.id in pending_photo and pending_photo[message.from_user.id]['status'] == 'awaiting_photo':
        pending_photo[message.from_user.id] = {'photo': message.photo[-1].file_id}
        await bot.send_message(message.from_user.id, "Rasm uchun Caption yuboring:")
        await AddedMovie.reklama_caption.set()

@dp.message_handler(content_types=['video'], state=AddedMovie.reklama_video)
async def handle_video(message: types.Message):
    if message.from_user.id in pending_video and pending_video[message.from_user.id]['status'] == 'awaiting_video':
        pending_video[message.from_user.id] = {'video': message.video.file_id}
        await bot.send_message(message.from_user.id, "Video uchun Caption yuboring:")
        await AddedMovie.reklama_caption.set()


@dp.message_handler(Text, state=AddedMovie.reklama_caption)
async def handle_caption(message: types.Message, state: MemoryStorage):
    user_id = message.from_user.id

    if user_id in pending_photo and 'photo' in pending_photo[user_id]:
        pending_photo[user_id]['caption'] = message.text
        await send_confirmation(message, 'photo')
        await state.finish()


    elif user_id in pending_video and 'video' in pending_video[user_id]:
        pending_video[user_id]['caption'] = message.text
        await send_confirmation(message, 'video')
        await state.finish()



async def send_confirmation(message: types.Message, ad_type: str):

    if ad_type == 'photo':
        await bot.send_photo(message.from_user.id, photo=pending_photo[message.from_user.id]['photo'],
                             caption=pending_photo[message.from_user.id]['caption'], reply_markup=confirm_button)

    elif ad_type == 'video':
        await bot.send_video(message.from_user.id, video=pending_video[message.from_user.id]['video'],
                             caption=pending_video[message.from_user.id]['caption'], reply_markup=confirm_button)

@dp.callback_query_handler(text='confirm_ad')
async def confirm_ad(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    
    if user_id in pending_photo:
        data = pending_photo.pop(user_id)
        user_ids = get_all_users_id()
        for uid in user_ids:
            try:
                await bot.send_photo(chat_id=uid, photo=data['photo'], caption=data['caption'])
            except BotBlocked:
                await callback_query.message.answer(f"Bot {uid} foydalanuvchiga xabar yubora olmadi, bot bloklangan.")
    
    elif user_id in pending_video:
        data = pending_video.pop(user_id)
        user_ids = get_all_users_id()
        for uid in user_ids:
            try:
                await bot.send_video(chat_id=uid, video=data['video'], caption=data['caption'])
            except BotBlocked:
                await callback_query.message.answer(f"Bot {uid} foydalanuvchiga xabar yubora olmadi, bot bloklangan.")
    
    await bot.send_message(user_id, "Reklama yuborildi!")


@dp.message_handler()
async def handle_movie_code(message: types.Message):
    user_id = message.from_user.id
    movie_code = message.text.strip()

    if await check_subscriptions(user_id):
        movie = get_movie_by_code(movie_code)
        if movie:
            movie_link = movie[0]
            caption = movie[1]
            try:
                await message.answer_video(video=movie_link, caption=caption)
            except Exception as e:
                await message.answer("Noto'g'ri video identifikatori yoki havola")
                logging.error(f"Video yuborishda xatolik: {e}")
        else:
            await message.answer("Kiritilgan kod mavjud emas. Iltimos, kodni tekshirib qaytadan kiriting")
    else:
        await message.answer(f"Xurmatli foydalanuvchi, kanallarga obuna bo'lmagansiz. Iltimos, obuna bo'ling 👇", reply_markup=channels)
    



async def on_start_up(dp):
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Bot ishga tushdi!')

async def on_shutdown(dp):
    for admin_id in ADMINS_ID:
        await bot.send_message(chat_id=admin_id, text='Bot o\'chdi!')

if __name__ == '__main__':
    setup_database()
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_up, on_shutdown=on_shutdown)
