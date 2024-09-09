
import discord
from discord.ext import commands
from discord import utils
from discord import message
from discord.utils import get
import ksconfig
import sqlite3
from ksconfig import settings

PREFIX = '!'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix = 'PREFIX', intents=intents)
config = ksconfig
bot.remove_command ('help')
connection = sqlite3.connect('server.db')
cursor = connection.cursor()

#Запуск бота--------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_ready():
	cursor.execute("""CREATE TABLE IF NOT EXISTS users (
		name TEXT,
		id INT,
		cash BIGINT,
		lvl INT
	)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS shop (
		role_id INT,
		guids_id INT,
		cost BIGINT
	)""")
	for guild in bot.guilds:
		for member in  guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id},0,1)")
			else:
				pass
	connection.commit()
	print('Авторизация {0.user} пройдена'.format(bot))
	await bot.change_presence( status = discord.Status.online, activity = discord.Game( 'Kitsunesland.ru' ) )

async def on_command_error( ctx, error ):
	print(error)

#Обработка новых участников--------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_member_join(member):
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}',{member.id},0,1)")
		connection.commit()
	else:
		pass

#Обработка сообщений--------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_message(message):
	if message.author.bot == False :
		await bot.process_commands( message ) #будут работать команды
		msg = message.content.lower()
		if msg == PREFIX + "привет":
			await message.channel.send( f'Привет **{message.author.mention}**, я бот {bot.user.mention}, чем я могу тебе помочь?\n Я могу посоветовать тебе ввести команду "!help" для разговора со мной.')
#неизвестная команда--------------------------------------------------------------------------------------------------------------------------------------
		elif PREFIX in msg and message.content.index(PREFIX) == 0:
			await message.channel.send("0_0 ? {} я тебя не понял, напиши команду '!help', чтобы узнать список моих команд".format(message.author.mention))
#фильтр слов--------------------------------------------------------------------------------------------------------------------------------------
		for i in ksconfig.фильтр: #ищет сообщение из списка
			if i in msg:  #сверяет 
				await message.delete() #Удаляет сообщение
				await message.author.send( f'{ message.author.mention }, сверив твой текст с моим фильтром, я удалил твоё сообщение из-за совподения определённых слов' )
	else:
		pass

#удаления чата--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.чистка )
@commands.has_permissions(administrator = True)

async def __clear( ctx, amount: int = 100 ):
	await ctx.channel.purge( limit = amount + 1 )
#	канал_настроек = client.get_channel( config.контроль )

#	await канал_настроек.send( embed = discord.Embed( description = f':white_check_mark: Удалено {len(кол_удал)} сообщений. С канала "{ctx.channel}" ', color=0xfff ) )
	


# Kick-----------------------------------------------------------------------------------------------------------------------------------------

@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def kick (ctx, member: discord.Member, *, reason = None):
	emb = discord.Embed (title = 'Kick :wave:', colour = discord.Color.red())
	await ctx.channel.purge(limit = 1)

	await member.kick(reason = reason)
	emb.set_author (name = member.name, icon_url = member.avatar_url)
	emb.add_field (name = 'Kick user', value = 'Kicked user : {}'.format(member.mention))
	emb.set_footer (text = 'Был выгнан с сервера администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)

	await ctx.send (embed = emb)

#Ban-------------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = config.блокирующие_слова)
@commands.has_permissions(administrator = True)

async def ban( ctx, member: discord.Member, *, reason = None ):
	await ctx.channel.purge( limit = 1 ) #сразу удаляет команду

	await member.ban( reason = reason )

	emb = discord.Embed( title = 'Отправлен в бан', colour = 0xb80606 )
	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = 'Нарушитель был наказан!', value = 'Нарушитель: {}'.format( member.mention ) )
	emb.set_footer( text = 'Отправитель {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
	emb.set_thumbnail( url ='https://cdn.discordapp.com/attachments/759863209967616001/760888524324208650/unnamed.jpg' ) #показывает картинку как иконку

	await ctx.send( embed = emb )

# Unban----------------------------------------------------------------------------------------------------------------------------------------

@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
	await ctx.channel.purge(limit = 1)
	emb = discord.Embed (title = 'Unban :unlock:', colour = discord.Color.purple())
	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban (user)
		emb.set_author (name = member.name, icon_url = member.avatar_url)
		emb.add_field (name = 'Unban user', value = 'Unbaned user : {}'.format(member.mention))
		emb.set_footer (text = 'Был разблокирован администратором {}'.format (ctx.author.name), icon_url = ctx.author.avatar_url)
		await ctx.send (embed = emb)
		return

#Проверка кошелька--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.бабки)
async def __balance(ctx, member: discord.Member = None):
	if member is None:
		await ctx.send(embed = discord.Embed(
			description = f"""Баланс **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}**"""
	))
	else:
		await ctx.send(embed = discord.Embed(
			description = f"""Баланс **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]}**"""
	))

#Наградить игрока--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.награда)
@commands.has_permissions(administrator = True)
async def __award(ctx, member: discord.Member = None, amount: int = None):
	if member is None:
		await ctx.send(f"**{ctx.author}**, укажите пользователя, которому желаете выдать награду!")
	else:
		if amount is None:
			await ctx.send(f"**{ctx.author}**, укажите сумму, которомую желаете выдать пользователю!")
		elif amount < 1:
			await ctx.send(f"**{ctx.author}** укажите сумму больше 1")
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
			connection.commit()

			await ctx.message.add_reaction('💰')

#Добавление роли в магазин--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.добавление)
@commands.has_permissions(administrator = True)
async def __add_shop(ctx,role: discord.Role =  None, cost: int = None):

	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете внести в магазин.")
	else:
		if cost is None:
			await ctx.send(f"**{ctx.author}**, укажите стоимость для новой роли.")
		elif cost < 0:
			await ctx.send(f"**{ctx.author}**, стоимость роли не можеть быть настолько маленькой.")
		else:
			cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
			connection.commit()

			await ctx.message.add_reaction('✔️')

#Удаление роли с магазина--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.удаление)
@commands.has_permissions(administrator = True)
async def __remove_shop(ctx, role: discord.Role = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль, которую желаете удалить из магазина")
	else:
		cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
		connection.commit()

		await ctx.message.add_reaction('✔️')

#Очистка всего магазина--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.лист1)
@commands.has_permissions(administrator = True)
async def __rs_all(ctx):
	cursor.execute("DELETE FROM shop")
	connection.commit()

	await ctx.message.add_reaction('✔️')

#Магазин--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.магазин)
async def __shop(ctx):
	embed = discord.Embed(title = 'Магазин ролей:')

	for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
		if ctx.guild.get_role(row[0]) != None:
			embed.add_field(
				name = f"Стоимость {row[1]}",
				value = f"Вы приобретёте роль {ctx.guild.get_role(row[0]).mention}",
				inline = False
			)
		else:
			pass
	await ctx.send(embed = embed)

#Покупка в магазине--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.покупка)
async def __buy(ctx, role: discord.Role = None):
	if role is None:
		await ctx.send(f"**{ctx.author}**, укажите роль, которую желаете приобрести.")
	else:
		if role in ctx.author.roles:
			await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль.")
		elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.author(f"**{ctx.author}**, у вас недостаточно средств для приобретения данной роли.")
		else:
			await ctx.author.add_role(role)
			cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
			connection.commit()
			
			await ctx.message.add_reaction('✔️')

# Оштрафовать игрока--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.штраф)
@commands.has_permissions(administrator = True)
async def __take(ctx, member: discord.Member = None, amount = None):
	s1 = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
	if member is None:
		await ctx.send(f"**{ctx.author}**, укажите пользователя, которого желаете оштрафовать!")
	else:
		if amount is None:
			await ctx.send(f"**{ctx.author}**, укажите сумму, которомую желаете забрать у пользователя!")
		elif amount == 'all':
			cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
			connection.commit()

			await ctx.message.add_reaction('💸')
		elif int(amount) > s1:
			await ctx.send("сумма превышает баланс **{}**, пользователя **{}**".format(s1, member))
		elif int(amount) < 1:
			await ctx.send(f"**{ctx.author}** укажите сумму больше 1")
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
			connection.commit()

			await ctx.message.add_reaction('💸')
# help----------------------------------------------------------------------------------------------------------------------------------------

@bot.command(aliases = ksconfig.помощь)
async def help(ctx):
	await ctx.channel.purge(limit = 1)
	emb = discord.Embed (title = 'Навигация по командам :clipboard: ')
	emb.add_field(name ='Описание сервера', value = 'Это сервер Kitsunesland. Его владелецы - "Первородные лисы".\n Я же бот написанный автором maFioza.')
	emb.add_field(name ='{}balance 💳'.format(PREFIX), value = 'Проверить баланс, при указании игрока проверяетя его баланс')
	emb.add_field(name ='{}shop 🛒'.format(PREFIX), value = 'Список ролей, которые можно приобрести')
	emb.add_field(name ='{}buy 💵'.format(PREFIX), value = 'Покупка роли из магазина')
	await ctx.send ( embed = emb )

# mute--------------------------------------------------------------------------------------------------------------------------------------

@bot.command(sum = ksconfig.молчанка)
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, срок_ч : float = 1 ): #команда и @человек
	await ctx.channel.purge( limit = 1 ) #сразу удаляет команду
	роль_mute = discord.utils.get( ctx.message.guild.roles, id = ksconfig.мут ) #ищет роль на сервере
	await member.add_roles( роль_mute ) #говорит что "хотим добавить участнику роль"
	emb = discord.Embed( title = 'Чат у пользователя {0.user} заблокирован'.format(user), colour = 0x1111)
	emb.set_author( name = member.name, icon_url = member.avatar_url )
	emb.add_field( name = f'Заблокирован чат на {срок_ч}ч', value = 'Muted  {}'.format( member.mention ), colour = 0x10000)
	emb.set_footer( text = 'Был выдан мут администратором:{}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
	emb.set_thumbnail( url ='https://cdn.discordapp.com/attachments/705220828043673642/714456107149688842/9_1_1.png' ) #показывает картинку как иконку
	await ctx.send( embed = emb )
	await asyncio.sleep(срок_ч*60*60)
	await member.remove_roles(роль_mute)
	emb2 = discord.Embed( title = '', colour = 0x8ad4d4)
	emb2.set_author( name = member.name, icon_url = member.avatar_url )
	emb2.add_field( name = f'Мут со сроком {срок_ч}ч окончен', value = ' Unmuted : {}'.format( member.mention ), colour = 0x10000)
	emb2.set_footer( text = 'Не нарушай больше правила!' )
	emb2.set_thumbnail( url ='https://cdn.discordapp.com/attachments/705220828043673642/718439769222152204/1_1.png' ) #показывает картинку как иконку
	await ctx.send( embed = emb2 )

#сбои команд--------------------------------------------------------------------------------------------------------------------------------------

@__clear.error
async def clear_error(ctx,error):
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')
@ban.error
async def ban_eror(ctx,error):
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')
@kick.error
async def kick_error(ctx,error):
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')
@mute.error
async def mute_error(ctx,error):
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')
@unban.error
async def unban_error(ctx,error):
	if isinstance (error, commands.MissingRequiredArgument):
		await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент без @!')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')

# эмоция выдача ролей--------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_raw_reaction_add(payload):
	if payload.message_id == ksconfig.POST_ID: # id поста с которого будут считываться реакции
		channel = bot.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
	try:
		emoji = str(payload.emoji) # эмоджик который выбрал юзер
		role = utils.get(message.guild.roles, id=ksconfig.ROLES[emoji]) # объект выбранной роли (если есть)
		if(len([i for i in member.roles if i.id not in ksconfig.EXCROLES]) <= ksconfig.MAX_ROLES_PER_USER):
			await member.add_roles(role)
			print('[SUCCESS] Игроку{0.display_name}, выдана роль {1.name}'.format(member, role))
		else:
			await message.remove_reaction(payload.emoji, member)
			print('[ERROR] Слишком много ролей для пользователя {0.display_name}'.format(member))
	except KeyError as e:
		print('[ERROR] KeyError, роль не найдена для ' + emoji)
	except Exception as e:
		print(repr(e))

# эмоция убирания ролей--------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_raw_reaction_remove(payload):
	if payload.message_id == ksconfig.POST_ID: # id поста с которого будут считываться реакции
		channel = bot.get_channel(payload.channel_id) # получаем объект канала
		message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
		member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
	try:
		emoji = str(payload.emoji) # эмоджик который выбрал юзер
		role = utils.get(message.guild.roles, id=ksconfig.ROLES[emoji]) # объект выбранной роли (если есть)
		await member.remove_roles(role)
		print('[SUCCESS] Роль {1.name}, убрана у игрока {0.display_name}'.format(member, role))
	except KeyError as e:
		print('[ERROR] KeyError, роль не найдена для ' + emoji)
	except Exception as e:
		print(repr(e))

# Connect--------------------------------------------------------------------------------------------------------------------------------------
bot.run(ksconfig.SAVE)  #Запускаем бота Discord по токену