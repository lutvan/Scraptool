from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

while True:

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

    print("\nInputkan dengan CTRL + SHIFT + V\n")

    input_url = input("Masukan URL : ")
    element_pembungkus = input("Masukan element pembungkus yang akan discrap : ")
    class_pembungkus = input("Masukan class pembungkus yang akan discrap : ")

    print("\nJumlah scroll screen pada web : \n")

    count_scroll = int(input("Masukan jumlah scroll screen : "))

    jumlah_kolom = int(input("Masukan jumlah kolom row untuk tabel pada excel : ")) 

    kolom_info = []
    for i in range(jumlah_kolom):
        print(f"\n== Kolom ke-{i+1} ==")
        nama_kolom = input("Masukan nama kolom : ")
        elemen = input("Masukan nama elemen HTML target : ")
        kelas = input("Masukan nama class dari elemen target : ")
        kolom_info.append({
            "nama": nama_kolom,
            "elemen": elemen,
            "kelas": kelas,
        })

    # Settingan
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

    
    driver.get(input_url)
    width_screen = 700
    for i in range(1, count_scroll):
        akhir = width_screen * i
        script = f"window.scrollTo(0, {akhir})"
        driver.execute_script(script)
        print("Loading scroll screen ", i)
        time.sleep(1)
    print("Wait for the process....")
    time.sleep(5)

    # scraping
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    data_rows = []
    count = 1
    for area in soup.find_all(element_pembungkus, class_=class_pembungkus):
        row = {}
        print("Data ke", count)
        for kolom in kolom_info:
            target = area.find(kolom['elemen'], class_=kolom['kelas'])
            row[kolom['nama']] = target.get_text(strip=True) if target else ''
        data_rows.append(row)
        count += 1

    driver.quit()

    
    input_save_file = input("Apakah anda ingin save file dalam bentuk Excel? (y/n) : ").lower()
    if input_save_file == 'y':
        input_name_file = input("Masukan nama file (.xlsx): ")
        df = pd.DataFrame(data_rows)
        df.to_excel(input_name_file, index=False, sheet_name='Sheet1')
        print(f"Data berhasil disimpan ke {input_name_file}")


    tanya = input("Coba lagi? y/n : ").lower()
    if tanya != 'y':
        break
    
    os.system('cls')
