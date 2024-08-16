# from aiogram.dispatcher.filters.state import State, StatesGroup


# class AddedMovie(StatesGroup):
#     add_movie = State()
#     add_movie_link = State()
#     add_movie_video = State()
#     send_video = State()
#     add_movie_caption = State()




from aiogram.dispatcher.filters.state import State, StatesGroup

class AddedMovie(StatesGroup):
    add_movie = State()
    add_movie_link = State()
    add_movie_video = State()
    send_video = State()
    add_movie_caption = State()
    add_movie_captionn = State()
    send_movie = State()
    reklama_video = State()
    reklama_img = State()
    reklama_caption = State()
    reklama_confirm = State()
