# -*- coding: utf-8 -*-
from random import shuffle, randint 
import asyncio
from vkbottle_types import BaseStateGroup
from vkbottle.bot import Bot, Message     									# python C:\Users\ПК\Downloads\lalala.py
from vkbottle import (
	Keyboard, 
	KeyboardButtonColor, 
	Text
	)



token = '29b86ae229fc76a29a88408f1f6277e959824731bd9f2b266c51ea41e6ac99cfae10310a761a532b3356e'
bot = Bot(token=token)

class menu(BaseStateGroup):
	MENU_RUS = 3




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


class botat(BaseStateGroup):
	BOT_RUS = 0
	BOT_TASKS = 1
	BOT_PRORAB = 2
	BOT_TASKS7 = 4






ex7 = """инструкторы 
редакторы 
лекторы
ректоры 
конструкторы 
прожекторы 
секторы 
инженеры 
шофёры
бухгалтеры
диспетчеры
договоры
приговоры
плейеры
драйверы
грифели
госпитали
векселя
вензеля
кителя
штабеля
штемпеля
тополя
шомпола
колокола
купола
слесари
токари
конюхи
возрасты
кремы
супы
грунты
лифты
порты
склады
торты
флоты
фронты
штабы
штурманы
адреса
бока
борта
века
желоба
жемчуга
ботинок
чулок
шаровар
шорт
туфель
сапог
тапок
тапочек
галош
бахил
бутс
валенок
манжет
серёг
клипс
носков
гольфов
рельсов
бронхов
джинсов
лампасов
бриджей
блюдец
зеркалец
копытец(копытцев)
одеялец
полотенец
сердец
солнц
болотцев
кружевцев 
деревцев
оконцев
апельсинов
бананов
огурцов
бананов
томатов
помидоров
гранатов
абрикосов
ананасов
лимонов
мандаринов
баклажанов
жернова
края
кузова
окорока
округа
острова
отпуска
паруса
паспорта
погреба
потроха
снега
стога
сорта
сторожа
тетерева
черепа
директора
профессора
инспектора
доктора
катера
ордера
тенора
фельдшера
флюгера
хутора
шулера
буфера
веера
буера
яблок
груш
слив
дынь
повара
принтеры""".split()







line1 = 'приоритет, привилегия, прибаутка, привередливый, пригожий, прибор, приличия, пристойно, приесться, приказ, приключения, прикорнуть, присяга, притеснять, причина, причуда, притязание, природа, пример, прическа, прискорбно, приволье, прицел, примета, приверженец, прилежный, причиндалы, приятный, приватный, принцип, примат, примитив, пригодный, присниться, приключение, присудить, призвание, присмотреть, приспособить, прерогатива, преамбула, препятствие, препоны, прерия, презент, преимущество, преисподняя, прегрешения, пренебрегать, прекословить, препираться, престол, превратный, знак_препинания, пресловутый, прельстить, преследовать, преподаватель, преподнести, препроводить, преподобный, пресмыкаться, препарировать, прелюдия, премьера, престиж, президент, претензия, презумпция, превентивный, прелат, превалировать, президиум, претендент, преферанс, прецедент, препарат, преодолеть'
txt = """
прибывать(приезжать) - пребывать(находиться);
призреть(приютить,позаботиться) - презреть(пренебречь);
притворить(закрыть) - претворить(воплотить);
приклонить(наклонить) - преклонить(выразить_уважение,вызывающий_уважение);
придать(добавить) - предать(предаться,_выдать);
приходящий(являющийся) -  преходящий(временный);
притерпеться(привыкнуть) -  претерпеть(пережить);
приемник(радио) - преемник(ученик);
приставить(поставить_к_чему-либо) - преставиться(умереть);
привратник(сторож) - превратности (неприятности);
приложить(положить_вплотную) - непреложный(незыблемый,_нерушимый);
придел(пристройка_в_церкви) - предел(граница);""".split(';')




wr_words = []
stop = False
did_t = -2
cor_t = 0
NOWWORD = 'прилежный'
pror_words = []
pror_words_new = []


for i in txt:
	a = i.replace('-', '')
	a = a.split()
	try:
		wr_words.append(a[0])
		wr_words.append(a[1])
	except:
		pass
line1 = line1.replace(',', '')
b = line1.split()
for i in b:
	wr_words.append(i)
words = []
words7 = []

def send_task7():
	global words7
	ans = words7[0]
	del words7[0]
	return ans

async def do_task7():
	global words7
	global ex7
	shuffle(ex7)
	words7 = ex7


def send_task_pror7():
	global pror_words
	k = randint(0, len(pror_words) - 1)
	ans = pror_words[k]
	del pror_words[k]
	return ans



def send_task():
	global words
	ans = words[0]
	del words[0]
	return ans

def send_task_pror():
	global pror_words
	k = randint(0, len(pror_words) - 1)
	ans = pror_words[k]
	del pror_words[k]
	return ans


async def do_task():
	global words
	global wr_words
	shuffle(wr_words)
	words = wr_words


@bot.on.message(func=lambda message: message.text.lower() == 'меню' or message.text.lower() == '[club187730402|@darowanoga]')
async def hi_handler(message: Message):
	if message.text.lower() == 'меню':
		users_info = await bot.api.users.get(message.from_id)
		await message.answer(message='{}, выбери раздел?'.format(users_info[0].first_name), keyboard=menu_kb)
		await bot.state_dispenser.set(message.peer_id, menu.MENU_RUS)
	elif message.text.lower() == '[club187730402|@darowanoga]':
		await message.answer(message='Отъебись'.format(users_info[0].first_name))






@bot.on.message(state=menu.MENU_RUS)
async def hi_handler(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	await message.answer(message='{}, нужно. Выбери задание'.format(users_info[0].first_name), keyboard=bot_kb)
	await bot.state_dispenser.delete(message.peer_id)
	await bot.state_dispenser.set(message.peer_id, botat.BOT_RUS)





tasks_kb = (
	Keyboard(one_time=True, inline=False)
	.add(Text("И"), color=KeyboardButtonColor.POSITIVE)
	.add(Text("Е"), color=KeyboardButtonColor.POSITIVE)
	.row()
	.add(Text("СТОП"), color=KeyboardButtonColor.NEGATIVE)
	.add(Text("ПРОРАБОТКА"), color=KeyboardButtonColor.PRIMARY)
	.get_json()
)



@bot.on.message(state = botat.BOT_RUS)
async def hi_handler(message: Message):
	global did_t
	global cor_t
	global NOWWORD
	global pror_words
	global pror_words_new
	if message.text == '[club187730402|@darowanoga] 10 ЗАДАНИЕ' or message.text == '10 ЗАДАНИЕ':
		pror_words = []
		pror_words_new = []
		did_t = -1
		cor_t = 0
		await message.answer(message='Начнем:')
		await do_task()
		NOWWORD = send_task()
		new_i = NOWWORD[:2] + '_' + NOWWORD[3:]
		await message.answer(message='Слово: ' + new_i, keyboard=tasks_kb)
		await message.answer(message='----------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS)
	elif message.text == '[club187730402|@darowanoga] 7 ЗАДАНИЕ' or message.text == '7 ЗАДАНИЕ':
		pror_words = []
		pror_words_new = []
		did_t = -1
		cor_t = 0
		await message.answer(message='Начнем:')
		await do_task7()
		NOWWORD = send_task7()
		new_i = NOWWORD[:-2] + '__'
		await message.answer(message='Слово: ' + new_i, keyboard=tasks_kb)
		await message.answer(message='----------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS7)
	else:
		await message.answer(message='долбаеб?')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_RUS)



@bot.on.message(state = botat.BOT_TASKS)
async def hi_handler(message: Message):
	global did_t
	global cor_t
	global NOWWORD
	global stop
	global pror_words
	new_word = NOWWORD
	did_t += 1
	if message.text.lower() == new_word[2] or message.text.lower() == '[club187730402|@darowanoga] ' + new_word[2]:
		cor_t += 1
		await message.answer(message='✅ Верно, ' + new_word[:2] + new_word[2].upper() + new_word[3:])
		await message.answer(message='----------------------------------')
		await asyncio.sleep(0.5)
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS)
	elif message.text.lower() == '[club187730402|@darowanoga] стоп' or message.text.lower() =='стоп':
		await message.answer(message='Результат: ' + str(cor_t) + '/' + str(did_t))
		if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота...')
		elif did_t - cor_t == 0: await message.answer(message='Минимум 92 будет')
		elif did_t - cor_t < 3: await message.answer(message='Заебись, конечно, но, чел, егэ через 0 дней.....')
		else:  await message.answer(message='Чел, проспись а..............')
		await bot.state_dispenser.delete(message.peer_id)
		stop = True
	elif message.text.lower() == '[club187730402|@darowanoga] проработка' or message.text.lower() =='проработка':
		NOWWORD = send_task_pror()
		new_i = NOWWORD[:2] + '_' + NOWWORD[3:]
		await message.answer(message='Слово: ' + new_i, keyboard=tasks_kb)
		await message.answer(message='---------------------------------')
		await bot.state_dispenser.delete(message.peer_id)
		await bot.state_dispenser.set(message.peer_id, botat.BOT_PRORAB)
		stop = True
	else:
		pror_words.append(new_word)
		await message.answer(message='❌ Неверно, '.upper() + new_word[:2] + new_word[2].upper() + new_word[3:])
		await message.answer(message='----------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS)
	if stop == False:
		NOWWORD = send_task()
		new_i = NOWWORD[:2] + '_' + NOWWORD[3:]
		await message.answer(message='Слово: ' + new_i, keyboard=tasks_kb)
	else:
		stop = False



@bot.on.message(state=botat.BOT_PRORAB)
async def hi_handler(message: Message):
	global NOWWORD
	global stop
	global pror_words
	global pror_words_new
	new_word = NOWWORD
	if len(pror_words) < 1:
		await message.answer(message='Удачи на экзамене!')
		await bot.state_dispenser.delete(message.peer_id)
		stop = True
	if message.text.lower() == new_word[2]:
		await message.answer(message='✅ Верно, ' + new_word[:2] + new_word[2].upper() + new_word[3:])
		await message.answer(message='---------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS)
	elif message.text.lower() == '[club187730402|@darowanoga] стоп' or message.text.lower() =='стоп':
		await message.answer(message='Удачи на экзамене!')
		await bot.state_dispenser.delete(message.peer_id)
		stop = True
	elif message.text.lower() == '[club187730402|@darowanoga] проработка' or message.text.lower() =='проработка':
		pror_words = pror_words_new
		NOWWORD = send_task_pror()
		new_i = NOWWORD[:2] + '_' + NOWWORD[3:]
		await message.answer(message='Слово: ' + new_i, keyboard=tasks_kb)
		await message.answer(message='----------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_PRORAB)
	else:
		pror_words_new.append(new_word)
		await message.answer(message='❌ Неверно, '.upper() + new_word[:2] + new_word[2].upper() + new_word[3:])
		await message.answer(message='----------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS)

	if stop == False:
		NOWWORD = send_task_pror()
		new_i = NOWWORD[:2] + '_' + NOWWORD[3:]
		await message.answer(message='Слово: ' + new_i, keyboard=tasks_kb)
	else:
		stop = False




@bot.on.message(state = botat.BOT_TASKS7)
async def hi_handler(message: Message):
	global did_t
	global cor_t
	global NOWWORD
	global stop
	global pror_words
	new_word = NOWWORD
	did_t += 1
	if message.text.lower() == new_word[-2:] or message.text.lower() == '[club187730402|@darowanoga] ' + new_word[-2:]:
		cor_t += 1
		await message.answer(message='✅ Верно, ' + new_word[:-2] + new_word[-2:].upper())
		await message.answer(message='----------------------------------')
		await asyncio.sleep(0.5)
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS)
	elif message.text.lower() == '[club187730402|@darowanoga] стоп' or message.text.lower() =='стоп':
		await message.answer(message='Результат: ' + str(cor_t) + '/' + str(did_t))
		if did_t - cor_t == 1: await message.answer(message='Спишем на брак бота...')
		elif did_t - cor_t == 0: await message.answer(message='Минимум 92 будет')
		elif did_t - cor_t < 3: await message.answer(message='Заебись, конечно, но, чел, егэ через 0 дней.....')
		else:  await message.answer(message='Чел, проспись а..............')
		await bot.state_dispenser.delete(message.peer_id)
		stop = True
	elif message.text.lower() == '[club187730402|@darowanoga] проработка' or message.text.lower() =='проработка':
		NOWWORD = send_task_pror()
		new_i = NOWWORD[:-2] + '__'
		await message.answer(message='Слово: ' + new_i)
		await message.answer(message='---------------------------------')
		await bot.state_dispenser.delete(message.peer_id)
		await bot.state_dispenser.set(message.peer_id, botat.BOT_PRORAB)
		stop = True
	else:
		pror_words.append(new_word)
		await message.answer(message='❌ Неверно, '.upper() + new_word[:-2] + new_word[-2:].upper())
		await message.answer(message='----------------------------------')
		await bot.state_dispenser.set(message.peer_id, botat.BOT_TASKS)
	if stop == False:
		NOWWORD = send_task()
		new_i = NOWWORD[:-2] + '__'
		await message.answer(message='Слово: ' + new_i)
	else:
		stop = False



bot.run_forever()
