from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from utils.DownloadTools import login
import concurrent.futures


class PageDownloader:
    def __init__(self,driver, email, password):
        self.email = email
        self.password = password
        self.max_count = 53

        self.driver = driver

    def download_page(self,url,stock_code,table):
        self.driver.get(url)
        time.sleep(1)
        
        save_dir = f"html_pages/{table}/{stock_code}"
        os.makedirs(save_dir, exist_ok=True)

        for count in range(self.max_count):
            file_path = os.path.join(save_dir, f"{stock_code}_page_{count+1}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print(f"📄 Đã lưu: {file_path}")
            
            try:
                back_button = self.driver.find_element(By.NAME, "btn-page-2")
                if "disabled" in back_button.get_attribute("class"):
                    print("Dừng lại ttrang số: ",(count+1))
                    print("⏹️ Nút 'Quay lại' bị vô hiệu hóa, dừng quá trình.")
                    break
                self.driver.execute_script("arguments[0].scrollIntoView(true);", back_button)
                time.sleep(5)
                try:
                    back_button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", back_button)    
                time.sleep(3)
                print("⬅️ Đã bấm nút quay lại để thu thập dữ liệu cũ hơn.")
            except Exception as e:
                print("Dừng lại ttrang số: ",(count+1))
                print(f"⚠️ Lỗi khi bấm nút 'Quay lại': {e}")
                break

    # def download_page_cafe(self,url,stock_code,table):
    #     self.driver.get(url)
    #     time.sleep(1)
        
    #     save_dir = f"html_pages/{table}/{stock_code}"
    #     os.makedirs(save_dir, exist_ok=True)

    #     for count in range(self.max_count):
    #         file_path = os.path.join(save_dir, f"{stock_code}_page_{count+1}.html")
    #         with open(file_path, "w", encoding="utf-8") as f:
    #             f.write(self.driver.page_source)
    #         print(f"📄 Đã lưu: {file_path}")
            
    #         try:
    #             next_button = self.driver.find_element(By.CLASS_NAME, "fa-chevron-right")
    #             if "enable" in next_button.get_attribute("class"):
    #                 print("Dừng lại ttrang số: ",(count+1))
    #                 print("⏹️ Nút 'Quay lại' bị vô hiệu hóa, dừng quá trình.")
    #                 break
    #             self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
    #             time.sleep(5)
    #             try:
    #                 next_button.click()
    #             except:
    #                 self.driver.execute_script("arguments[0].click();", next_button)    
    #             time.sleep(3)
    #             print("⬅️ Đã bấm nút quay lại để thu thập dữ liệu cũ hơn.")
    #         except Exception as e:
    #             print("Dừng lại ttrang số: ",(count+1))
    #             print(f"⚠️ Lỗi khi bấm nút 'Quay lại': {e}")
    #             break


    def download_single_page(self, save_dir, stock_code, count):
        """ Lưu HTML của trang hiện tại """
        file_path = os.path.join(save_dir, f"{stock_code}_page_{count+1}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        print(f"📄 Đã lưu: {file_path}")

    def download_page_cafe(self, url, stock_code, table):
        """ Tải nhiều trang bằng Multithreading """
        self.driver.get(url)
        time.sleep(1)

        save_dir = f"html_pages/{table}/{stock_code}"
        os.makedirs(save_dir, exist_ok=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = []

            for count in range(self.max_count):
                futures.append(executor.submit(self.download_single_page, save_dir, stock_code, count))

                try:
                    next_button = self.driver.find_element(By.CLASS_NAME, "fa-chevron-right")
                    if "enable" in next_button.get_attribute("class"):
                        print("Dừng lại trang số:", count + 1)
                        break

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(2)

                    try:
                        next_button.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", next_button)
                    
                    time.sleep(3)
                    print("➡️ Đã bấm nút tiếp tục để thu thập dữ liệu.")

                except Exception as e:
                    print("⚠️ Lỗi khi bấm nút 'Tiếp tục':", e)
                    break

            # Đợi tất cả các luồng hoàn thành
            concurrent.futures.wait(futures)
if __name__ == "__main__":
    # Initial config
    EMAIL = "nguyenhanam_t66@hus.edu.vn"
    PASSWORD = "nguyenhanam_t66"
    stock_codes = [
        # "ACB",
        #   "BCM", "BID", "BVH", "CTG", "FPT", 
        #   "GAS", 
        #   "GVR", "HDB", "HPG",
        # "LPB", "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB",
        # "SSI", 
        "STB",
        "TCB", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"
    ]
    table_urls = {
        # "balance" : "CDKT",
        # "inc_state": "KQKD",
        # "cash_flow": "LC&languageid=1",
        "cafef-his-1": "1",
        "cafef-his-2": "2",
        "cafef-his-3": "3"

    }

    # Selenium setup
    options = Options()
    options.add_argument("--headless=new")  # Chạy trình duyệt ở chế độ nền (headless)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-web-security")
    options.add_argument("--ignore-ssl-errors")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
        

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Start login
    # login(driver,"https://finance.vietstock.vn/ACB/tai-chinh.htm?tab=CDKT",EMAIL,PASSWORD)
    bot = PageDownloader(driver,EMAIL, PASSWORD)

    print("_____________Start Download______________________")
    for stock_code in stock_codes:
        for table, tab in table_urls.items():
            url = f"https://cafef.vn/du-lieu/lich-su-giao-dich-{stock_code.lower()}-{tab}.chn#data"
            bot.download_page_cafe(url,stock_code,table)
    driver.quit() 
