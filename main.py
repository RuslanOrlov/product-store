# Ctrl + Shift + X  - открыть панель расширений с нужным ИИ помощником и
#                     полностью отключить/включить (Disable / Enable)
#                     (если не видно нужное расширение, в строке поиска
#                     написать GitHub Copilot Chat или Fitten Code)

# Ctrl + Shift + P  - открыть палитру команд и набрать GitHub Copilot: Disable/Enable
#                     (или имя другого помощника), чтобы найти нужную команду
#                     и нажать Enter, чтобы отключить/включить ИИ помощника

# Для включения автозаполнения Fitten Code:
# 1. нажать шестеренку слева снизу -> Settings ->
# 2. ввести в поле поиска fitten ->
# 3. включить галочку в поле "Enable inline code completion"

# Закомментировать несколько строк  - Ctrl + K, затем Ctrl + C
# Раскомментировать несколько строк - Ctrl + K, затем Ctrl + U

from fastapi import FastAPI, Response

app = FastAPI()
