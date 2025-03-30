import discord
from discord.ext import commands
import asyncio
from sheets import get_data  # Импорт функции получения данных

TOKEN = "MTM1NTg3MjkxOTA2NjI1MTMzNA.Gq1mVU.0BxJ4qHoXbwNJRkv8lmlIh_OaPM1YwxlF0KVzc"  # Замените на ваш токен
GUILD_ID = 833611339502321665  # ID вашего сервера
DEFAULT_ROLE = 833709801833758792  # ID роли, которую бот будет выдавать всем

intents = discord.Intents.default()
intents.members = True  # Нужно для управления ролями

bot = commands.Bot(command_prefix="!", intents=intents)

async def update_roles():
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)

    if guild is None:
        print("❌ Ошибка: Сервер не найден!")
        return

    while not bot.is_closed():
        print("🔄 Обновление ролей...")

        data = get_data()  # Получаем список пользователей
        for row in data:
            if len(row) < 1:  # Проверяем, что строка не пустая
                print(f"⚠ Пропущена пустая строка: {row}")
                continue

            username = row[0]  # Получаем имя пользователя

            # Поиск пользователя по имени
            member = discord.utils.find(lambda m: m.name == username, guild.members)
            if member is None:
                print(f"⚠ Пользователь {username} не найден!")
                continue

            # Поиск роли по ID
            role = guild.get_role(DEFAULT_ROLE)
            if role is None:
                print(f"⚠ Роль с ID {DEFAULT_ROLE} не найдена!")
                continue

            # Выдача роли
            if role not in member.roles:
                await member.add_roles(role)
                print(f"✅ {username} получил роль {role.name}")

        await asyncio.sleep(60)  # Обновление каждые 60 секунд

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} подключен!")
    bot.loop.create_task(update_roles())

bot.run(TOKEN)
