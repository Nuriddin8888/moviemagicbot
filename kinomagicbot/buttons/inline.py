from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

channels = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Obuna bo'lish ➕", url="https://t.me/Mutalov_Nuriddin"),
        ],
        [
            InlineKeyboardButton(text="Tasdiqlash ✅",callback_data="check_subscribe"),
        ]
    ]
)


admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Show user",callback_data="show_user"),
        ],
        [
            InlineKeyboardButton(text="Add Movie",callback_data="add_movie"),
        ],
        [
            InlineKeyboardButton(text="Show Movie",callback_data="show_movie"),
        ],
        [
            InlineKeyboardButton(text="Reklama",callback_data="reklama"),
        ]
    ]
)


caption = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Enter Description", callback_data='enter_description')
        ]
    ]
)


confirmation_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tasdiqlash", callback_data='confirm'),
        ]
    ]
)


movie_insert_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Send Link",callback_data="send_link"),
        ],
        [
            InlineKeyboardButton(text="Send Video",callback_data="send_video"),
        ]
    ]
)


add_rekmama = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Send Photo",callback_data="send_photo"),
            InlineKeyboardButton(text="Send Video",callback_data="send_videoo")
        ]
    ]
)


confirm_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tasdiqlash",callback_data="confirm_ad")
        ]
    ]
)


def create_pagination_keyboard(page, total_users, page_size=4):
    max_page = (total_users + page_size - 1) // page_size
    prev_button = InlineKeyboardButton('◀️', callback_data=f'prev_page:{page}')
    next_button = InlineKeyboardButton('▶️', callback_data=f'next_page:{page}')
    page_button = InlineKeyboardButton(f'{page}/{max_page}', callback_data='current_page')
    
    keyboard = InlineKeyboardMarkup()
    
    if page > 1:
        keyboard.add(prev_button)
    
    keyboard.add(page_button)
    
    if page < max_page:
        keyboard.add(next_button)
    
    return keyboard


def create_movie_pagination_keyboard(page, total_movies, page_size=4):
    max_page = (total_movies + page_size - 1) // page_size
    prev_button = InlineKeyboardButton('◀️', callback_data=f'prev_movie_page:{page}')
    next_button = InlineKeyboardButton('▶️', callback_data=f'next_movie_page:{page}')
    page_button = InlineKeyboardButton(f'{page}/{max_page}', callback_data='current_movie_page')
    
    keyboard = InlineKeyboardMarkup()
    
    if page > 1:
        keyboard.add(prev_button)
    
    keyboard.add(page_button)
    
    if page < max_page:
        keyboard.add(next_button)
    
    return keyboard