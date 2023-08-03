import sys
from aiogram import types


import sys
sys.path.append("..")
from db import get_db_conn_and_cursor


def create_repo_list(user_id :int) -> str:
    _, cursor = get_db_conn_and_cursor()

    cursor.execute("""
        SELECT * FROM repos 
        WHERE user == ?""", 
        (
            user_id,
        )
    )
    user_repos = cursor.fetchall()
    repo_list_str = ""
    for i, repo in enumerate(user_repos):
        repo_list_str += f"{i+1}) <b>{repo[2]}</b> / <b>{repo[3]}</b> <code>{repo[4]}</code>\n"
    return repo_list_str, user_repos


async def list_repo(message :types.Message, repo_str = ""):
    if repo_str == "":
        message_text, _ = create_repo_list(message.from_user.id)
    else:
        message_text = repo_str
    if message_text == "":
        message_text = "There is no repo now! Add a couple :)"
    await message.answer(message_text, parse_mode="html")