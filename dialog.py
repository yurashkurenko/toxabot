from vedis import Vedis
#vedis_db=Vedis("dbvedis.db")
#vedis_db["Привет"]="Привет от Vedis"
DB_PATH = 'bot_database.vdb'

# Функции для работы с базой данных
def get_db():
    return Vedis(DB_PATH)

def get_answer_from_vedis(query):
    with get_db() as db:
        key = query.lower()
        answer = db.List(key)
#    return query+" От Vedis"
#    """Получает ответ из Redis, если есть, иначе возвращает None."""
#    key = query.lower()  # Преобразуем запрос к нижнему регистру для поиска
#    answer = vedis_db[key]
#   return answer.decode("utf-8") if answer else None
    return answer.decode("utf-8") if answer else "Привет"


def get_answer_from_llm(query):
    """Запрашивает ответ у LLM, если в Redis нет."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Или другой подходящий engine
            prompt=query,
            max_tokens=256,  # Установите подходящее количество токенов
            n=1,
            stop=None,
            temperature=0.7,  # Экспериментируйте с этим параметром
        )
        answer = response.choices[0].text.strip()
        return answer
    except openai.error.OpenAIError as e:
        print(f"Ошибка OpenAI: {e}")
        return "Извините, я столкнулся с проблемой."

def dialog(query):
    return query+" "+get_answer_from_vedis(query)
