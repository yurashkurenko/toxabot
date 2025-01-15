from vedis import Vedis
DB_PATH = 'bot_database.vdb'

# Функции для работы с базой данных
def get_db():
    return Vedis(DB_PATH)

def save_user_interaction(user_id: int, message: str):
    with get_db() as db:
        key = f"user:{user_id}:history"
        history = db.List(key)
        history.append(message.encode('utf-8'))

def get_user_history(user_id: int, limit: int = 5):
    with get_db() as db:
        key = f"user:{user_id}:history"
        history = db.List(key)
        return [msg.decode('utf-8') for msg in history[-limit:]]

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    history = get_user_history(user_id)
    if history:
        response = "Ваша история сообщений:\n" + "\n".join(history)
    else:
        response = "История сообщений пуста"
    await update.message.reply_text(response)


