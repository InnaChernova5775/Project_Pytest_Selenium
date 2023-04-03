import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


@pytest.fixture(autouse=True)
def testing():
    EXE_PATH = r'C:\Users\Инна\PycharmProjects\pythonProject\Project_Pytest_Selenium\chromedriver.exe'
    pytest.driver = webdriver.Chrome(executable_path=EXE_PATH)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    pytest.driver.implicitly_wait(10)  # неявное ожидание
    yield
    pytest.driver.quit()


def test_show_my_pets():

    pytest.driver.find_element(By.ID, 'email').send_keys('innachernova5577@yandex.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345678910')

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Добавляем явное ожидание на загрузку главной страницы с карточками питомцев
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-deck')))

    # Переходим на страницу "Мои питомцы"
    pytest.driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/my_pets"]').click()

    # Устанавливаем явное ожидание для загрузки страницы "Мои питомцы"
    WebDriverWait(pytest.driver,10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))

    # Получаем элементы -фото питомцев со страницы "Мои питомцы" по СSS-локатору
    images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets tbody th img')

    # Получаем элементы информации пользователя по XPATH-локатору
    info_user = pytest.driver.find_elements(By.XPATH, '//*[@class=".col-sm-4 left"]')

    # Получаем элементы имени питомцев со страницы "Мои питомцы' по XPATH-локатору
    names = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')

    # Получаем элементы пород питомцев со страницы "Мои питомцы' по XPATH-локатору
    animals_typs = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')

    # Получаем элементы возраста питомцев со страницы "Мои питомцы' по XPATH-локатору
    ages = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    list_info_user = info_user[0].text.split()
    num_pets = int(list_info_user[3])

    list_names = []
    for i in range(len(names)):
        list_names.append(names[i].text)
    unique_names = set(list_names)

    list_animals_types = []
    for i in range(len(animals_typs)):
        list_animals_types.append(animals_typs[i].text)

    list_ages = []
    for i in range(len(animals_typs)):
        list_ages.append(ages[i].text)

    pets_matrix = np.array([list_names, list_animals_types, list_ages])
    pets_matrix_trans = pets_matrix.transpose()
    list_my_pets = pets_matrix_trans.tolist()

    is_unique = True
    for i in list_my_pets:
        if list_my_pets.count(i) > 1:
            is_unique = False
            break
    if not is_unique:
        print(f"{list_my_pets(i)}Питомцы повторяются")
    else:
        print("Питомцы уникальны")

    assert len(names) == num_pets
    assert len(images) >= num_pets // 2
    assert len(names) == len(animals_typs) == len(ages)
    assert len(list_names) == len(unique_names)
