#Created by @hegakura
#Created by @hegakura
#Created by @hegakura
#Profile cmd

#IMPORTS ---
import aiogram
from aiogram import Bot, Dispatcher, executor, types
import logging

#BOT ---
bot = aiogram.Bot('YourBotToken', parse_mode='html')
dp = Dispatcher(bot)
logging.basicConfig(level = logging.INFO)

#handler
@dp.message_handler(commands=['profile', 'info', 'infa'], commands_prefix='/!.#')
async def hegakura_profile(message: types.Message):
	user_id = message.from_user.id
	user_first_name = message.from_user.first_name
	user_last_name = message.from_user.last_name
	user_username = message.from_user.username
	if user_last_name is None:
		user_lname = 'Не указана.'
	else:
		user_lname = user_last_name
	if user_username is None:
		user_uname = 'Не указан.'
	else:
		user_uname = "@" + user_username
	if message.chat.type == 'private':
		await message.answer(
			f'<b>Профиль пользователя</b>:\n'
			f'<b>Имя</b>: {user_first_name}\n'
			f'<b>Фамилия</b>: {user_lname}\n'
			f'<b>Юзернейм</b>: {user_uname}\n'
			f'<b>ID</b>: <code>{user_id}</code>'
			)
	else:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id
			user_first_name = message.reply_to_message.from_user.first_name
			user_last_name = message.reply_to_message.from_user.last_name
			user_username = message.reply_to_message.from_user.username
			if user_last_name is None:
				user_lname = 'Не указана.'
			else:
				user_lname = user_last_name
			if user_username is None:
				user_uname = 'Не указан.'
			else:
				user_uname = "@" + user_username
			admins_id = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
			if user_id in admins_id:
				await message.reply(
					f'<b>Профиль пользователя</b>:\n'
					f'<b>Имя</b>: {user_first_name}\n'
					f'<b>Фамилия</b>: {user_lname}\n'
					f'<b>Юзернейм</b>: {user_uname}\n'
					f'<b>ID</b>: <code>{user_id}</code>\n'
					f'<b>Статус в чате</b>: Администратор.'
					)
			else:
				await message.reply(
					f'<b>Профиль пользователя</b>:\n'
					f'<b>Имя</b>: {user_first_name}\n'
					f'<b>Фамилия</b>: {user_lname}\n'
					f'<b>Юзернейм</b>: {user_uname}\n'
					f'<b>ID</b>: <code>{user_id}</code>\n'
					f'<b>Статус в чате</b>: Участник.'
					)
		else:
			admins_id = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
			if user_id in admins_id:
				await message.reply(
					f'<b>Профиль пользователя</b>:\n'
					f'<b>Имя</b>: {user_first_name}\n'
					f'<b>Фамилия</b>: {user_lname}\n'
					f'<b>Юзернейм</b>: {user_uname}\n'
					f'<b>ID</b>: <code>{user_id}</code>\n'
					f'<b>Статус в чате</b>: Администратор.'
					)
			else:
				await message.reply(
					f'<b>Профиль пользователя</b>:\n'
					f'<b>Имя</b>: {user_first_name}\n'
					f'<b>Фамилия</b>: {user_lname}\n'
					f'<b>Юзернейм</b>: {user_uname}\n'
					f'<b>ID</b>: <code>{user_id}</code>\n'
					f'<b>Статус в чате</b>: Участник.'
					)

#LAUNCH ---
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
