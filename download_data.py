import time
import datetime
import os
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

########################### FUNCTIONS ########################### 

def click(xpath):
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

def choose_date(xpath, date):
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.clear()
    element.send_keys(date)
    time.sleep(2)

def check_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate over the files and folders inside the directory
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if the item is a file or a folder
            if os.path.isfile(file_path):
                # Remove the file
                os.remove(file_path)
            elif os.path.isdir(file_path):
                # Recursively remove the subfolder and its contents
                shutil.rmtree(file_path)
    else:
        os.makedirs(folder_path)

def excels_to_csv(tab_code, base_folder, download_path, 
                  tab_name, subtab_name, region, station):
    # Set timer
    start_time = time.time()

    # Specify the output CSV file name
    kazgydromet_path = os.path.join(base_folder, 'kazgydromet_data')
    folder_dir = os.path.join(kazgydromet_path, tab_name, subtab_name, region)

    is_exist = os.path.exists(folder_dir)
    if not is_exist:
        os.makedirs(folder_dir)

    if '/' in station:
        station = station.replace('/', '-')

    if subtab_name != '':
        temp_list = (tab_name, subtab_name, region, station + '.csv')
    else:
        temp_list = (tab_name, region, station + '.csv')
    
    csv_name = '_'.join(temp_list)

    output_csv_file = os.path.join(folder_dir, csv_name)

    # Iterate thorugh each page and download all corresponding excel files

    excel_xpath = "//text()[.='Excel']/ancestor::button[1]"
    next_button_xpath = "//a[text() = 'Next']"
    pages_xpath = f'/html[1]/body[1]/div[1]/div[1]/section[1]/div[1]/div[{tab_code}]/div[1]/div[2]/div[1]/div[1]/div[6]'

    page_count = 1
    
    # Download excel file (wait until table is updated and wait until the whole file is done downloading)
    if subtab_name == 'возд':
        time.sleep(7)
    else:
        time.sleep(3)

    click(excel_xpath)
    time.sleep(2)

    if subtab_name != '':
        print(f"[EXCEL] Page {page_count} of {tab_name}_{subtab_name}_{region}_{station} was downloaded successfully.")
    else: 
        print(f"[EXCEL] Page {page_count} of {tab_name}_{region}_{station} was downloaded successfully.")
    
    # Downloaded excel file name
    input_file_path = os.path.join(download_path, "МЕТЕОРОЛОГИЧЕСКАЯ БАЗА ДАННЫХ.xlsx")
    
    # Create a dataframe where all data from all excel files will be merged
    merged_df = pd.read_excel(input_file_path, skiprows=2)

    # Collect all page numbers to a list
    element = driver.find_element(By.XPATH, pages_xpath)
    pages = element.find_elements(By.CLASS_NAME, 'paginate_button')
    pages_list = [page.text for page in pages if page.text != '']

    # While not the last page
    while str(page_count) != pages_list[-2]:

        # Delete Excel file to free memory
        check_folder(download_path)

        page_count += 1

        click(next_button_xpath)
        time.sleep(3)

        click(excel_xpath)
        time.sleep(2)
        
        if subtab_name != '':
            print(f"[EXCEL] Page {page_count} of {tab_name}_{subtab_name}_{region}_{station} was downloaded successfully.")
        else:
            print(f"[EXCEL] Page {page_count} of {tab_name}_{region}_{station} was downloaded successfully.")

        new_excel = pd.read_excel(input_file_path, skiprows=2)
        merged_df = pd.concat([merged_df, new_excel], ignore_index=True)

    # Add "region" and "type" columns to the dataframe
    type_name = tab_name + '_' + subtab_name if subtab_name != '' else tab_name
    merged_df.insert(0, 'type', type_name)
    merged_df.insert(1, 'region', region)
    
    # Save the merged dataframe as a CSV file
    merged_df.to_csv(output_csv_file, index=False)
    print(f"[CSV] File '{output_csv_file}' was saved successfully.")
    
    process_time = str(datetime.timedelta(seconds = (time.time() - start_time)))
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"[TIME] Process time: {process_time}. Current time: {current_time}")

    # Delete the last Excel file to free memory
    check_folder(download_path)


def apply_filters(tab_code, base_folder, download_path, tab_name, subtab_name=''):

    date_xpath = f'/html[1]/body[1]/div[1]/div[1]/section[1]/div[1]/div[{tab_code}]/div[1]/div[1]/div[3]/div[1]/div[1]/input[1]'
    region_xpath = f"/html[1]/body[1]/div[1]/div[1]/section[1]/div[1]/div[{tab_code}]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]"
    station_xpath = f"/html[1]/body[1]/div[1]/div[1]/section[1]/div[1]/div[{tab_code}]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]"
    
    # Choose date from "Диапозон даты:" date picker
    choose_date(date_xpath, "2000-01-01")
    
    # Locate and click on "Регион:" drop down
    click(region_xpath)

    # Collect all "Регион:" name options to a list
    region_text = driver.find_elements(By.XPATH, f"//*[@role='option']")
    region_options = [region.text for region in region_text if region.text != '']
    
    # Iterate through each "Регион:" option
    for region_option in region_options:
# ['KZ-AKM', 'KZ-AKT', 'KZ-ALM', 'KZ-ATY', 'KZ-KAR', 'KZ-KUS', 'KZ-KZY','KZ-MAN', 'KZ-PAV', 
# 'KZ-SEV', 'KZ-VOS', 'KZ-YUZ', 'KZ-ZAP', 'KZ-ZHA']:

        # if region_option in ['KZ-AKM', 'KZ-AKT']:
        #     continue
            
        click(region_xpath)
        if region_option == 'KZ-AKM':
            click(f"//text()[.='{region_option}']/ancestor::div")
        else:
            click(f"//text()[.='{region_option}']/ancestor::div[1]")
        time.sleep(3)
        
        # Locate and click on "Станция:" drop down
        click(station_xpath)

        # Collect all "Станция:" name options to a list
        station_text = driver.find_elements(By.XPATH, f"//*[@role='option']")
        station_options = [station.text for station in station_text if station.text != '']
        print(station_options)

        # Iterate through each "Станция:" option
        for station_option in station_options:

            # if station_option in ['Алматы', 'Кеген', 'Айдарлы', 'Аксенгир']:

            click(station_xpath)
            click(f"//div[text()='{station_option}']")
            time.sleep(2)
            
            # Download Excel file and convert it to CSV
            excels_to_csv(tab_code, base_folder, download_path, tab_name, 
                        subtab_name, region_option, station_option)
            

########################### LOCATORS ###################################

class XPATHS_BANK:
    def __init__(self, name, xpath):
        self.name = name
        self.xpath = xpath
        self.subxpath = {}

# 1 Срочные данные
srochniye_danniye = XPATHS_BANK(name = 'сроч-данн', 
                            xpath = "//span[contains(.,'1 Срочные данные')]")

# 1.1 Tемпература
temperatura = XPATHS_BANK(name = 'темп',
                        xpath = "//span[contains(.,'1.1 Температура')]")

temperatura.subxpath['возд'] = "//a[contains(.,' 1.1.1 Воздуха')]"
temperatura.subxpath['пов-почвы'] = "//a[contains(.,' 1.1.2 Пов. почвы')]"
temperatura.subxpath['точ-росы'] = "//a[contains(.,' 1.1.3 Точки росы')]"

# 1.2 Парциональное давление
parc_davlenie = XPATHS_BANK(name = 'парц-давл',
                            xpath = "//span[contains(.,'1.2 Парциальное давление')]")

# 1.3 Относительная влажность, проценты
otn_vlazh_proc = XPATHS_BANK(name = 'отн-влаж-проц',
                            xpath = "//span[contains(.,'1.3 Относительная влажность, проценты')]")

# 1.4 Дефицит насыщения
deficit_nasyshenniya = XPATHS_BANK(name = 'дефиц-насыщ', 
                                xpath = "//span[contains(.,'1.4 Дефицит насыщения')]")

# 1.5 Атмосферное давление
atmosfer_davleniye = XPATHS_BANK(name = 'атм-давл', 
                                xpath = "//span[contains(.,'1.5 Атмосферное давление')]")

atmosfer_davleniye.subxpath['на-ур-станц'] = "//a[contains(.,' 1.5.1 На уровне станции')]"
atmosfer_davleniye.subxpath['на-ур-моря'] = "//a[contains(.,' 1.5.2 На уровне моря')]"

# 1.6 Барическая тенденция
barich_tendenc = XPATHS_BANK(name = 'бар-тенд',
                            xpath = "//span[contains(.,'1.6 Барическая тенденция')]")

barich_tendenc.subxpath['вид-кривой'] = "//a[contains(.,' 1.6.1 вид кривой')]"
barich_tendenc.subxpath['велич-гпа'] = "//a[contains(.,' 1.6.2 величина, гПа')]"

# 1.7 Видимость
vidimost = XPATHS_BANK(name = 'видим',
                    xpath = "//span[contains(.,'1.7 Видимость')]")

# 1.8 Облачность
oblachnost = XPATHS_BANK(name = 'облач',
                        xpath = "//span[contains(.,'1.8 Облачность')]")

kolich_bally = XPATHS_BANK(name = 'колич-балл',
                        xpath = "//span[contains(.,'Количесто, баллы')]")
kolich_bally.subxpath['o'] = "//a[contains(.,' 1.8.1 о')]"
kolich_bally.subxpath['н'] = "//a[contains(.,' 1.8.2 н')]"

formy = XPATHS_BANK(name = 'формы',
                    xpath = "//span[contains(.,'Формы')]")

formy.subxpath['ci-cc-cs'] = "//a[contains(.,' 1.8.3 Ci, Cc, Cs')]"
formy.subxpath['ac-as'] = "//a[contains(.,' 1.8.4 Ac, As')]"
formy.subxpath['cu-cb'] = "//a[contains(.,' 1.8.5 Cu, Cb')]"
formy.subxpath['st-sc'] = "//a[contains(.,' 1.8.6 St, Sc')]"
formy.subxpath['frnb'] = "//a[contains(.,' 1.8.7 Frnb')]"

# 1.9 Погода шифр
pogoda_shifr = XPATHS_BANK(name = 'пог-шифр',
                        xpath = "//span[contains(.,'1.9 Погода шифр')]")
pogoda_shifr.subxpath['ww'] = "//a[contains(.,' 1.9.1 WW')]"
pogoda_shifr.subxpath['w1w2'] = "//a[contains(.,' 1.9.2 W1W2')]"

# 1.10 Ветер
veter = XPATHS_BANK(name = 'ветер',
                    xpath = "//span[contains(.,'1.10 Ветер')]")
veter.subxpath['напр-гр'] = "//a[contains(.,' 1.10.1 Направление, гр')]"
veter.subxpath['cкор-ветра'] = "//a[contains(.,' 1.10.2 Скорость ветра, м/с')]"

# 1.11 Осадки
osadki = XPATHS_BANK(name = 'осадки',
                    xpath = "//span[contains(.,'1.11 Осадки')]")

# all_tabs = [temperatura, parc_davlenie, otn_vlazh_proc, deficit_nasyshenniya, atmosfer_davleniye, 
#          barich_tendenc, vidimost, oblachnost, pogoda_shifr, veter, osadki]

all_tabs = [barich_tendenc]

########################### TAB CODES ###################################

tab_codes = {'возд': 5,
             'пов-почвы': 6,
             'точ-росы': 7,
             'парц-давл': 8,
             'отн-влаж-проц': 9,
             'дефиц-насыщ': 10,
             'на-ур-станц': 11,
             'на-ур-моря': 12,
             'вид-кривой': 13,
             'велич-гпа': 14,
             'видим': 15,
             'o': 16,
             'н': 17,
             'ci-cc-cs': 18,
             'ac-as': 19,
             'cu-cb': 20,
             'st-sc': 21,
             'frnb': 22,
             'ww': 25,
             'w1w2': 26,
             'напр-гр': 27,
             'cкор-ветра': 28,
             'осадки': 29
            }

#########################################################################

# Create necessary folders
base_folder = os.getcwd()

# Set up Selenium WebDriver
chrome_options = webdriver.ChromeOptions()
download_path = os.path.join(base_folder, 'temp_downloads')

# Launch Selenium WebDriver
chrome_options.add_experimental_option('prefs', 
                {'download.default_directory' : download_path,
                 "detach": True})
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
# driver.maximize_window()

driver.get("http://ecodata.kz:3838/dm_climat_ru/")
wait = WebDriverWait(driver, 30)

# Locate and click on "1 Срочные данные"
click(srochniye_danniye.xpath)

# Iterate through each tab in "1 Срочные данные"
for tab in all_tabs:
    # Make sure the folder is empty
    check_folder(download_path)

    click(tab.xpath)

    if tab.subxpath:
        for subtab_name, subtab_xpath in tab.subxpath.items():
            click(subtab_xpath)
            apply_filters(tab_codes[subtab_name], base_folder, download_path, 
                          tab.name, subtab_name)
    else:
        apply_filters(tab_codes[tab.name], base_folder, download_path, tab.name)