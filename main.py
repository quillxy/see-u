from telethon import TelegramClient, events
from telethon.tl.types import UserStatusOnline, UserStatusOffline
from telethon import errors
import asyncio
import datetime
import os
import colorama
from colorama import init, Fore  
import requests
from db import connect_bd, insert_history, get_history

#скрипт взял у @KanareykaXD и переписал немного

colorama.init(autoreset=True)


def ip():
    api = "http://ip-api.com/json/?fields=query,country"
    data = requests.get(api).json()
    ip = f"Ip: {data['query']}"
    return ip
  


def time():
    now = datetime.datetime.now()
    time = now.strftime('%H:%M:%S')
    return time

ip = ip()
time = time()

banner = f"""
░░░░░░▄▄▄▄███▄▄▄▄░░░░░░░░░░░░░              
░░░▄▄█▀░░░░░░░░░▀▀▄▄░░░░░░░░░░              
░░█▀░░░░░░░░░░░░░░░▀█▄░░░░░░░░
░█▀░░░░░░░░░░░░░░░░░░█▄░░░░░░░
██░░░░░░░░░░░░░░░░░░░░█▄░░░░░░
█░░░░░░░░░░░░░░░░░░░░░░█▄░░░░░
██░░░░░░░░░░░░▄▄▄▄▄█▀▀▀██▄░░░░             
▀█░░░░░░░░░▄█▀▀░░▀▀█▄░░░░█▄░░░
░█▄░▄░░░░░▄█░░░░░░░░█▄░█░░█░░░
░▄█▄██▄░░░█▄░░██░░░░██▄▄▄██░░░
░████░▀▀░░░█▄░░░░░░▄█░░░░░██░░
░█░░██▄▄░░░░▀██▄▄██▀▄▄▄▄▄▄█░░░
░░▄█▀░░░░░░░░░▄▄██▀▀▀▀▀▀▀░▀█▄░              1.Создать сессию
░░▀█░░░░░░░▄█▀▀░░░░░░░░░░░░░█▄              2.Следить
░░░▀█▄▄█▀░█▀░░░░░░░░░░░░░░░▄█▀              3.Выйти из программы
░░░░░░██░▄█░░░█▀██▀▀█▀██▀▀▀▀░░
░░░░░▄█░░▀█░░▀█░█░░██░██░░░░░░
░░░░██▀█▄░▀█▄░▀▀████▀▀██░░░░░░               Время запуска: {time}
░░░░█░░░▀▀█▄▀█▄▄▄▄▄▄▄▄██▄░░░░░               {ip}


"""


session_file = 'see.session'


async def create_session():
    connect_bd()
    api_id = input('ur api id --> ')        
    api_hash =  input('ur api hash --> ')  
    phone = input("enter ur phone number --> ")
    client = TelegramClient(session_file, api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input("enter code --> ")
            insert_history(api_id, api_hash)
            try:
                await client.sign_in(phone, code)
            except errors.SessionPasswordNeededError:
                password = input("enter 2fa --> ")
                await client.sign_in(password=password)
        except Exception as e:
            print(Fore.RED + f"auth error: {e}")
            input()
            await client.disconnect()
            return
    print("session created")
    await client.disconnect()
    

async def spy(target_username):
    print("Сохранять информацию в txt файл?(y or n)")
    choice = input(Fore.BLUE + '--> ')
    api_id, api_hash = get_history()
    
    client = TelegramClient(session_file, api_id, api_hash)

    await client.start()
    me = await client.get_me()
    try:
        target = await client.get_entity(target_username)

        target_id = target.id
        target_first_name = target.first_name
        target_last_name = target.last_name
        target_photo = target.photo
        last_status = target.status
        target_username = target.username
        last_msg_id = None

       
      
        print(Fore.BLUE + f"""
    ==========================================
    Следим через сессию: @{me.username}
    Следим за: @{target.username}

    Имя - {target_first_name}
    Фамилия - {target_last_name}
    id - {target_id}
    Аватарка - {"да" if target_photo else "нет"} 
    ==========================================
    """)
        
        @client.on(events.NewMessage(chats=target_id))
        async def your(event):
            if event.out:
                message_time = datetime.datetime.now()
                print(Fore.GREEN + f"Вы отправили новое сообщение для @{target_username}: {event.text} ({message_time.strftime('%H:%M:%S')})")


        @client.on(events.NewMessage(from_users=target_id))
        async def handler(event):
            if event.sender_id == target_id:
                nonlocal last_msg_id
                last_msg_id = event.id
                message_time = datetime.datetime.now()
                print(Fore.GREEN + f"Новое сообщение от @{target_username}: {event.message.text} ({message_time.strftime('%H:%M:%S')})")

        @client.on(events.MessageRead())
        async def shii(event):
            nonlocal last_msg_id
            last_msg_checked_time = datetime.datetime.now()
            if last_msg_id is None:
                return
            
            if event.max_id >= last_msg_id:
                print(Fore.GREEN + f"Сообщение от вас было прочитано. ({last_msg_checked_time.strftime('%H:%M:%S')})")
    
        while True:
            fuck = ""
            try:
                target = await client.get_entity(target_id)
             
                current_fist_name = target.first_name
                current_username = target.username
                current_last_name = target.last_name
                current_photo = target.photo
                status = target.status


                if current_username != target_username:
                    user_change_time = datetime.datetime.now()
                    if current_username is None:
                        fuck +=  f"Пользователь полностью удалил юзернейм: {target_username} ({fname_change_time.strftime('%H:%M:%S')})"
                        print(Fore.BLUE + f"Пользователь полностью удалил юзернейм: {target_username} ({fname_change_time.strftime('%H:%M:%S')})")
                    else:
                        fuck += f'Пользователь поменял юзернейм: @{target_username} -> @{current_username} ({user_change_time.strftime("%H:%M:%S")})'
                        print(Fore.BLUE + f'Пользователь поменял юзернейм: @{target_username} -> @{current_username} (({user_change_time.strftime("%H:%M:%S")}))')
                        target_username = current_username if current_username else target_username

                if current_fist_name != target_first_name:
                    fname_change_time = datetime.datetime.now()
                    fuck += f"Пользователь поменял имя: {target_first_name} -> {current_fist_name} ({fname_change_time.strftime("%H:%M:%S")})"
                    print(Fore.BLUE + f"Пользователь поменял имя: {target_first_name} -> {current_fist_name} ({fname_change_time.strftime("%H:%M:%S")})")
                    target_first_name = current_fist_name

                if current_last_name != target_last_name:
                    lname_change_time = datetime.datetime.now()
                    if current_last_name is None:
                        fuck += f"Пользователь полностью удалил фамилию: {target_last_name} ({lname_change_time.strftime('%H:%M:%S')})"
                        print(Fore.BLUE + f"Пользователь полностью удалил фамилию: {target_last_name} ({lname_change_time.strftime('%H:%M:%S')})")
                    else:
                        fuck += f"Пользоватль поменял фамилию: {target_last_name} -> {current_last_name} ({lname_change_time.strftime("%H:%M:%S")})"
                        print(Fore.BLUE + f"Пользоватль поменял фамилию: {target_last_name} -> {current_last_name} ({lname_change_time.strftime("%H:%M:%S")})")
                    target_last_name = current_last_name

                if target_photo is None and current_photo is not None:
                    photo_time = datetime.datetime.now()
                    fuck += f'Пользователь установил аватарку ({photo_time.strftime("%H:%M:%S")})'
                    print(Fore.BLUE + f'Пользователь установил аватарку ({photo_time.strftime("%H:%M:%S")})')
                    target_photo = current_photo

                elif target_photo is not None and current_photo is None:
                    photo_time = datetime.datetime.now()
                    fuck += f'Пользователь удалил аватарку ({photo_time.strftime("%H:%M:%S")})'
                    print(Fore.BLUE + f'Пользователь удалил аватарку ({photo_time.strftime("%H:%M:%S")})')
                    target_photo = current_photo
                    
                elif target_photo != current_photo and target_photo:
                    photo_time = datetime.datetime.now()
                    fuck += f'Пользователь сменил аватарку ({photo_time.strftime("%H:%M:%S")})'
                    print(Fore.BLUE + f'Пользователь сменил аватарку ({photo_time.strftime("%H:%M:%S")})')
                    target_photo = current_photo
        
                if isinstance(status, UserStatusOnline):
                    if last_status != 'online':
                        last_online_time = datetime.datetime.now()
                        fuck += f'Пользователь @{target_username} зашёл в сеть ({last_online_time.strftime("%H:%M:%S")})'
                        print(Fore.GREEN + f'Пользователь @{target_username} зашёл в сеть ({last_online_time.strftime("%H:%M:%S")})')
                        last_status = 'online'
                elif isinstance(status, UserStatusOffline):
                    if last_status != 'offline':
                        last_offline_time = datetime.datetime.now()
                        fuck += f'Пользователь @{target_username} вышел из сети ({last_offline_time.strftime("%H:%M:%S")})'
                        print(Fore.RED + f'Пользователь @{target_username} вышел из сети ({last_offline_time.strftime("%H:%M:%S")})')
                        last_status = 'offline'
                else:
                    if last_status != 'unknown':
                        fuck +=  f'Пользователь @{target_username} статус {status}'
                        print(Fore.RED + f'Пользователь @{target_username} статус {status}')
                        last_status = 'unknown'

                if (choice in ["y", "yes"]) and fuck:
                    with open(f"{target_username}.txt", "a", encoding='utf-8') as file:
                        file.write(f"\n{fuck}")
                else:
                    pass

                await asyncio.sleep(1)  

            except Exception as e:
                print(Fore.RED + f"Ошибка получения данных пользователя: {e}")
                await asyncio.sleep(5)

    except Exception as e:
        print(Fore.RED + f"Произошла ошибка: юзернейм не верный.")
        print(Fore.YELLOW +'Нажмите enter для возврата в меню.')
        input()
          


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    while True:
        print(Fore.BLUE + banner)
        choice = input(Fore.BLUE + '--> ')
        if choice == '1':
            asyncio.run(create_session())
        elif choice == '2':
            if get_history() is not None:
                target_username = input(Fore.BLUE + 'Введите username для слежки --> '.replace("@", ''))
                asyncio.run(spy(target_username))
            else:
                print(Fore.RED + 'Для работы скрипта необходимо создать сессию!')
        elif choice == '3':
            break
        clear()

main()