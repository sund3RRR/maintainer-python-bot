# Maintainer-bot
***Maintainer-telegram-bot*** is simple but useful assistant, that notify you about new `GitHub` releases (`GitLab`, `BitBucket`, etc. will be added later).
<div align="center">
  
  ![image](https://github.com/sund3RRR/maintainer-bot/assets/73298492/b2fa9fb7-0ef5-46ac-a7a9-971f76507f24)
  
</div>

# Setup
### Clone git repository
```bash
git clone https://github.com/sund3RRR/maintainer-bot.git
cd maintainer-bot
```
### Setup python
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
### Run
Don't forget to set your tokens in  environment variables.
```
githubToken=<TOKEN> tgToken=<TOKEN> python src/run.py
```
# Info
Bot uses an exception wrapper, which is set via `excepthook` to catch unhandled exceptions and write them to the `log/` directory.
```python
def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, exc_traceback))
    tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    dt = datetime.datetime.now().strftime(r"%Y-%m-%d-%H:%M")
    with open(f"log/exception-{dt}.log", "w") as f:
        f.write(tb)

sys.excepthook = log_exception
```
# Media
<div align="center">
  
![image](https://github.com/sund3RRR/maintainer-bot/assets/73298492/9b6b0f2e-7442-424b-91db-144943fbee90)
![add_repo](https://github.com/sund3RRR/maintainer-bot/assets/73298492/34c3baab-be8c-45f5-b1ea-76e764339415)
![list_repos](https://github.com/sund3RRR/maintainer-bot/assets/73298492/e98aa6a6-69cd-4006-8477-a6e61577967a)

</div>
