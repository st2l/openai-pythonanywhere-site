import os
from openai import OpenAI


client = OpenAI(api_key='___')

def input_headers(headers_entry: str):
    headers = headers_entry.split('\n')
    return headers

def input_keywords(keyword_entry: str):
    keywords = {}
    for line in keyword_entry.split('\n'):
        line = line.replace('\t', ' ')

        try:
            # Разбиваем строку по последнему пробелу
            keyword, frequency = line.rsplit(' ', 1)
            keywords[keyword.strip()] = int(frequency.strip())
        except ValueError:
            print(f"Ошибка формата для строки: '{line}'. Попробуйте снова.")
    return keywords

# Функция для генерации текста по каждому подзаголовку
def generate_initial_text(subheading, model="gpt-4o-mini"):
    prompt = (
        f"Ты – профессиональный копирайтер. Напиши раздел на тему '{subheading}'.\n"
        "Текст должен быть простым, но профессиональным. Размер текста - 3-5 абзацев по 5-7 предложений каждый. "
        "Используй короткие и ясные предложения. Не пиши очень много текста. Старайся, чтобы текст был насыщен качественной полезной информацией. Избегай выражений с пассивным залогом, сложносочиненных и сложноподчиненных предложений. "
        "Все сложные термины объясняй простыми словами. Избегай шаблонных фраз и клише. Включай только полезную и важную информацию. "
        "Текст должен быть уникальным и не содержать длинных, перегруженных предложений."
    )

    response = client.chat.completions.create(model=model,
                                              messages=[
                                                  {"role": "user", "content": prompt}
                                              ],
                                              max_tokens=5000,
                                              temperature=0.7)

    return response.choices[0].message.content.strip()


# Функция для вставки ключевых слов в текст
def insert_keywords(text, keywords, model="gpt-4o-mini"):
    keyword_list = ', '.join(keywords)
    prompt = (
        f"Текст, который нужно доработать: {text}\n\n"
        f"Вставь ключевые слова в текст. Вот список ключевых слов и их частоты: {keyword_list}. "
        "Каждое ключевое слово должно быть вставлено в текст ровно столько раз, сколько указано. "
        "Пожалуйста, убедись, что текст остаётся естественным и читаемым. Не изменяй стиль и структуру текста."
    )

    response = client.chat.completions.create(model=model,
                                              messages=[
                                                  {"role": "user", "content": prompt}
                                              ],
                                              max_tokens=5000,
                                              temperature=0.7)

    return response.choices[0].message.content.strip()

# Функция для обработки и генерации текста на основе подзаголовков и ключевых слов
def process_headings(subheadings, keywords, output_file='ans.txt'):
    # Проверяем, существует ли папка, и создаем её, если необходимо
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir) and output_dir:
        os.makedirs(output_dir)

    # Открываем файл для записи
    with open(output_file, "w", encoding="utf-8") as f:
        # Генерация начального текста и вставка ключевых слов для каждого подзаголовка
        for subheading in subheadings:
            initial_text = generate_initial_text(subheading)
            subheading_keywords = {k: v for k, v in keywords.items() if k in initial_text}  # Фильтруем ключевые слова
            section_text = insert_keywords(initial_text, subheading_keywords)
            f.write(f"{subheading}\n{section_text}\n\n")
            print(f"Текст для '{subheading}' добавлен в файл: {output_file}")
    return output_file