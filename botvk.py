from random import shuffle, randint 
from pathlib import Path	
import asyncio											# python C:\Users\ПК\Downloads\botvk.py
from vkbottle_types import BaseStateGroup
from vkbottle.bot import Bot, Message
from vkbottle import (
	Keyboard, 
	KeyboardButtonColor, 
	Text
	)



dir = Path('botvk.py').parent # r'C:\Users\ПК\Downloads\botvk.py' \\\\ 'botvk.py'
token = '1eefd03cabef397c236c72b85a734fe05d3b73171a6dd9a01f4beb7c5c5aa6a08a814bbdbdcea81a23012'
bot = Bot(token=token)
chat_id = 2*10**9+1



@bot.loop_wrapper.interval(seconds=18000)
async def repeated_task():
	await bot.api.messages.send(peer_id=chat_id, random_id=0, message='Пора ботать')


users_busy = dict()
users_words = dict()
users_check_word = dict()
users_points = dict()



bot_kb = (
	Keyboard(one_time=False, inline=True)
	.add(Text("7 ЗАДАНИЕ"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("10 ЗАДАНИЕ"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("11 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.add(Text("12 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)

menu_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("БОТ РУССКОГО"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("ДОБАВЛЕНИЕ СЛОВ"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)

tasks_kb = (
	Keyboard(one_time=False, inline=False)
	.add(Text("И"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("Е"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("СТОП"), color=KeyboardButtonColor.NEGATIVE)
	.add(Text("ПРОРАБОТКА"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)

end_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("МЕНЮ"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)



class STATE_EX(BaseStateGroup):
	STATE_EX_7_10 = 710
	STATE_EX_7 = 7



class STATE_MENU(BaseStateGroup):
	BOT_RUS = 0
	BOT_TASK = 1


def changeDict(dictt, peer_id, obj):
	if dictt.get(peer_id) != None:
		dictt.pop(peer_id)
	dictt.setdefault(peer_id, obj)

async def newState(peer_id, obj):
	await bot.state_dispenser.set(peer_id, obj)
	changeDict(users_busy, peer_id, True)

async def delState(peer_id):
	await bot.state_dispenser.delete(peer_id)
	changeDict(users_busy, peer_id, False)


def check_orph10(s):
	if s.islower():
		return s
	else:
		ans = ''
		for i in s:
			if i.isupper() and '_' not in ans:
				ans += '_'
			elif i.isupper() and '_' in ans:
				pass
			else:
				ans += i
		return ans


def getCords(s):
	cc = 0
	mincord = 100
	for i in range(len(s)):
		if s[i].isupper():
			cc += 1
			mincord = min(mincord, i)
	return (mincord, cc)


def get_ex10(href):
	with open(dir / href) as file:
		ans = []
		for i in file.readlines():
			inp = [x.strip() for x in i.split(';')]
			for x in inp:
				ans.append(x)
	return ans


def shuf(ll):  
	shuffle(ll)
	return ll


def get_word(ll):
	ans = ll[0]
	del ll[0]
	return ans, ll



@bot.on.private_message(func=lambda message: (users_busy.get(message.peer_id) == False or users_busy.get(message.peer_id) == None) and (message.text.lower() == 'меню' or message.text.lower() == '[club187730402|@botaiege]'))
async def hi_handler(message: Message):
	changeDict(users_busy, message.peer_id, False)
	if message.text.lower() == 'меню':
		users_info = await bot.api.users.get(message.from_id)
		await message.answer(message='{}, выбери раздел?'.format(users_info[0].first_name), keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_RUS)
	elif message.text.lower() == '[club187730402|@darowanoga]':
		await message.answer(message='Отъебись')




@bot.on.private_message(state=STATE_MENU.BOT_RUS)
async def hi_handler(message: Message):
	if message.text.lower() == '[club187730402|@botaiege] бот русского' or message.text.lower() == 'бот русского':
		await message.answer(message='Выбери задание (зеленые готовы)', keyboard=bot_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_TASK)
	else:
		await message.answer(message='Еще не готово :(', keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_RUS)




@bot.on.private_message(state = STATE_MENU.BOT_TASK)
async def hi_handler(message: Message):
	if message.text.lower() == '10 задание':
		changeDict(users_points, message.peer_id, (-2, 0))
		words = get_ex10("ex10.txt")
		changeDict(users_words, message.peer_id, shuf(words))
		await do_ex10(message)
	elif message.text.lower() == '7 задание':
		#await message.answer(message='Выберите форму слов', keyboard=Keyboard(one_time=True, inline=False).add(Text("МЕНЮ"), color=KeyboardButtonColor.PRIMARY).get_json())
		changeDict(users_points, message.peer_id, (-2, 0))
		words = get_ex10("ex7.txt")
		changeDict(users_words, message.peer_id, shuf(words))
		await do_ex10(message)
	else:
		await message.answer(message='долбаеб?')
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_TASK)




@bot.on.private_message(state=STATE_EX.STATE_EX_7_10)
async def do_ex10(message: Message):
	#try:
	points = users_points.get(message.peer_id)
	did_t = points[0]
	cor_t = points[1]
	did_t += 1
	new_words = users_words.get(message.peer_id)
	if users_busy.get(message.peer_id) == False:
		get_word_ans, new_words = get_word(new_words) 
		changeDict(users_words, message.peer_id, new_words)
		changeDict(users_check_word, message.peer_id, get_word_ans)
		await newState(message.peer_id, STATE_EX.STATE_EX_7_10)
		if message.text.lower() == '10 задание':
			await message.answer(message='Начнем:\n----------------------------------------\n' + check_orph10(get_word_ans), keyboard=tasks_kb)
		elif message.text.lower() == '7 задание':
			await message.answer(message='Клавиатура заебатая (не обращаем внимание)\n\nНачнем:\n----------------------------------------\n' + check_orph10(get_word_ans), keyboard=tasks_kb)
	else:
		if message.text.lower() =='стоп' or len(new_words) == 0:
			users_info = await bot.api.users.get(message.from_id)
			await delState(message.peer_id)
			await message.answer(message=f'{users_info[0].first_name}, твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
			if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота')
			elif did_t - cor_t == 0: await message.answer(message='Минимум 92 будет')
			elif did_t - cor_t < 3: await message.answer(message='Not bad')
			else:  await message.answer(message='Ты не Илья, тебе можно')
		elif message.text.lower() =='проработка':
			users_info = await bot.api.users.get(message.from_id)
			await message.answer(message='бигбой не успел сделать')
			await delState(message.peer_id)
			await message.answer(message=f'{users_info[0].first_name}, твой результат: ' + str(cor_t) + '/' + str(did_t))
		else:
			check_word = users_check_word.get(message.peer_id)
			get_word_ans, new_words = get_word(new_words)
			changeDict(users_words, message.peer_id, new_words)
			cord_start, cord_end = getCords(check_word)
			cord_end += cord_start
			if message.text.lower() == check_word[cord_start:cord_end].lower():
				cor_t += 1
				await message.answer(message='✅ Верно, ' + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:] + 
					'\n----------------------------------------\n' + check_orph10(get_word_ans), keyboard=tasks_kb)
			else:
				await message.answer(message='❌ Неверно, '.upper() + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:] + 
					'\n----------------------------------------\n' + check_orph10(get_word_ans), keyboard=tasks_kb)
			changeDict(users_check_word, message.peer_id, get_word_ans)
			await newState(message.peer_id, STATE_EX.STATE_EX_7_10)
	changeDict(users_points, message.peer_id, (did_t, cor_t))
	#except:
	#	await message.answer(message='Возникли проблемы, все починим в скором времени')
	#	await delState(message.peer_id)


@bot.on.private_message(func=lambda message: message.text.lower() != 'меню' and message.text.lower() != '[club187730402|@botaiege]')
async def hi_handler(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	await message.answer(message='{}, нажми кнопку меню'.format(users_info[0].first_name), keyboard=end_kb)

bot.run_forever()
