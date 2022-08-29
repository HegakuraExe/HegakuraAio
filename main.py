#created by @hegakura
#created by @hegakura
#created by @hegakura

#Основные импорты
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ContentType, Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from asyncio import sleep
from time import strftime
import sqlite3
import asyncio
import logging
import datetime
import timedelta
import time

#Импорт конфига
import config as cfg

#Импорт данных из конфига
bot_token = cfg.TOKEN
bot_adm_id = cfg.ADMINID
bot_chat_id = cfg.CHATID

#Бот
bot = aiogram.Bot(bot_token, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

#Для обращения/вопросов
class Question(StatesGroup):
	msg = State()

#Для ответа
class AnswerToQuestion(StatesGroup):
	msg = State()

#Для рассылки
class Rass(StatesGroup):
	msg = State()

#Создание базы данных
connect = sqlite3.connect("users.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
	user_id INTEGER,
	user_name STRING,
	user_username STRING,
	user_question STRING,
	user_lastQ STRING,
	question_id INTEGER
)
""")
connect.commit()

#Девборд
@dp.message_handler(commands=['дев', 'dev'], commands_prefix='!./')
async def adm_ui(message):
	user_id = message.from_user.id
	if user_id == bot_adm_id:
		admin_menu = InlineKeyboardMarkup()
		statistics_bt = InlineKeyboardButton(
		text = '📊 Статистика',
		callback_data = 'stat'
		)
		mail_bt = InlineKeyboardButton(
		text = '✉️ Рассылка',
		callback_data = 'rassilka'
		)
		ping_bt = InlineKeyboardButton(
		text = '🖥 Пинг бота',
		callback_data = 'ping'
		)
		waiting_bt = InlineKeyboardButton(
		text = '🕰 Ждут ответа',
		callback_data = 'waiting'
		)
		cancel_del_bt = InlineKeyboardButton(
		text = '❌ Закрыть ❌',
		callback_data = 'cancel_del'
		)
		admin_menu.add(statistics_bt, ping_bt)
		admin_menu.add(mail_bt)
		admin_menu.add(waiting_bt)
		admin_menu.add(cancel_del_bt)
		await message.answer(
		f'🛠 Выберите пункт меню:',
		reply_markup=admin_menu
		)
	else:
		await message.reply(
		f'Вы не разработчик!'
		)

#Кнопка назад
@dp.callback_query_handler(text='cancel_del')
async def handle_cdel_button(c: types.CallbackQuery):
	user_id = c.from_user.id
	if user_id == bot_adm_id:
		await c.message.delete()
	else:
		await c.answer(
		text='Вы не разработчик!',
		show_alert=True
		)

#Кнопка стат
@dp.callback_query_handler(text='stat')
async def handle_stat_button(c: types.CallbackQuery):
	user_id = c.from_user.id
	if user_id == bot_adm_id:
		cancel_menu = InlineKeyboardMarkup()
		cancel_bt = InlineKeyboardButton(
		text = '🚫 Отмена',
		callback_data = 'cancel'
		)
		cancel_menu.add(cancel_bt)
		us = cursor.execute('SELECT * FROM users').fetchall()
		yes = cursor.execute('SELECT * FROM users WHERE user_question == "Да"').fetchall()
		await c.message.edit_text(
		f"""#STATISTICS
<b>USERS: {len(us)}</b> 👤
<b>WAITING: {len(yes)}</b> 🕰""", reply_markup = cancel_menu
)
	else:
		await c.answer(
		text='Вы не разработчик!', show_alert=True
		)

#Кнопка пинг
@dp.callback_query_handler(text='ping')
async def handle_ping_button(c: types.CallbackQuery):
	user_id = c.from_user.id
	if user_id == bot_adm_id:
		cancel_menu = InlineKeyboardMarkup()
		cancel_bt = InlineKeyboardButton(
		text = '🚫 Отмена', callback_data = 'cancel'
		)
		cancel_menu.add(cancel_bt)
		a = time.time()
		bot_msg = await c.message.edit_text(
		text='Проверка...'
		)
		if bot_msg:
			b = time.time()
		await c.message.edit_text(
		f'🤖 PING: <code>{round((b-a)*1000, 2)}</code> м/с.', reply_markup = cancel_menu
		)
	else:
		await c.answer(
		text='Вы не разработчик!', show_alert=True
		)

#Кнопка назад
@dp.callback_query_handler(text='cancel')
async def cancel_wnum_button_handler(c: types.callback_query):
	user_id = c.from_user.id
	if user_id == bot_adm_id:
		admin_menu = InlineKeyboardMarkup()
		statistics_bt = InlineKeyboardButton(
		text = '📊 Статистика', callback_data = 'stat'
		)
		mail_bt = InlineKeyboardButton(
		text = '✉️ Рассылка', callback_data = 'rassilka'
		)
		ping_bt = InlineKeyboardButton(
		text = '🖥 Пинг бота', callback_data = 'ping'
		)
		waiting_bt = InlineKeyboardButton(
		text = '🕰 Ждут ответа', callback_data = 'waiting'
		)
		cancel_del_bt = InlineKeyboardButton(
		text = '❌ Закрыть ❌', callback_data = 'cancel_del'
		)
		admin_menu.add(statistics_bt, ping_bt)
		admin_menu.add(mail_bt)
		admin_menu.add(waiting_bt)
		admin_menu.add(cancel_del_bt)
		await c.message.edit_text(
		f'🛠 Выберите пункт меню:',
		reply_markup=admin_menu
		)
	else:
		await c.answer(
		text='Вы не разработчик!',
		show_alert=True
		)

#Кнопка вайтинг
@dp.callback_query_handler(text='waiting')
async def witing_button_handler(c: types.callback_query):
	user_id = c.from_user.id
	if user_id == bot_adm_id:
		cancel_menu = InlineKeyboardMarkup()
		cancel_bt = InlineKeyboardButton(
		text = '🚫 Отмена',
		callback_data = 'cancel'
		)
		cancel_menu.add(cancel_bt)
		waiters = ""
		cursor.execute(f"SELECT user_name FROM users WHERE user_question == 'Да'")
		waiters_query = cursor.fetchall()
		user_nms = [user[0] for user in waiters_query]
		for usernm in user_nms:
			waiters += f"👤 Ник: <code>{usernm}</code>" + str('\n')
		if str(waiters) == "":
		    await c.message.edit_text(
		    f'✅ На данный момент ожиданий нет!',
		    reply_markup = cancel_menu
		    )
		else:
		    await c.message.edit_text(
		    f'🕰 <b>Ожидают ответа:</b>\n' + str(waiters),
		    reply_markup = cancel_menu
		    )
	else:
		await c.answer(
		text='Вы не разработчик!',
		show_alert=True
		)


#Рассылка
@dp.callback_query_handler(text="rassilka")
async def send_rass(call: types.CallbackQuery):
	user_id = call.from_user.id
	if user_id == bot_adm_id:
		await call.message.edit_text(
		text='🖋 Введите текст/фото для рассылки:'
		)
		await Rass.msg.set()
	else:
		await call.answer(
		text='Вы не разработчик!',
		show_alert=True
		)

@dp.message_handler(content_types=ContentType.ANY, state=Rass.msg)
async def rassilka_msgl(message: types.Message, state: FSMContext):
	await state.finish()
	cursor.execute(f"SELECT user_id FROM users")
	users_query = cursor.fetchall()
	user_ids = [user[0] for user in users_query]
	nowtim = time.time()
	confirm = []
	decline = []
	bot_msg = await message.answer(
	f'Рассылка началась...'
	)
	for i in user_ids:
		try:
			await message.copy_to(i)
			confirm.append(i)
		except:
			decline.append(i)
		await asyncio.sleep(0.3)
	nowtime = time.time()
	uptime = round(nowtime - nowtim)
	uptimestr = str(time.strftime("%H:%M:%S", time.gmtime(int(uptime))))
	await bot_msg.edit_text(
	f'📣 Рассылка завершена!\n\n'
	f'✅ Успешно: {len(confirm)}\n'
	f'❌ Неуспешно: {len(decline)}\n'
	f'⌚ Время: {str(uptimestr)}'
	)

#Команда /start
@dp.message_handler(commands=['start', 'старт', 'начать'], commands_prefix='/!.#')
async def start_cmd(msg: types.Message):
	user_id = msg.from_user.id #Получаем ID пользователя
	user_name = msg.from_user.full_name #Получаем полное имя пользователя
	user_username = msg.from_user.username #Получаем юзернем пользователя
	user_question = 'Нет' #По умолчанию вопрос не задан
	user_lastQ = 'Нет' #Последнее обращение (время и дата)

	#Регистрация пользователя
	cursor.execute(f"SELECT user_id FROM users WHERE user_id = '{user_id}'")
	#Проверка пользователя в базе данных
	if cursor.fetchone() is None:

		#Регистрация пользователя
		cursor.execute(
			f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?);", (
			user_id,
			user_name,
			user_username,
			user_question,
			user_lastQ,
			0)
			)
		connect.commit()

		#Отправка приветствия
		await msg.answer(
			f'👋 Привет <a href="tg://user?id={user_id}">пользователь</a>, здесь ты сможешь задавать вопросы касательно ботов владельцу, а также предложить идею для его нового бота.'
			)

		#Проверка юзернейма
		if user_username is None:
			uname = 'Not entered'
		else:
			uname = user_username

		#Отправка сообщения в лог. чат
		await bot.send_message(
			bot_chat_id,
			f'✅ #NewMemberInBot\n'
			f'👤 <b>Name:</b> {user_name}\n'
			f'📎 <b>Username:</b> {user_username}\n'
			f'🆔 <b>ID:</b> <code>{user_id}</code>'
			)
	else:

		#Отправка иного текста
		await msg.answer(
			f'Ты уже вводил(-а) команду /start\n'
			f'Больше этого делать - <b>не нужно!</b>'
			)

#Выйти из чата если это необходимо
@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def bot_in_chat(msg: Message):

	#Проверка бота в чате
	new_chat = msg.new_chat_members[0]
	if str(new_chat.mention) == '@hegakuraBot':

		#Отправка сообщения и выход из чата
		await msg.answer(
			f'❎ Я работаю только в л/с!'
			)
		await bot.leave_chat(
		msg.chat.id
		)
	else:
		pass

#Отправить обращение
@dp.message_handler(commands=['обращение', 'question', 'вопрос'], commands_prefix='!./#')
async def cmd_question(message: types.Message):
	user_id = message.from_user.id

	#Проверка типа чата
	if message.chat.type == 'private':
		user_question_stat = cursor.execute(f"SELECT user_question FROM users WHERE user_id = '{user_id}'").fetchone()
		user_status = (user_question_stat[0])

		#Проверка статуса обращения
		if str(user_status) == 'Нет':
			await message.answer(
				f'📄 Отправьте текст или медиа для обращения:'
				)
			await Question.msg.set()
		else:
			await message.answer(
				f'Вы уже отправляли обращение, дождитесь пока на него ответят!'
				)
	else:
		await message.reply(
			f'Бот работает только в л/с!'
			)

		#Выходи из чата
		await bot.leave_chat(
		msg.chat.id
		)

#Приём обращения в лог. чат
@dp.message_handler(content_types=ContentType.ANY, state=Question.msg)
async def question_finish(message: types.Message, state: FSMContext):
	await state.finish()
	user_id = message.from_user.id #Получаем ID пользователя
	user_name = message.from_user.full_name #Получаем полное имя пользователя
	user_username = message.from_user.username #Получаем юзернем пользователя

	#Отправка обращения
	bot_msg = await message.answer(
		f'🕰 Ваше обращение отправляется...'
		)

	await bot.send_message(bot_chat_id,
	f'✅ #NewQuestion\n'
	f'👤 <b>Name:</b> {user_name}\n'
	f'📎 <b>Username:</b> {user_username}\n'
	f'🆔 <b>ID:</b> <code>{user_id}</code>\n'
	f'<b>Question</b> 🔽'
	)

	#Копирование обращения
	await message.copy_to(
	bot_chat_id
	)

	#Конец
	await bot_msg.edit_text(
		f'✅ Ваше обращение отправлено!\n'
		f'🕰 Дождитесь пока на него ответят'
		)
	#Обновление базы данных
	cursor.execute('UPDATE users SET user_question = ? WHERE user_id = ?',("Да", message.from_user.id))
	cursor.execute('UPDATE users SET user_lastQ = ? WHERE user_id = ?', (strftime("%d.%m.%Y, %H:%M:%S"), message.from_user.id))
	connect.commit()

#Статус
@dp.message_handler(commands=['статус', 'status'], commands_prefix='!./#')
async def status_cmd(msg: types.Message):
	user_id = msg.from_user.id

	#Если это не админ
	if user_id != bot_adm_id:
		quest_stat = cursor.execute(f"SELECT user_question FROM users WHERE user_id = '{user_id}'").fetchone()
		que_st = (quest_stat[0])
		quest_time = cursor.execute(f"SELECT user_lastQ FROM users WHERE user_id = '{user_id}'").fetchone()
		que_time = (quest_time[0])
		if str(que_st) == 'Нет':
			que_stts = '✅ Вы можете отправить обращение'
		elif str(que_st) == 'Да':
			que_stts = '❎ На ваше обращение ещё не ответили'
		if str(que_time) == 'Нет':
			que_ttime = '🕰 Вы ещё не отправляли обращений'
		else:
			que_ttime = "🕰" + que_time
		await msg.answer(
			f'{que_stts}'
			f'{que_ttime}'
			)
	else:
		await msg.answer(
			f'Ты админ!'
			)

#Прикрепить ID
@dp.message_handler(commands=['привязать', 'bind'], commands_prefix='!./#')
async def bind_cmd(msg: types.Message):
	user_id = msg.from_user.id

	#Если это админ
	if user_id == bot_adm_id:
		quest_id = cursor.execute(f"SELECT question_id FROM users WHERE user_id = '{user_id}'").fetchone()
		que_id = (quest_id[0])

		#Если ИД не привязан
		if int(que_id) == 0:

			#Привязка
			answer_id = int(msg.text.split()[1])
			cursor.execute('UPDATE users SET question_id = ? WHERE user_id = ?', (answer_id, msg.from_user.id))
			connect.commit()
			await msg.answer(
				f'✅ Успешно! Вы привязали ID для ответа'
				)
		else:
			await msg.answer(
				f'❎ Не успешно! Вы ещё не ответили на обращение: <code>{que_id}</code>'
				)
	else:
		pass

#Ответ на обращение
@dp.message_handler(commands=['ответить', 'ответ', 'answer'], commands_prefix='!./#')
async def answer_question(message: types.Message):
	user_id = message.from_user.id

	#Если это админ
	if user_id == bot_adm_id:
		quest_id = cursor.execute(f"SELECT question_id FROM users WHERE user_id = '{user_id}'").fetchone()
		que_id = (quest_id[0])

		#Если ИД привязан
		if int(que_id) != 0:
			await message.answer(
				f'📄 Отправьте текст или медиа для ответа:'
				)
			await AnswerToQuestion.msg.set()

		else:
			await message.answer(
				f'❎ Вы еще не привязали идентификатор для ответа!'
				)

	else:
		pass

#Отправка ответа пользователю
@dp.message_handler(content_types=ContentType.ANY, state=AnswerToQuestion.msg)
async def answer_finish(message: types.Message, state: FSMContext):
	await state.finish()
	user_id = message.from_user.id

	#Получение ИД
	quest_id = cursor.execute(f"SELECT question_id FROM users WHERE user_id = '{user_id}'").fetchone()
	que_id = (quest_id[0])

	#Отправка обращения
	bot_msg = await message.answer(
		f'Ваш ответ обрабатывается...'
		)

	#Копирование обращения
	await bot.send_message(que_id,
		f'✅ Администратор ответил вам на ваше обращение:'
		)

	await message.copy_to(
	que_id
	)

	#Конец
	await bot_msg.edit_text(
		f'✅ Ваш ответ отправлен!'
		)

	#Обновление базы данных
	cursor.execute('UPDATE users SET user_question = ? WHERE user_id = ?', ("Нет", que_id))
	cursor.execute('UPDATE users SET question_id = ? WHERE user_id = ?', (0, user_id))
	connect.commit()

@dp.message_handler()
async def echo_help(message: types.Message):
	if message.chat.type == 'private':
		await message.answer(
		f'<b>Команды бота</b>:\n'
		f'/question - задать вопрос (отправить обращение) владельцу\n'
		f'/status - статусы ваших обращений'
		)
	else:
		pass

#Запуск
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
