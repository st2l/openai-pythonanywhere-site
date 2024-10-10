from openai import OpenAI
import os

client = OpenAI(api_key='___')


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


# Функция для уникализации текста
def unique_text(text, model="ft:gpt-4o-mini-2024-07-18:personal:unique-text-maker:A96wW44G"):
    prompt = (
        f"Ты крутой копирайтер, который пишет уникальные тексты. Вот текст, который нужно сделать уникальным:\n{text}\n"
        "Пожалуйста, перепиши текст так, чтобы он стал уникальным, сохранив все ключевые моменты."
    )

    response = client.chat.completions.create(model=model,
                                              messages=[
                                                  {"role": "user", "content": prompt}
                                              ],
                                              max_tokens=5000,
                                              temperature=0.7)

    return response.choices[0].message.content.strip()


# Функция для обработки и генерации текста на основе подзаголовков и ключевых слов
def process_headings(subheadings, keywords, output_file):
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
            unique_section_text = unique_text(section_text)  # Уникализация текста
            f.write(f"{subheading}\n{unique_section_text}\n\n")
            print(f"Текст для '{subheading}' добавлен в файл: {output_file}")


# Функция для ввода подзаголовков через консоль
def input_subheadings():
    subheadings = []
    print("Введите подзаголовки (формат 'H2: Текст подзаголовка'), завершите ввод пустой строкой:")
    while True:
        subheading = input()
        if not subheading:
            break
        subheadings.append(subheading.strip())
    return subheadings


# Функция для ввода ключевых слов через консоль
def input_keywords():
    keywords = {}
    print("Введите ключевые слова и их частоту в формате 'слово частота', завершите ввод пустой строкой:")
    while True:
        keyword_entry = input().strip()

        if not keyword_entry:
            break

        # Заменяем табуляции на пробелы
        keyword_entry = keyword_entry.replace('\t', ' ')

        try:
            # Разбиваем строку по последнему пробелу
            keyword, frequency = keyword_entry.rsplit(' ', 1)
            keywords[keyword.strip()] = int(frequency.strip())
        except ValueError:
            print(f"Ошибка формата для строки: '{keyword_entry}'. Попробуйте снова.")

    return keywords


# Основная функция для запуска процесса
def main():
    subheadings = input_subheadings()
    keywords = input_keywords()

    output_file = input("Введите полный путь к файлу для сохранения результата: ").strip()

    process_headings(subheadings, keywords, output_file)


if __name__ == "__main__":
    main()
