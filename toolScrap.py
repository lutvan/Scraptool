from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time


print(Fore.CYAN + Style.BRIGHT + ''' 
                                                                                     __
                                                                                    / /
███████╗ ██████╗██████╗  █████╗ ██████╗ ████████╗ ██████╗  ██████╗ ██╗             / /
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║            / /
███████╗██║     ██████╔╝███████║██████╔╝   ██║   ██║   ██║██║   ██║██║           / /
╚════██║██║     ██╔══██╗██╔══██║██╔═ ══╝   ██║   ██║   ██║██║   ██║██║       ___/ /___
███████║╚██████╗██║  ██║██║  ██║██║        ██║   ╚██████╔╝╚██████╔╝███████╗ //////////
                                                                           //////////
''' + Fore.BLACK + Style.BRIGHT + '''
    Developer : Lutvan
    Email     : nightbatman649@gmail.com
    Github    : OKelutvan
    Version   : 0.1.0

''' + Fore.CYAN + Style.BRIGHT + '===========================================')

# input URL
print("\nInputkan dengan CTRL + SHIFT + V\n")
input_url = input("Masukan URL : ")
input_element1 = input("Masukan element pembungkus yang akan discrap : ")
input_class1 = input("Masukan class pembungkus yang akan discrap : ")

# memasukan target element yang akan discrap
print("==============================")
input_element2 = input("Masukan target element yang akan discrap : ")
input_class2 = input("Masukan target class dari element yang akan discrap : ")
print("\nJumlah scroll screen pada web : \n")
count_scroll = int(input("Masukan jumlah scroll screen : "))

# Setting
opsi = webdriver.ChromeOptions()
opsi.add_argument('--ignore-certificate-errors')
opsi.add_argument('--ignore-ssl-errors')
opsi.add_argument('--disable-web-security')
opsi.add_argument('--allow-running-insecure-content')
opsi.add_argument('--disable-blink-features=AutomationControlled')
opsi.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
opsi.add_argument('--headless=new')
servis = Service("Chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=servis, options=opsi)



# grep structure
driver.get(input_url)
# scroll
width_screen = 700
for i in range(1,count_scroll):
    akhir = width_screen * i
    script = "window.scrollTo(0, "+str(akhir)+")"
    driver.execute_script(script)
    print("Loading scroll screen ", i)
    time.sleep(1)
print("Wait for the process....")


time.sleep(5)
content = driver.page_source
data = BeautifulSoup(content, 'html.parser')


list_heading = []

count = 1
for area in data.find_all(input_element1, class_=input_class1):
    print("data ke ", count)
    heading = area.find(input_element2, class_=input_class2).get_text()
    list_heading.append(heading)
    count += 1

driver.quit()

input_save_file = input("Apakah anda ingin save file dalam bentuk Excel? (y/n) : ").lower()
if input_save_file == 'y':
    input_name_column = input("Masukan nama kolom : ")
    input_name_file = input("Masukan nama file (.xlsx): ")
    dataF = pd.DataFrame({input_name_column: list_heading})
    dataF.to_excel(input_name_file, index=False, sheet_name='Sheet1')