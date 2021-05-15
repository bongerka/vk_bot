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
	try:
		for i in users.keys():
			await bot.api.messages.send(peer_id=i, random_id=0, message='Пора ботать')
	except:
		await bot.api.messages.send(peer_id=chat_id, random_id=0, message='Пора ботать')
		



class user:
	def __init__(self, name):
		self.busy = False
		self.words = []
		self.check_word = ''
		self.points = (-2, 0)
		self.name = name

	def _change_kb(self, *args):
		listOfButtons = []
		for i in args:
			listOfButtons.append({"label": i, "type": "text", "color": "positive"})
		if len(listOfButtons):
			self.keyboard = (Keyboard(one_time=False, inline=False)
								.schema(
								    [
								        listOfButtons,
								        [
									        {"label": "СТОП", "type": "text", "color": 'negative'},
									        {"label": "ПРОРАБОТКА", "type": "text", "color": 'primary'}
								        ],
								    ]
								)
								.get_json()
							)
		else:
			self.keyboard = (Keyboard(one_time=False, inline=False)
					.schema(
					    [
					        [
						        {"label": "СТОП", "type": "text", "color": 'negative'},
						        {"label": "ПРОРАБОТКА", "type": "text", "color": 'primary'}
					        ],
					    ]
					)
					.get_json()
				)


users = dict()


bot_kb = (
	Keyboard(one_time=False, inline=True)
	.add(Text("7 ЗАДАНИЕ"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("10 ЗАДАНИЕ"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("14 ЗАДАНИЕ"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("15 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
).get_json()

menu_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("РУССКИЙ ЯЗЫК"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("ДОБАВЛЕНИЕ СЛОВ"), color=KeyboardButtonColor.PRIMARY)
).get_json()


end_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("МЕНЮ"), color=KeyboardButtonColor.PRIMARY)
).get_json()



class STATE_EX(BaseStateGroup):
	STATE_EX_7_10 = 710
	STATE_EX_7 = 7
	STATE_EX_14 = 14



class STATE_MENU(BaseStateGroup):
	BOT_RUS = 0
	BOT_TASK = 1


async def newUser(peer_id, name):
	if users.get(peer_id) != None:
		users.pop(peer_id)
	users.setdefault(peer_id, user(name))

async def newState(peer_id, obj):
	await bot.state_dispenser.set(peer_id, obj)
	users.get(peer_id).busy = True

async def delState(peer_id):
	await bot.state_dispenser.delete(peer_id)
	users.get(peer_id).busy = False


def secret_word(s):
	if s.islower():
		return 'в слове ' + s + ' нет больших букв'
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


def get_ex(href):
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



@bot.on.private_message(func=lambda message: message.text.lower() == 'меню')
async def hi_handler(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	await newUser(message.peer_id, users_info[0].first_name)
	if message.text.lower() == 'меню':
		await message.answer(message=f'{users_info[0].first_name}, выбери раздел?', keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_RUS)




@bot.on.private_message(state=STATE_MENU.BOT_RUS)
async def hi_handler(message: Message):
	if message.text.lower() == 'русский язык':
		await message.answer(message='Выбери задание (зеленые готовы)', keyboard=bot_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_TASK)
	else:
		await message.answer(message='Еще не готово :(', keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_RUS)




@bot.on.private_message(state = STATE_MENU.BOT_TASK)
async def hi_handler(message: Message):
	this_user = users.get(message.peer_id)
	if message.text.lower() == '10 задание':
		words = get_ex("ex10.txt")
		this_user.words = shuf(words)
		this_user._change_kb('И', 'Е')
		await do_ex10(message)
	elif message.text.lower() == '7 задание':
		await message.answer(message='Выберите форму слов', 
			keyboard=(Keyboard(one_time=False, inline=True)
						.add(Text("Иментильный падеж, множ. число"), color=KeyboardButtonColor.PRIMARY)
						.row()
						.add(Text("Родительный падеж, множ. число"), color=KeyboardButtonColor.PRIMARY)
					  ).get_json())
		await bot.state_dispenser.set(message.peer_id, STATE_EX.STATE_EX_7)
	elif message.text.lower() == '14 задание':
		words = get_ex("ex14.txt")
		this_user.words = shuf(words)
		this_user._change_kb('СЛИТНО', 'РАЗДЕЛЬНО')
		await do_ex14(message)
	else:
		await message.answer(message='Еще не готово, выберите другое задание')
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_TASK)


@bot.on.private_message(state=STATE_EX.STATE_EX_7)
async def hi_handler(message: Message):
	this_user = users.get(message.peer_id)
	if message.text.lower() == "иментильный падеж, множ. число":
		words = get_ex("ex7(1).txt")
		this_user.words = shuf(words)
		this_user._change_kb('А', 'Ы', 'Я', 'И')
		await do_ex10(message)
	elif message.text.lower() == "родительный падеж, множ. число":
		words = get_ex("ex7(2).txt")
		this_user.words = shuf(words)
		this_user._change_kb()
		await do_ex10(message)
	else:
		await message.answer(message='Выберите другое задание')
		await bot.state_dispenser.set(message.peer_id, STATE_EX.STATE_EX_7)

@bot.on.private_message(state=STATE_EX.STATE_EX_7_10)
async def do_ex10(message: Message):
	try:
		this_user = users.get(message.peer_id)
		points = this_user.points
		did_t = points[0]
		cor_t = points[1]
		did_t += 1
		new_words = this_user.words
		if this_user.busy == False:
			get_word_ans, new_words = get_word(new_words) 
			this_user.words = new_words
			this_user.check_word = get_word_ans
			await newState(message.peer_id, STATE_EX.STATE_EX_7_10)
			await message.answer(message='Начнем:\n----------------------------------------\n' + secret_word(get_word_ans), keyboard=this_user.keyboard)
		else:
			if message.text.lower() =='стоп' or len(new_words) == 0:
				await delState(message.peer_id)
				await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
				if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота')
				elif did_t - cor_t == 0: await message.answer(message='Думаю, тут минимум 92 балла в формате ЕГЭ')
				elif did_t - cor_t < 3: await message.answer(message='Not bad')
				else:  
					if this_user.name == 'Илья': await message.answer(message='Даже не верится, что ты Илья 0_0')
					else: await message.answer(message='Ты не Илья, тебе можно')
			elif message.text.lower() =='проработка':
				await message.answer(message='Бигбой не успел сделать')
				await delState(message.peer_id)
				await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t))
			else:
				check_word = this_user.check_word
				get_word_ans, new_words = get_word(new_words)
				this_user.words = new_words
				cord_start, cord_end = getCords(check_word)
				cord_end += cord_start
				if message.text.lower() == check_word[cord_start:cord_end].lower():
					cor_t += 1
					await message.answer(message='✅ Верно, ' + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:] + 
						'\n----------------------------------------\n' + secret_word(get_word_ans))
				else:
					await message.answer(message='❌ Неверно, '.upper() + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:] + 
						'\n----------------------------------------\n' + secret_word(get_word_ans))
				this_user.check_word = get_word_ans
				await newState(message.peer_id, STATE_EX.STATE_EX_7_10)
		this_user.points = (did_t, cor_t)
	except:
		await message.answer(message='Возникли проблемы, все починим в скором времени')
		await delState(message.peer_id)


@bot.on.private_message(state=STATE_EX.STATE_EX_14)
async def do_ex14(message: Message):
	try:
		this_user = users.get(message.peer_id)
		points = this_user.points
		did_t = points[0]
		cor_t = points[1]
		did_t += 1
		new_words = this_user.words
		if this_user.busy == False:
			get_word_ans, new_words = get_word(new_words) 
			this_user.words = new_words
			this_user.check_word = get_word_ans
			await newState(message.peer_id, STATE_EX.STATE_EX_14)
			await message.answer(message='Начнем:\n----------------------------------------\n' + secret_word(get_word_ans), keyboard=this_user.keyboard)
		else:
			if message.text.lower() =='стоп' or len(new_words) == 0:
				await delState(message.peer_id)
				await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
				if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота')
				elif did_t - cor_t == 0: await message.answer(message='Думаю, тут минимум 92 балла в формате ЕГЭ')
				elif did_t - cor_t < 3: await message.answer(message='Not bad')
				else:  
					if this_user.name == 'Илья': await message.answer(message='Даже не верится, что ты Илья 0_0')
					else: await message.answer(message='Ты не Илья, тебе можно')
			elif message.text.lower() =='проработка':
				await message.answer(message='Бигбой не успел сделать')
				await delState(message.peer_id)
				await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t))
			else:
				check_word = this_user.check_word
				get_word_ans, new_words = get_word(new_words)
				this_user.words = new_words
				cord_start, cord_end = getCords(check_word)
				cord_end += cord_start
				if message.text.lower() == check_word[cord_start:cord_end].lower():
					cor_t += 1
					if 'СЛИТНО' in check_word:
						check_word = check_word.replace('СЛИТНО', '')
					else:
						check_word = check_word.replace('РАЗДЕЛЬНО', ' ')
					await message.answer(message='✅ Верно, ' + check_word + 
						'\n----------------------------------------\n' + secret_word(get_word_ans))
				else:
					if 'СЛИТНО' in check_word:
						check_word = check_word.replace('СЛИТНО', '')
					else:
						check_word = check_word.replace('РАЗДЕЛЬНО', ' ')

					await message.answer(message='❌ Неверно, '.upper() + check_word + 
						'\n----------------------------------------\n' + secret_word(get_word_ans))
				this_user.check_word = get_word_ans
				await newState(message.peer_id, STATE_EX.STATE_EX_14)
		this_user.points = (did_t, cor_t)
	except:
		await message.answer(message='Возникли проблемы, все починим в скором времени')
		await delState(message.peer_id)



@bot.on.private_message(func=lambda message: message.text.lower() != 'меню' and message.text.lower() != '[club187730402|@botaiege]')
async def hi_handler(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	await message.answer(message='{}, нажми кнопку меню'.format(users_info[0].first_name), keyboard=end_kb)

bot.run_forever()
