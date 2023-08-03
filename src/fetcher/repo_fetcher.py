import asyncio, re

from aiogram import Bot
from github.GitRelease import GitRelease
from github.Tag import Tag

from .github_fetcher import g

import sys
sys.path.append("..")
from db import get_db_conn_and_cursor


async def fetch_repos(bot :Bot):
    conn, cursor = get_db_conn_and_cursor()

    while True:
        cursor.execute("""
            SELECT * FROM repos;
        """)
        repos = cursor.fetchall()

        for db_repo in repos:
            repo = g.get_repo(f"{db_repo[2]}/{db_repo[3]}")

            if db_repo[5]:
                last_release = repo.get_latest_release()
                if db_repo[4] != last_release.tag_name:
                    await send_last_release(db_repo, last_release, bot)

                    cursor.execute("""
                        UPDATE repos
                        SET last_tag_name = ?
                        WHERE id = ?;""",
                        (
                            last_release.tag_name,
                            db_repo[0]
                        )
                    )
                    conn.commit()
            else:
                last_tag :Tag = repo.get_tags()[0]
                if db_repo[4] != last_tag.name:
                    await send_last_tag(db_repo, last_tag, bot)

                    cursor.execute("""
                        UPDATE repos
                        SET last_tag_name = ?
                        WHERE id = ?;""",
                        (
                            last_tag.name,
                            db_repo[0]
                        )
                    )
                    conn.commit()
            

        await asyncio.sleep(60)

def format_release_body(text :str) -> str:
    splitted = text.split("\r\n")
    result = ""
    for line in splitted:
        if len(line) > 0:
            if line[0] == "#":
                line = line.replace("#", "").strip()
                line = f"<b><u>{line}</u></b>"
            result += line + "\r\n"
    result = replace_tags(result, "`", "code")
    result = replace_tags(result, r"\*\*", "b")
    result = replace_tags(result, r"\*", "i")
    return result 


def replace_tags(text :str, md_symbol :str, html_tag :str) -> str:
    # Define a regular expression to find words enclosed in backticks
    pattern = f'{md_symbol}([^`]+){md_symbol}'
    
    # Replace all occurrences of the pattern with <code>word</code>
    result = re.sub(pattern, r'{}\1{}'.format(f"<{html_tag}>", f"</{html_tag}>"), text)
    
    return result


async def send_last_release(repo :tuple, last_release :GitRelease, bot :Bot):
    user_id = repo[1]
    
    message_text = f"<b>{repo[2]}</b> / <b>{repo[3]}</b> " + \
        f"<code>{repo[4]}</code> -> <code>{last_release.tag_name}</code>\n\n" + \
        f"{format_release_body(last_release.body)}\n" + \
        f"{last_release.html_url}"
    
    await bot.send_message(user_id, message_text, parse_mode="html")


async def send_last_tag(repo :tuple, last_tag :Tag, bot :Bot):
    user_id = repo[1]

    message_text = f"<b>{repo[2]}</b> / <b>{repo[3]}</b> " + \
        f"<code>{repo[4]}</code> -> <code>{last_tag.name}</code>\n\n" + \
        f"https://github.com/{repo[2]}/{repo[3]}/releases/tag/{last_tag.name}"
    
    await bot.send_message(user_id, message_text, parse_mode="html")