from random import shuffle, randint 
from pathlib import Path	
import sqlite3
import asyncio									
from vkbottle_types import BaseStateGroup
from vkbottle.bot import Bot, Message
from vkbottle import (
	Keyboard, 
	KeyboardButtonColor, 
	Text
	)



dir = Path('botvk.py').parent
token = '1eefd03cabef397c236c72b85a734fe05d3b73171a6dd9a01f4beb7c5c5aa6a08a814bbdbdcea81a23012'
bot = Bot(token=token)
chat_id = 2*10**9+1


conn = sqlite3.connect(r"C:\Users\ПК\Downloads\vk_bd2.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS vk_bd(
				peer_id INTEGER NOT NULL, 
				balance INTEGER NOT NULL)''')
conn = sqlite3.connect(r"C:\Users\ПК\Downloads\vk_bd2.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS vk_bd(
				peer_id INTEGER NOT NULL, 
				balance INTEGER NOT NULL)''')
conn.commit()


@bot.loop_wrapper.interval(seconds=86400)
async def repeated_task():
	await bot.api.messages.send(peer_id=chat_id, random_id=0, message='Пора ботать')



class user:
	def __init__(self, name, surname):
		self.busy = False
		self.words = []
		self.check_word = ''
		self.points = (-1, 0)
		self.name = name
		self.surname = surname

	def _change_kb(self, ll = [], bl = True):
		listOfButtons = []
		if bl:
			for i in ll:
				listOfButtons.append({"label": i, "type": "text", "color": "positive"})
			if len(listOfButtons) > 0:
				pp = [{"label": "СТОП", "type": "text", "color": 'negative'}, {"label": "ПРОРАБОТКА", "type": "text", "color": 'primary'}]
				self.keyboard = (Keyboard(one_time=False, inline=False)
									.schema([listOfButtons, pp])
									.get_json()
								)
			else:
				pp = [{"label": "СТОП", "type": "text", "color": 'negative'}, {"label": "ПРОРАБОТКА", "type": "text", "color": 'primary'}]
				self.keyboard = (Keyboard(one_time=False, inline=False)
									.schema([pp])
									.get_json()
								)
		else:
			for i in ll:
				fff = []
				fff.append({"label": i, "type": "text", "color": "positive"})
				listOfButtons.append(fff)
			if bl:
				pp = [{"label": "СТОП", "type": "text", "color": 'negative'}, {"label": "ПРОРАБОТКА", "type": "text", "color": 'primary'}]
			else:
				pp = [{"label": "СТОП", "type": "text", "color": 'negative'}]
			if len(listOfButtons) > 0:
				listOfButtons.append(pp)
				self.keyboard = (Keyboard(one_time=False, inline=False)
									.schema(listOfButtons)
									.get_json()
								)
			else:
				self.keyboard = (Keyboard(one_time=False, inline=False)
									.schema([pp])
									.get_json()
								)


users = dict()


bot_kb = (
	Keyboard(one_time=False, inline=True)
	.add(Text("5 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.add(Text("7 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.row()
	.add(Text("10 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.add(Text("14 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.row()
	.add(Text("15 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
	.add(Text("26 ЗАДАНИЕ"), color=KeyboardButtonColor.PRIMARY)
).get_json()

menu_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("РУССКИЙ ЯЗЫК"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("РЕЙТИНГ"), color=KeyboardButtonColor.PRIMARY)
).get_json()


end_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("МЕНЮ"), color=KeyboardButtonColor.PRIMARY)
).get_json()



class STATE_EX(BaseStateGroup):
	STATE_EX_7_10 = 710
	STATE_EX_7 = 7
	STATE_EX_14 = 14
	STATE_EX_PAR = 4
	STATE_EX_26 = 26



class STATE_MENU(BaseStateGroup):
	BOT_RUS = 0
	BOT_TASK = 1


async def newUser(peer_id, name, surname):
	if users.get(peer_id) != None:
		users.pop(peer_id)
	users.setdefault(peer_id, user(name, surname))

async def newState(peer_id, obj):
	await bot.state_dispenser.set(peer_id, obj)
	users.get(peer_id).busy = True

async def delState(peer_id):
	await bot.state_dispenser.delete(peer_id)
	users.get(peer_id).busy = False


def getRate():
	ll = []
	for i in users.keys():
		cursor.execute("""SELECT balance FROM vk_bd WHERE peer_id = (?)""", (i,))
		ll.append([str(users.get(i).name) + ' ' + users.get(i).surname, cursor.fetchone()[0]])
	return ll

def NewUser(peer_id):
	cursor.execute("""
					SELECT peer_id FROM vk_bd WHERE peer_id = (?)
					""", (peer_id,))
	if cursor.fetchone() is None:
		return True
	else:
		return False

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

def addBal(amount, peer_id):
	cursor.execute("""SELECT balance FROM vk_bd WHERE peer_id = (?)""", (peer_id,))
	oldBalance = cursor.fetchone()[0]
	cursor.execute("""UPDATE vk_bd 
					  SET balance = (?)
					  WHERE peer_id = (?)
					""", (oldBalance + amount, peer_id))
	conn.commit()


def getCords(s):
	cc = 0
	mincord = 100
	for i in range(len(s)):
		if s[i].isupper():
			cc += 1
			mincord = min(mincord, i)
	return (mincord, cc)

def get_ex26(href):
	with open(dir / href) as file:
		ansss = []
		for i in file.readlines():
			i = i.replace('\n', '')
			ans1 = []
			ans = i.split(':')
			ans1.append(ans[0])
			ans1.append(ans[1].split(';'))
			ansss.append(ans1)
	return ansss


def get_ex(href):
	with open(dir / href) as file:
		ans = []
		for i in file.readlines():
			inp = [x.strip() for x in i.split(';')]
			for x in inp:
				ans.append(x)
	return ans


def get_ex_par(href):
	with open(dir / href) as file:
		ansss = []
		for i in file.readlines():
			i = i.replace('(', '')
			i = i.replace(')', '')
			mas = [x.strip() for x in i.split('%')]
			for y in mas:
				ans = []
				para = [x.strip() for x in y.split('&')]
				titles = [x.strip() for x in para[0].split(':')]
				dicts = [x.strip() for x in para[1].split(':')]
				ans.append(titles)
				ans.append(dicts)
				ansss.append(ans)
		return ansss




def shuf(ll):  
	shuffle(ll)
	return ll


def get_word_par(ll):
	a = randint(0, len(ll) - 1)
	ans = ll[a]
	b = randint(0, len(ans[1]) - 1)
	c, v = ans[1][b], ans[0][b]
	m = ans[0].copy()
	del ans[1][b]
	del ans[0][b]
	if len(ans[0]) < 2: del ll[a]
	return m, c, v, ll


def get_word_26(ll):
	a = randint(0, len(ll) - 1)
	ans = ll[a]
	b = randint(0, len(ans[1]) - 1)
	c, v = ans[1][b], ans[0]
	del ans[1][b]
	if len(ans[1]) == 0: del ll[a]
	return c, v, ll



def get_word(ll):
	ans = ll[0]
	del ll[0]
	return ans, ll



@bot.on.message(func=lambda message: message.text.lower() == '!рейтинг')
async def hi_handler(message: Message):
	try:
		nes_list = getRate()
		nes_list.sort(key=lambda x: -x[1])
		str_bals = ''
		for i in range(len(nes_list)):
			str_bals += str(i+1) + '. ' + nes_list[i][0] + f' ({nes_list[i][1]})\n'
		await message.answer(message=str_bals)
	except:
		await message.answer(message='Рейтингу пизда')


@bot.on.private_message(func=lambda message: message.text.lower() == 'меню')
async def hi_handler(message: Message):
	if NewUser(message.from_id):
		cursor.execute("""INSERT INTO vk_bd
						  (peer_id, balance)
						  VALUES (?, ?)
							""", (message.from_id, 0))
		conn.commit()
	users_info = await bot.api.users.get(message.from_id)
	await newUser(message.peer_id, users_info[0].first_name, users_info[0].last_name)
	if message.text.lower() == 'меню':
		await message.answer(message=f'{users_info[0].first_name}, выбери раздел?', keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_RUS)




@bot.on.private_message(state=STATE_MENU.BOT_RUS)
async def hi_handler(message: Message):
	if message.text.lower() == 'русский язык':
		await message.answer(message='Выбери задание', keyboard=bot_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_TASK)
	elif message.text.lower() == 'рейтинг':
		nes_list = getRate()
		nes_list.sort(key=lambda x: -x[1])
		str_bals = ''
		for i in range(len(nes_list)):
			str_bals += str(i+1) + '. ' + nes_list[i][0] + f' ({nes_list[i][1]})\n'
		await message.answer(message=str_bals, keyboard=end_kb)
		await delState(message.peer_id)
	else:
		await message.answer(message='Такого раздела нет!', keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_RUS)



@bot.on.private_message(state = STATE_MENU.BOT_TASK)
async def hi_handler(message: Message):
	this_user = users.get(message.peer_id)
	if message.text.lower() == '10 задание':
		words = get_ex("ex10.txt")
		this_user.words = shuf(words)
		this_user._change_kb(['И', 'Е'])
		await do_ex10(message)
	elif message.text.lower() == '15 задание':
		words = get_ex("ex15.txt")
		this_user.words = shuf(words)
		this_user._change_kb(['Н', 'НН'])
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
		this_user._change_kb(['СЛИТНО', 'РАЗДЕЛЬНО'])
		await do_ex14(message)
	elif message.text.lower() == '26 задание':
		words = get_ex26("ex26.txt")
		this_user.words = shuf(words)
		this_user._change_kb(['ТРОПЫ', 'СИНТАКСИЧЕСКИЕ СРЕДСТВА', 'СТИЛИСТИЧЕСКИЕ ПРИЁМЫ', 'ЛЕКСИЧЕСКИЕ СРЕДСТВА'], False)
		await do_ex26(message)
	elif message.text.lower() == '5 задание':
		words = get_ex_par("exPar.txt")
		this_user.words = shuf(words)
		await do_exPar(message)
	else:
		await message.answer(message='Такого задания нет!')
		await bot.state_dispenser.set(message.peer_id, STATE_MENU.BOT_TASK)


@bot.on.private_message(state=STATE_EX.STATE_EX_7)
async def hi_handler(message: Message):
	this_user = users.get(message.peer_id)
	if message.text.lower() == "иментильный падеж, множ. число":
		words = get_ex("ex7(1).txt")
		this_user.words = shuf(words)
		this_user._change_kb(['А', 'Ы', 'Я', 'И'])
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
			await message.answer(message='Начнем:\n-----------------------------------\n' + secret_word(get_word_ans), keyboard=this_user.keyboard)
		else:
			if message.text.lower() =='стоп':
				did_t -= 1
				addBal(2*cor_t-did_t, message.peer_id)
				await delState(message.peer_id)
				await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
				if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота')
				elif did_t - cor_t == 0: await message.answer(message='Думаю, тут минимум 92 балла в формате ЕГЭ')
				elif did_t - cor_t < 3: await message.answer(message='Not bad')
				else:  
					if this_user.name == 'Илья': await message.answer(message='Даже не верится, что ты Илья 0_0')
					else: await message.answer(message='Ты не Илья, тебе можно')
			elif len(new_words) == 0:
				check_word = this_user.check_word
				cord_start, cord_end = getCords(check_word)
				cord_end += cord_start
				addBal(2*cor_t-did_t, message.peer_id)
				await delState(message.peer_id)
				if message.text.lower() == check_word[cord_start:cord_end].lower():
					cor_t += 1
					await message.answer(message='✅ Верно, ' + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:])
				else:
					await message.answer(message='❌ Неверно, '.upper() + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:])
				await message.answer(message=f'{this_user.name}, слова закончились. Твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
			else:
				check_word = this_user.check_word
				get_word_ans, new_words = get_word(new_words)
				this_user.words = new_words
				cord_start, cord_end = getCords(check_word)
				cord_end += cord_start
				if message.text.lower() =='проработка':
					addBal(2*cor_t-did_t, message.peer_id)
					await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t))
					new_words = new_words[cor_t - did_t:]
					shuffle(new_words)
					get_word_ans, new_words = get_word(new_words)
					this_user.words = new_words
					cord_start, cord_end = getCords(check_word)
					cord_end += cord_start
					did_t = 0
					cor_t = 0
					await message.answer(message='Повторим неправильно сделанные слова' + 
							'\n-----------------------------------\n' + secret_word(get_word_ans))
				elif message.text.lower() == check_word[cord_start:cord_end].lower():
						cor_t += 1
						await message.answer(message='✅ Верно, ' + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:] + 
							'\n-----------------------------------\n' + secret_word(get_word_ans))
				else:
					this_user.words.append(check_word)
					await message.answer(message='❌ Неверно, '.upper() + check_word[:cord_start] + check_word[cord_start:cord_end].upper() + check_word[cord_end:] + 
						'\n-----------------------------------\n' + secret_word(get_word_ans))
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
			await message.answer(message='Начнем:\n-----------------------------------\n' + secret_word(get_word_ans), keyboard=this_user.keyboard)
		else:
			if message.text.lower() =='стоп':
				did_t -= 1
				addBal(2*cor_t-did_t, message.peer_id)
				await delState(message.peer_id)
				await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
				if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота')
				elif did_t - cor_t == 0: await message.answer(message='Думаю, тут минимум 92 балла в формате ЕГЭ')
				elif did_t - cor_t < 3: await message.answer(message='Not bad')
				else:  
					if this_user.name == 'Илья': await message.answer(message='Даже не верится, что ты Илья 0_0')
					else: await message.answer(message='Ты не Илья, тебе можно')
			elif len(new_words) == 0:
				check_word = this_user.check_word
				cord_start, cord_end = getCords(check_word)
				cord_end += cord_start
				addBal(2*cor_t-did_t, message.peer_id)
				await delState(message.peer_id)
				if message.text.lower() == check_word[cord_start:cord_end].lower():
					cor_t += 1
					if 'СЛИТНО' in check_word:
						check_word = check_word.replace('СЛИТНО', '')
					else:
						check_word = check_word.replace('РАЗДЕЛЬНО', ' ')
					await message.answer(message='✅ Верно, ' + check_word)
				else:
					if 'СЛИТНО' in check_word:
						check_word = check_word.replace('СЛИТНО', '')
					else:
						check_word = check_word.replace('РАЗДЕЛЬНО', ' ')
					await message.answer(message='❌ Неверно, '.upper() + check_word)
				await message.answer(message=f'{this_user.name}, слова закончились. Твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
			else:
				check_word = this_user.check_word
				get_word_ans, new_words = get_word(new_words)
				this_user.words = new_words
				cord_start, cord_end = getCords(check_word)
				cord_end += cord_start
				if message.text.lower() =='проработка':
					addBal(2*cor_t-did_t, message.peer_id)
					await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t))
					new_words = new_words[cor_t - did_t:]
					shuffle(new_words)
					get_word_ans, new_words = get_word(new_words)
					this_user.words = new_words
					cord_start, cord_end = getCords(check_word)
					cord_end += cord_start
					did_t = 0
					cor_t = 0
					await message.answer(message='Повторим неправильно сделанные слова\n' + 
							'-----------------------------------\n' + secret_word(get_word_ans))
				elif message.text.lower() == check_word[cord_start:cord_end].lower():
					cor_t += 1
					if 'СЛИТНО' in check_word:
						check_word = check_word.replace('СЛИТНО', '')
					else:
						check_word = check_word.replace('РАЗДЕЛЬНО', ' ')
					await message.answer(message='✅ Верно, ' + check_word + 
						'\n-----------------------------------\n' + secret_word(get_word_ans))
				else:
					this_user.words.append(check_word)
					if 'СЛИТНО' in check_word:
						check_word = check_word.replace('СЛИТНО', '')
					else:
						check_word = check_word.replace('РАЗДЕЛЬНО', ' ')
					await message.answer(message='❌ Неверно, '.upper() + check_word + 
						'\n-----------------------------------\n' + secret_word(get_word_ans))
				this_user.check_word = get_word_ans
				await newState(message.peer_id, STATE_EX.STATE_EX_14)
		this_user.points = (did_t, cor_t)
	except:
		await message.answer(message='Возникли проблемы, все починим в скором времени')
		await delState(message.peer_id)






@bot.on.private_message(state=STATE_EX.STATE_EX_PAR)
async def do_exPar(message: Message):
	try:
		this_user = users.get(message.peer_id)
		points = this_user.points
		did_t = points[0]
		cor_t = points[1]
		did_t += 1
		new_words = this_user.words
		if this_user.busy == False:
			par_kb, get_word_ans, par_word, new_words = get_word_par(new_words) 
			this_user.words = new_words
			this_user.check_word = par_word
			await newState(message.peer_id, STATE_EX.STATE_EX_PAR)
			this_user._change_kb(par_kb, False)
			await message.answer(message='Начнем:\n-----------------------------------\n' + get_word_ans, keyboard=this_user.keyboard)
		else:
			if message.text.lower() =='стоп':
				did_t -= 1
				addBal(2*cor_t-did_t, message.peer_id)
				await delState(message.peer_id)
				await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
				if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота')
				elif did_t - cor_t == 0: await message.answer(message='Думаю, тут минимум 92 балла в формате ЕГЭ')
				elif did_t - cor_t < 3: await message.answer(message='Not bad')
				else:  
					if this_user.name == 'Илья': await message.answer(message='Даже не верится, что ты Илья 0_0')
					else: await message.answer(message='Ты не Илья, тебе можно')
			elif len(new_words) == 0:
				check_word = this_user.check_word
				addBal(2*cor_t-did_t, message.peer_id)
				await delState(message.peer_id)
				if message.text.lower() == check_word.lower():
					cor_t += 1
					await message.answer(message='✅ Верно')
				else:
					await message.answer(message='❌ Неверно, ' + check_word)
				await message.answer(message=f'{this_user.name}, слова закончились. Твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
			else:
				check_word = this_user.check_word
				par_kb, get_word_ans, par_word, new_words = get_word_par(new_words) 
				this_user.words = new_words
				this_user._change_kb(par_kb, False)
				if message.text.lower() == check_word.lower():
						cor_t += 1
						await message.answer(message='✅ Верно' + '\n-----------------------------------\n' + get_word_ans, keyboard=this_user.keyboard)
				else:
					await message.answer(message='❌ Неверно, '.upper() + check_word + '\n-----------------------------------\n' + get_word_ans, keyboard=this_user.keyboard)
				this_user.check_word = par_word
				await newState(message.peer_id, STATE_EX.STATE_EX_PAR)
		this_user.points = (did_t, cor_t)
	except:
		await message.answer(message='Возникли проблемы, все починим в скором времени')
		await delState(message.peer_id)



@bot.on.private_message(state=STATE_EX.STATE_EX_26)
async def do_ex26(message: Message):
	#try:
	this_user = users.get(message.peer_id)
	points = this_user.points
	did_t = points[0]
	cor_t = points[1]
	did_t += 1
	new_words = this_user.words
	if this_user.busy == False:
		get_word_ans, par_word, new_words = get_word_26(new_words) 
		this_user.words = new_words
		this_user.check_word = par_word
		await newState(message.peer_id, STATE_EX.STATE_EX_26)
		await message.answer(message='Начнем:\n-----------------------------------\n' + get_word_ans, keyboard=this_user.keyboard)
	else:
		if message.text.lower() =='стоп':
			did_t -= 1
			addBal(2*cor_t-did_t, message.peer_id)
			await delState(message.peer_id)
			await message.answer(message=f'{this_user.name}, твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
			if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота')
			elif did_t - cor_t == 0: await message.answer(message='Думаю, тут минимум 92 балла в формате ЕГЭ')
			elif did_t - cor_t < 3: await message.answer(message='Not bad')
			else:  
				if this_user.name == 'Илья': await message.answer(message='Даже не верится, что ты Илья 0_0')
				else: await message.answer(message='Ты не Илья, тебе можно')
		elif len(new_words) == 0:
			check_word = this_user.check_word
			addBal(2*cor_t-did_t, message.peer_id)
			await delState(message.peer_id)
			if message.text.lower() == check_word.lower():
				cor_t += 1
				await message.answer(message='✅ Верно')
			else:
				await message.answer(message='❌ Неверно, ' + check_word)
			await message.answer(message=f'{this_user.name}, слова закончились. Твой результат: ' + str(cor_t) + '/' + str(did_t), keyboard=end_kb)
		else:
			check_word = this_user.check_word
			get_word_ans, par_word, new_words = get_word_26(new_words) 
			this_user.words = new_words
			if message.text.lower() == check_word.lower():
					cor_t += 1
					await message.answer(message='✅ Верно' + '\n-----------------------------------\n' + get_word_ans, keyboard=this_user.keyboard)
			else:
				await message.answer(message='❌ Неверно, '.upper() + check_word + '\n-----------------------------------\n' + get_word_ans, keyboard=this_user.keyboard)
			this_user.check_word = par_word
			await newState(message.peer_id, STATE_EX.STATE_EX_26)
	this_user.points = (did_t, cor_t)
	#except:
	#	await message.answer(message='Возникли проблемы, все починим в скором времени')
	#	await delState(message.peer_id)




@bot.on.private_message(func=lambda message: message.text.lower() != 'меню' and message.text.lower() != '[club187730402|@botaiege]')
async def hi_handler(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	await message.answer(message='{}, нажми кнопку меню'.format(users_info[0].first_name), keyboard=end_kb)




bot.run_forever()
