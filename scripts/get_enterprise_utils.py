import random
import re
import time
import unicodedata

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def process_url(url_str: str, comp_list: list = None):
    company_codes = []
    company_names = []
    company_exchanges = []
    cafef_url = []
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    driver = webdriver.Firefox(options=option)
    done = 0
    try:
        driver.get(url_str)
        for counts in range(83):
            print(f"Page {counts + 1}")
            html = driver.page_source

            c_codes, c_names, c_exs, c_url = extract_companies(html, comp_list)
            done += len(c_codes)
            print(c_codes)
            print(done)
            company_codes.extend(c_codes)
            company_names.extend(c_names)
            company_exchanges.extend(c_exs)
            cafef_url.extend(c_url)
            if done == len(comp_list):
                break
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "paging-right"))
            )
            next_button.click()
    except TimeoutException:
        driver.get(url_str)
        html = driver.page_source

        c_codes, c_names, c_exs, c_url = extract_companies(html, comp_list)
        done += len(c_codes)

        company_codes.extend(c_codes)
        company_names.extend(c_names)
        company_exchanges.extend(c_exs)
        cafef_url.extend(c_url)
    except ValueError:
        pass
    finally:
        driver.quit()

    df = pd.DataFrame({
        "code": company_codes,
        "name": company_names,
        "exchange": company_exchanges,
        "cafef_url": cafef_url
    })
    return df


def extract_companies(html_str: str, comp_list: list = None):
    soup = BeautifulSoup(html_str, "html.parser")
    tables = None
    tries = 0
    while (tables is None or len(tables) != 1) and tries < 5:
        tables = soup.find_all("table", class_="table-data-business")
        tries += 1
        print("Try getting table again.")
    if not tables:
        raise ValueError("No table found after multiple attempts.")
    table = tables[0]
    rows = table.find_all("tr")
    company_codes = []
    company_names = []
    exchanges = []
    cafef_url = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 0:
            if comp_list and len(comp_list) > 0:
                if cols[0].get_text(strip=True) in comp_list:
                    company_codes.append(cols[0].text.strip())
                    company_names.append(cols[1].text.strip())
                    exchanges.append(cols[3].text.strip())
                    cafef_url.append(cols[0].find("a").get("href"))
            else:
                company_codes.append(cols[0].text.strip())
                company_names.append(cols[1].text.strip())
                exchanges.append(cols[3].text.strip())
                cafef_url.append(cols[0].find("a").get("href"))
        else:
            continue
    return company_codes, company_names, exchanges, cafef_url


def get_industries_data():
    url = "https://esign.misa.vn/5873/ma-nganh-nghe-kinh-doanh/"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    curr_group = ""
    lv_1 = []
    lv_4 = []
    names = []
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            level_1_text = cols[0].text.strip()
            if level_1_text not in ["", "Cấp 1"]:
                curr_group = cols[0].text
            level_4_text = cols[3].text.strip()
            name = cols[5].text.strip()
            if level_4_text not in ["", "Cấp 4"]:
                lv_1.append(curr_group)
                lv_4.append(level_4_text)
                names.append(name)

    return pd.DataFrame({"industry_group": lv_1, "industry_code": lv_4, "industry_name": names})


def get_enterprise_information(enterprise_code: str):
    url = f"https://finance.vietstock.vn/{enterprise_code}/ho-so-doanh-nghiep.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://finance.vietstock.vn/",
    }
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "html5lib")
    try:
        niem_yet = soup.find("div", id="niem-yet").find("table").find("tbody")
        listing = niem_yet.find_all("tr")[0]
        listing_data = listing.find_all("td")
        if listing_data[0].text.strip() == "Ngày giao dịch đầu tiên":
            listing_date = listing_data[1].text.strip()
        else:
            listing_date = None

        print(enterprise_code)

        information = soup.find("div", id="thanh-lap-cong-ty").find("table").find("tbody")
        rows = information.find_all("tr")
        answer = {}
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                field = cols[0].text.strip()
                field = field.replace("• ", "")
                value = cols[1].text.strip()
                match field:
                    case "Mã số thuế":
                        answer['tax_code'] = value
                    case "Địa chỉ":
                        answer['address'] = value
                    case "Điện thoại":
                        answer['phone_number'] = value
                    case "Email":
                        answer['email'] = value
                    case "Website":
                        answer['website'] = value
                    case _:
                        pass

        return answer['tax_code'], answer['address'], answer['phone_number'], answer['email'], answer[
            'website'], listing_date
    except AttributeError:
        return None, None, None, None, None, None


def get_all_enterprise_information(df: pd.DataFrame):
    df[['tax_code', 'address', 'phone_number', 'email', 'website', 'listing_date']] \
        = df['code'].apply(get_enterprise_information).apply(pd.Series)
    return df


def remove_vn_diacritics(text: str) -> str:
    # Normalize Unicode characters to decomposed form (NFD)
    normalized = unicodedata.normalize("NFD", text)
    # Remove diacritic marks (accents)
    no_diacritics = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    # Replace special Vietnamese characters that remain
    replacements = {
        "Đ": "D", "đ": "d"
    }
    return re.sub("|".join(replacements.keys()), lambda m: replacements[m.group()], no_diacritics)


def get_enterprise_industry_based_on_tax_code(tax_code: str | None, company_name: str):
    if tax_code is None or tax_code == "" or tax_code == "nan":
        return None
    company_name = remove_vn_diacritics(company_name)
    company_name = "-".join(company_name.lower().split())
    base_url = "https://thuvienphapluat.vn/ma-so-thue/"
    url = base_url + company_name + "-mst-" + str(tax_code) + ".html"
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 "
        "Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://www.google.com/",
        "Accept-Language": "en-US,en;q=0.9"
    }
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")
    info = soup.find("ul", id='ThongTinDoanhNghiep')
    driver = None
    if not info:
        print("Searching URL")
        search_url = (f"https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep?timtheo=ma-so-thue"
                      f"&tukhoa={tax_code}")
        option = webdriver.FirefoxOptions()
        option.add_argument("--headless")
        driver = webdriver.Firefox(options=option)
        driver.get(search_url)
        try:
            table = driver.find_element(By.CLASS_NAME, "table-bordered")
            links = table.find_elements(By.TAG_NAME, "a")
            for link in links:
                if tax_code.strip() == link.text:
                    url = link.get_attribute("href")
            html = requests.get(url, headers=headers).content
            soup = BeautifulSoup(html, "html.parser")
            info = soup.find("ul", id='ThongTinDoanhNghiep')
        except Exception:
            pass
        finally:
            driver.close()
    else:
        print("Direct URL")
    try:
        count = 0
        for row in info.find_all("li"):
            title = row.find_all("span", class_="dn_1")
            if "Mã ngành" in [s.text.strip() for s in title]:
                break
            count += 1
        main_industry = info.find_all("li")[count + 1].find("div", class_="col-md-2").text.strip()
        print(f"Success {tax_code} - {main_industry}")
        return main_industry
    except Exception as e:
        print(f"Tax code: {tax_code}. Error: {e}")
        return "Exception"
    finally:
        if driver:
            driver.quit()


def get_all_enterprises_industry_code(df: pd.DataFrame):
    df['industry_code'] = df.apply(lambda row: get_enterprise_industry_based_on_tax_code(row['tax_code'], row['name']),
                                   axis=1)

    null_count = df['industry_code'].isnull().sum()
    tries = 0
    while null_count > 0 and tries < 10:
        time.sleep(30)
        tries += 1
        df.loc[df['industry_code'].isnull(), 'industry_code'] = df[df['industry_code'].isnull()].apply(
            lambda row: get_enterprise_industry_based_on_tax_code(row['tax_code'], row['name']),
            axis=1
        )
        null_count = df['industry_code'].isnull().sum()  # Update null_count
    return df


def get_vn30_list():
    url = f"https://topi.vn/vn30-la-gi.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://finance.vietstock.vn/",
    }
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table").find("tbody")
    answer = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        answer.append(cols[1].get_text(strip=True))

    return pd.DataFrame({"stock_code": answer[1:]})


def get_sub_companies(df: pd.DataFrame):
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    driver = webdriver.Firefox(options=option)

    def get_sub_comps(stock_code: str, cf_url: str):
        url = "https://cafef.vn" + cf_url
        driver.get(url)

        comps = []
        comps_types = []
        charter_caps = []
        contributed_caps = []
        own_ratio = []
        try:
            wait = WebDriverWait(driver, 10)
            ctc_button = wait.until(EC.element_to_be_clickable((By.ID, "lsTab4CT")))
            ctc_button.click()
            driver.implicitly_wait(3)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            tables = soup.find_all("table")
            for table in tables:
                if table.find("table", class_="congtycon"):
                    for row in table.find_all('tr'):
                        for col in row.find_all("td"):
                            if 'CÔNG TY CON' in col.get_text(strip=True):
                                rs = col.find_all("tr")
                                legal_rs = [r for r in rs if len([c for c in r.children]) == 13]
                                for r in legal_rs:
                                    legal_cs = r.find_all("td")
                                    comps.append(legal_cs[0].get_text(strip=True))
                                    charter_caps.append(legal_cs[1].get_text(strip=True))
                                    contributed_caps.append(legal_cs[2].get_text(strip=True))
                                    own_ratio.append(legal_cs[3].get_text(strip=True))
                                    comps_types.append("sub")
                            if 'CÔNG TY LIÊN KẾT' in col.get_text(strip=True):
                                rs = col.find_all("tr")
                                legal_rs = [r for r in rs if len([c for c in r.children]) == 13]
                                for r in legal_rs:
                                    legal_cs = r.find_all("td")
                                    comps.append(legal_cs[0].get_text(strip=True))
                                    charter_caps.append(legal_cs[1].get_text(strip=True))
                                    contributed_caps.append(legal_cs[2].get_text(strip=True))
                                    own_ratio.append(legal_cs[3].get_text(strip=True))
                                    comps_types.append("aff")
            return pd.DataFrame({
                "stock_code": stock_code,
                "comp_name": comps,
                "comp_type": comps_types,
                "charter_capital": charter_caps,
                "contributed_capital": contributed_caps,
                "ownership_ratio": own_ratio
            })
        except Exception as e:
            print(f"Error: {stock_code} - {e}")
            return pd.DataFrame({
                "stock_code": [],
                "comp_name": [],
                "comp_type": [],
                "charter_capital": [],
                "contributed_capital": [],
                "ownership_ratio": []
            })

    try:
        sub_comp_list = df.apply(lambda row: get_sub_comps(row['code'], row['cafef_url']), axis=1).tolist()
        sub_comp_df = pd.concat(sub_comp_list, ignore_index=True)
        driver.quit()

        return sub_comp_df
    finally:
        driver.quit()
