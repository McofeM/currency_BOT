from selenium import webdriver
from bs4 import BeautifulSoup as bs


def course(url):
    cours = []
    all_cours = []
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    )
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        HTML = driver.page_source
        soup = bs(HTML, "html.parser")
        top_growing = soup.find('p', string="Топ зростаючих").find_parent()
        top_falling = soup.find('p', string="Топ падаючих").find_parent()
        user_choice = soup.find('p', string="Вибір користувачів").find_parent()
        for search in top_growing, top_falling, user_choice:
            section_name = search.find('p').text.strip()
            ul = search.find('ul')

            items = [li for li in ul.find_all('li') if li.a]

            for item in items:
                name = item.find('span').text.strip()
                price = item.find_all('span')[-2].text.strip()
                change = item.find_all('span')[-1].text.strip()
                all_cours.append("https://whitebit.com" + item.a['href'] + "?tab=open-orders")

                if section_name == "Топ зростаючих":
                    cours = f"""
                    {name}
                    Ціна: {price}
                    Зміни ціни у відцотках: {change}"""
                if section_name == "Топ падаючих":
                    cours = f"""
                    {name}
                    Ціна: {price}
                    Зміни ціни у відцотках: {change}"""
                if section_name == "Популярна валюта":
                    cours = f"""
                    {name}
                    Ціна: {price}
                    Зміни ціни у відцотках: {change}"""
                all_cours.append(cours)
        return all_cours

    except Exception as ex:
        print(type(ex).__name__, ex)
        return [f"Помилка при витягуванні даних: {type(ex).__name__}, Повідомлення: {ex}"]
    finally:
        driver.close()
        driver.quit()


def main():
    (course("https://whitebit.com/ua/markets"))


if __name__ == '__main__':
    main()



