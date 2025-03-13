import asyncio
import os
import re
import pandas as pd
import google.generativeai as genai
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig, CacheMode
import multiprocessing


os.environ["GOOGLE_API_KEY"] = "AIzaSyA1upkMkhy1abNO_Zu7AGHIqf5H6J18INU"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class WebPageParser:
    def __init__(self, stock_codes, table_sign, base_path):
        self.stock_codes = stock_codes
        self.table_sign = table_sign
        self.base_path = base_path

    async def crawl_local_file(self, local_file_path, sign):
        file_url = f"file://{local_file_path}"
        config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=file_url, config=config)
            if result.success:
                soup = BeautifulSoup(result.html, "html.parser")
                table = soup.find("table", {"class": "table table-hover", "id": sign})

                if not table:
                    table = soup.find("table", {"class": "table table-hover", "id": "tbl-data-LCTT-direct"})

                if table:
                    rows = []
                    for row in table.find_all("tr"):
                        cells = [cell.get_text(separator=" ", strip=True) for cell in row.find_all(["th", "td"])]
                        if cells:
                            rows.append(" | ".join(cells))

                    return "\n".join(rows)
            return None

    def markdown_to_csv(self, markdown_text, stock_code, num_page, sign, output_folder):
        os.makedirs(output_folder, exist_ok=True)
        output_filename = os.path.join(output_folder, f"{stock_code}_{sign}_{num_page}.csv")

        lines = [line for line in markdown_text.strip().split("\n") if not re.match(r'^-+\|', line)]
        data = [[cell.strip().replace('__', '') for cell in line.split("|")] for line in lines]
        data = [[cell for cell in row if cell] for row in data]

        df = pd.DataFrame(data)
        header_row_index = next(i for i, row in enumerate(data) if any("Q" in cell for cell in row))
        df.columns = df.iloc[header_row_index].tolist()
        df = df.iloc[header_row_index + 1:].reset_index(drop=True)

        df.to_csv(output_filename, index=False, encoding="utf-8-sig")
        print(f"File CSV saved: {output_filename}")

    def markdown_to_excel(self, markdown_text, stock_code, num_page, sign , output_folder):
        os.makedirs(output_folder, exist_ok=True)
        output_filename = os.path.join(output_folder, f"{stock_code}_{sign}_{num_page}.xlsx")

        lines = [line for line in markdown_text.strip().split("\n") if not re.match(r'^-+\|', line)]
        data = [[cell.strip().replace('__', '') for cell in line.split("|")] for line in lines]
        data = [[cell for cell in row if cell] for row in data]

        df = pd.DataFrame(data)
        header_row_index = next(i for i, row in enumerate(data) if any("Q" in cell for cell in row))
        df.columns = df.iloc[header_row_index].tolist()
        df = df.iloc[header_row_index + 1:].reset_index(drop=True)

        df.to_excel(output_filename, index=False)
        print(f"File Excel saved: {output_filename}")

        import multiprocessing

    def process_file(self, args):
        local_file_path, stock_code, table, signs = args
        numpage = int(re.search(r'(\d+)(?=\.\w+$)', os.path.basename(local_file_path)).group(1))
        print(f"Processing: {local_file_path}, numpage: {numpage}")

        for sign in signs:
            markdown_data = asyncio.run(self.crawl_local_file(local_file_path, sign))  # Chạy async trong multiprocess
            if markdown_data:
                csv_folder = f"parsed_data_raw/csv/{table}/{stock_code}_csv"
                excel_folder = f"parsed_data_raw/excel/{table}/{stock_code}_excel"
                self.markdown_to_csv(markdown_data, stock_code, numpage, sign, csv_folder)
                self.markdown_to_excel(markdown_data, stock_code, numpage, sign, excel_folder)


    async def process(self):
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())  # Sử dụng tối đa CPU

        tasks = []
        for stock_code in self.stock_codes:
            for table, signs in self.table_sign.items():
                if isinstance(signs, str):  # Nếu chỉ có 1 bảng, chuyển thành danh sách
                    signs = [signs]

                pj_path = os.path.dirname(__file__)
                pj_path = os.path.dirname(pj_path)  # Điều chỉnh tùy theo cấu trúc thư mục
                folder_path = os.path.abspath(os.path.join(pj_path, self.base_path, table, stock_code))
                print("Processing folder: ", folder_path)

                if os.path.exists(folder_path):
                    sorted_files = sorted(
                        os.listdir(folder_path),
                        key=lambda f: int(re.search(r'(\d+)(?=\.\w+$)', f).group(1)) if re.search(r'(\d+)(?=\.\w+$)', f) else 0
                    )

                    for file_name in sorted_files:
                        local_file_path = os.path.join(folder_path, file_name)
                        tasks.append((local_file_path, stock_code, table, signs))

        # Chạy song song các file
        pool.map(self.process_file, tasks)
        pool.close()
        pool.join()


if __name__ == "__main__":
    stock_codes = [
        "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
        "LPB", "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", "STB",
        "TCB", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"
    ]

    table_sign = {
        # "balance": [tbl-data-CDKT],
        "inc_state": ["tbl-data-CDKT"],
        "cash_flow": ["tbl-data-LCTT-indirect", "tbl-data-LCTT-direct"]  # Dùng list để chứa cả hai bảng
    }

    parser = WebPageParser(stock_codes, table_sign, "html_pages")
    asyncio.run(parser.process())
