import time
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ваш Discord токен
DISCORD_TOKEN = 'OTc1MzE3NDMzMTA1Njc0MjYw.GIYqPM.oNO_CV0o2Vi6PZmAoOltqitUvgQ5mV88-bOtLY'
# URL сервера та каналу, куди бот повинен зайти
DISCORD_VOICE_CHANNEL_URL = 'https://discord.com/channels/472108046559084585/1106663142739693578'
# Фраза, яку потрібно озвучити
PHRASE_TO_SPEAK = "Привіт, це тестовий бот."


def login_to_discord():
    # Налаштування браузера з автоматичним дозволом на мікрофон
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")

    # Автоматичний дозвіл на мікрофон, камеру, геолокацію та сповіщення
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    })

    # Ініціалізація Selenium WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Відкриваємо Discord і входимо через токен
    driver.get("https://discord.com/login")
    time.sleep(2)

    # Вставка токену через консоль (неофіційний метод, використовуйте з обережністю)
    script = f"""
    function login(token) {{
        setInterval(() => {{
            document.body.appendChild(document.createElement(`iframe`)).contentWindow.localStorage.token = `"${{token}}"`;
        }}, 50);
        setTimeout(() => {{
            location.reload();
        }}, 2500);
    }}
    login("{DISCORD_TOKEN}");
    """
    driver.execute_script(script)
    time.sleep(5)

    # Переходимо в голосовий канал
    driver.get(DISCORD_VOICE_CHANNEL_URL)
    print("Перейшли в голосовий канал, очікування на кнопку 'Join Voice'...")

    # Очікуємо на кнопку за допомогою нового точного XPATH і натискаємо її
    try:
        join_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[4]/div[2]/div[1]/div/div[1]/button/div'))
        )
        print("Кнопка 'Join Voice' знайдена, підключаємося...")
        join_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Не вдалося знайти кнопку приєднання до голосового каналу: {e}")

    return driver


def speak_phrase(phrase):
    # Ініціалізація TTS (Text-to-Speech) двигуна
    engine = pyttsx3.init()
    engine.say(phrase)
    engine.runAndWait()


def main():
    driver = login_to_discord()
    time.sleep(2)
    speak_phrase(PHRASE_TO_SPEAK)
    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    main()
