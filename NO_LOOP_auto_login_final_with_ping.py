import subprocess
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fungsi untuk memeriksa koneksi internet
def check_internet_connection():
    try:
        # Menggunakan ping ke 8.8.8.8 untuk mengecek koneksi internet
        result = subprocess.run(
            ["ping", "-c", "4", "8.8.8.8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # Mengecek apakah paket diterima
        if result.returncode == 0:
            return True  # Koneksi internet tersedia
        else:
            return False  # Tidak ada koneksi internet
    except Exception as e:
        print(f"Error saat memeriksa koneksi internet: {e}")
        return False

# Path ke ChromeDriver
chromedriver_path = "/usr/bin/chromedriver"
service = Service(chromedriver_path)

# Setup opsi Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Fungsi login
def login(driver):
    try:
        print("\nMembuka halaman login...")
        driver.get("http://u-sarah.ac.id/login")

        print("Menunggu halaman termuat...")
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        print("Halaman termuat. Menunggu elemen input username tersedia...")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input#inputUser")))

        print("Elemen input username ditemukan. Memasukkan username...")
        username_input = driver.find_element(By.CSS_SELECTOR, "input#inputUser")
        username_input.clear()
        username_input.send_keys(os.getenv("USERNAME", "ptipd5"))  # Menggunakan variabel lingkungan untuk username

        print("Menunggu elemen input password tersedia...")
        password_input = driver.find_element(By.CSS_SELECTOR, "input#inputPassword")
        password_input.clear()
        password_input.send_keys(os.getenv("PASSWORD", "ptipd123"))  # Menggunakan variabel lingkungan untuk password

        print("Mengirim form login...")
        password_input.send_keys(Keys.RETURN)

        print("Menunggu proses login dan redirect...")
        WebDriverWait(driver, 10).until(EC.url_to_be("http://u-sarah.ac.id/status"))  # Tunggu sampai URL berubah

        print(f"URL setelah login: {driver.current_url}\n")

    except Exception as e:
        print(f"Terjadi kesalahan saat login: {e}")

# Fungsi utama untuk memeriksa koneksi internet dan login
if __name__ == "__main__":
    print("\nMemeriksa koneksi internet...")
    print("----------------------------------------")

    if check_internet_connection():
        print("Koneksi internet tersedia. Tidak perlu menjalankan login.")
    else:
        print("Tidak ada koneksi internet. Menjalankan skrip login...")
        
        # Jalankan ChromeDriver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Jalankan proses login
        login(driver)
        
        # Tutup driver setelah selesai
        driver.quit()
        print("Proses login selesai.")
