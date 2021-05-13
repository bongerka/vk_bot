from random import shuffle, randint 	
import asyncio											# python C:\Users\ПК\Downloads\sdvb.py
from vkbottle_types import BaseStateGroup
from vkbottle.bot import Bot, Message
from vkbottle import (
	Keyboard, 
	KeyboardButtonColor, 
	Text
	)


token = '1eefd03cabef397c236c72b85a734fe05d3b73171a6dd9a01f4beb7c5c5aa6a08a814bbdbdcea81a23012'
bot = Bot(token=token)
chat_id = 2*10**9+1



@bot.loop_wrapper.interval(seconds=36000)
async def repeated_task():
	await bot.api.messages.send(peer_id=chat_id, random_id=0, message='Пора ботать')



new_nums = []
check_word = ''
busy = False
did_t = -2
cor_t = 0

bot_kb = (
	Keyboard(one_time=False, inline=True)
	.add(Text("10 ЗАДАНИЕ"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("11 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.row()
	.add(Text("12 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.add(Text("13 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)

menu_kb = (
	Keyboard(one_time=False, inline=True)
	.add(Text("БОТ РУССКОГО"), color=KeyboardButtonColor.POSITIVE)
	.get_json()
)

tasks_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("И"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("Е"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("СТОП"), color=KeyboardButtonColor.NEGATIVE)
	.add(Text("ПРОРАБОТКА"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)

end_kb = (
	Keyboard(one_time=False, inline=True)
	.add(Text("МЕНЮ"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)

async def newState(peer_id, obj):
	global busy
	await bot.state_dispenser.set(peer_id, obj)
	busy = True

async def delState(peer_id):
	global busy
	await bot.state_dispenser.delete(peer_id)
	busy = False

def check_orph10(s):
	if s.islower():
		return s[:2] + '_' + s[3:]
	else:
		for i in s:
			if i.isupper():
				return s[:s.index(i)] + '_' + s[s.index(i) + 1:]

def get_ex10():
	with open(r'\ex10.txt') as file:
		ans = [x.strip() for x in file.readline().split(',')]
		for i in file.readlines():
			inp = [x.strip() for x in i.split('-')]
			ans.append(inp[0])
			ans.append(inp[1])
	return ans



def shuf(ll):  
	shuffle(ll)
	return ll


def get_word(ll):
	ans = ll[0]
	del ll[0]
	return ans, ll


class STATE_EX(BaseStateGroup):
	STATE_EX_10 = 10
	STATE_2 = 2

class STATE_MENU(BaseStateGroup):
	BOT_RUS = 0
	BOT_TASK = 1




@bot.on.private_message(func=lambda message: busy == False and message.text.lower() == 'меню' or message.text.lower() == '[club187730402|@botaiege]')
async def hi_handler(message: Message):
	if message.text.lower() == 'меню':
		users_info = await bot.api.users.get(message.from_id)
		await message.answer(message='{}, выбери раздел?'.format(users_info[0].first_name), keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_RUS)
	elif message.text.lower() == '[club187730402|@darowanoga]':
		await message.answer(message='Отъебись')




@bot.on.private_message(state=STATE_MENU.BOT_RUS)
async def hi_handler(message: Message):
	await message.answer(message='Выбери задание (зеленые готовы)', keyboard=bot_kb)
	await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_TASK)





@bot.on.private_message(state = STATE_MENU.BOT_TASK)
async def hi_handler(message: Message):
	global did_t
	global cor_t
	global new_words
	if message.text == '[club187730402|@botaiege] 10 ЗАДАНИЕ' or message.text == '10 ЗАДАНИЕ':
		pror_words = []
		pror_words_new = []
		did_t = -2
		cor_t = 0
		words = get_ex10()
		new_words = shuf(words)
		await message.answer(message='Начнем:\n-----------------------------------------------')
		await do_ex10(message)
	elif message.text == '[club187730402|@botaiege] 7 ЗАДАНИЕ' or message.text == '7 ЗАДАНИЕ':
		pror_words = []
		pror_words_new = []
		did_t = -2
		cor_t = 0
		await message.answer(message='Начнем:\n-----------------------------------------------')
		await do_task7()
		NOWWORD = send_task7()
		new_i = NOWWORD[:-2] + '__'
		await message.answer(message='Слово: ' + new_i, keyboard=tasks_kb)
		await message.answer(message='----------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS7)
	else:
		await message.answer(message='долбаеб?')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_RUS)




@bot.on.private_message(state=STATE_EX.STATE_EX_10)
async def do_ex10(message: Message):
	global check_word
	global busy
	global new_words
	global old_message
	global did_t
	global cor_t
	did_t += 1
	if (message.text == '[club187730402|@botaiege] 10 ЗАДАНИЕ' or message.text == '10 ЗАДАНИЕ') and busy == False:
		get_word_ans, new_nums = get_word(new_words) 
		await message.answer(message=check_orph10(get_word_ans))
		check_word = get_word_ans
		await newState(message.peer_id, STATE_EX.STATE_EX_10)
		old_message = message.id
	else:
		if message.text.lower() == '[club187730402|@botaiege] стоп' or message.text.lower() =='стоп' or len(new_words) == 0:
			await delState(message.peer_id)
			await message.answer(message='Результат: ' + str(cor_t) + '/' + str(did_t))
			if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота...')
			elif did_t - cor_t == 0: await message.answer(message='Минимум 92 будет')
			elif did_t - cor_t < 3: await message.answer(message='Заебись, конечно, но, чел, егэ через 0 дней.....')
			else:  await message.answer(message='Чел, проспись а..............')
		else:
			get_word_ans, new_words = get_word(new_words)
			cord = check_orph10(check_word).index('_')
			if message.text.lower() == check_word[cord].lower() or message.text.lower() == '[club187730402|@botaiege] ' + check_word[cord].lower():
				cor_t += 1
				await message.answer(message='✅ Верно, ' + check_word[:cord] + check_word[cord].upper() + check_word[cord+1:] + 
					'\n-----------------------------------------------\n' + check_orph10(get_word_ans))
				#await bot.api.messages.delete(message_id=old_message)
			else:
				await message.answer(message='❌ Неверно, '.upper() + check_word[:cord] + check_word[cord].upper() + check_word[cord+1:] + 
					'\n-----------------------------------------------\n' + check_orph10(get_word_ans))
			check_word = get_word_ans 
			await newState(message.peer_id, STATE_EX.STATE_EX_10)

@bot.on.private_message(func=lambda message: message.text.lower() != 'меню' and message.text.lower() != '[club187730402|@botaiege]')
async def hi_handler(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	await message.answer(message='{}, нажми кнопку меню'.format(users_info[0].first_name), keyboard=end_kb)

bot.run_forever()
