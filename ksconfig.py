SAVE = ''#тут будет токен

#Settings для ...
settings = {
	'NAME BOT': 'Kitsunes',
	'ID': 749590747317272647,
	'PREFIX': '!'
}


лист1 = ['rs-all', 'rs-clear', 'кы-сдуфк', 'кы-фдд', 'удалить-all', 'удалить-clear', 'remove-shop-all', 'remove-shop-clear', 'shop-remove-all', 'shop-remove-clear', 'алах-акбар']
команда_время = ['время', 'time'] #команда, которая показывает время
команда_погода = ['weather', 'погода'] #команда, которая показывает погоду
карта_человека = ['карточка'] #показывает инфу человека
фильтр = [ 'хуй', ' пизда', 'сука', 'suka', 'syka', 'cyka', 'cuka', 'пидор', 'пидрас', 'ебал', 'pidor', 'pidoras', 'нахуй', 'пиздец', 'ахуеть', 'ахуеваю', 'хуя' ] #удалает и отпровляет в лс, что "нельзя писать токое"
выгоняющие_слова = ['kick'] # команда, kick выгоняет с сервера
блокирующие_слова = [ 'бан', 'ифт', ',fy', 'забанить', 'наказать'] #команда, ban выгоняет и блокирует заход на сервер
разблокирующие_слова = ['unban'] #команда, unban освобождает от блока захода на сервер
канал_сюда = ['play', 'играть'] #команда, которая начинает играть музыку
чистка = ['clear', 'elfkbnm', 'очистить', 'cl', 'сд'] #команда, которая очищает чат
удаление = ['удалить', 'remove-shop', 'shop-remove', 'rs'] #команда, которая приглfшает бота на голосовой канал
добавление = ['shop-add', 'добавить', 'add-shop', 'as'] #команда, которая выгоняет бота из голосового канала
молчанка = ['обеззвучить', 'молчанка', 'мут', 'молчи','не матерись','muted', 'узбагойся'] #команда, которая кидает в тюрьму на несколько часов
награда = ['give', 'пшму', 'награда', 'yfuhflf',' gift', 'подарок', 'подарить','наградить','фцфкв','award']
штраф = ['штраф','inhfa','оштрафовать','забрать','отнять','jnyfznm','take']
помощь = ['рудз', 'ihelp', '+help', 'помощь', 'информация', 'инфо', 'памагити', 'на помощь', 'спасити', 'хелп','gjvjom'] #команда, которая даёт информацию о командах
бабки = ['bal','b','баланс','ифдфтсу',',fkfyc','кошелёк','qiwi','бабки','balance']
магазин =['магазин', 'vfufpby', 'shop', 'шоп', 'магаз', 'ырщз']
покупка =['buy', 'buy-role', 'инг', 'купить', 'regbnm', 'атдай']

id_канал_админ = 747004862386012272 #канал для админов
id_канал_новости = 751056242390204436 #канал на котором делаем опрос
id_канал_привет = 710897225319841827 #канал, на котором пишет, когда зашёл новичёк

мут = 755448748976635924 #роль, запрещающая пользователю писат в чат
роль_правила = 745397337999933470 #роль, подтверждающая правила
модер = 751043972755095679 #роль, которая использует Модер сервера
админ = 745223609756155934 #роль, которую использует Администратор сервера


#список ролей в сответствии с эмоджи

POST_ID = 745395662266302594 # id поста с которого будут считываться реакции
channel_id = 745393198397915326 # id канала "привет" c который подтверждает правила
message_id = 745395662266302594 # не ебу зачем, но вот ещё раз пост для реаций
ROLES = {
    '🆗': 745397337999933470,
}

EXCROLES = () #список исключений ролей, которые не учитываються при подсчёте кол. ролей у пользователя
MAX_ROLES_PER_USER = 99 #максимальное количество ролей которые может взять пользователь от эмоции