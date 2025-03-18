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
                table = soup.find("table", {"id": sign})

                if table:
                    print("found table")
                    rows = []
                    for row in table.find_all("tr"):
                        cells = [cell.get_text(separator=" ", strip=True) if cell.get_text(strip=True) else "EMPTY" 
                                for cell in row.find_all(["th", "td"])]
                        rows.append(" | ".join(cells))

                    return "\n".join(rows)
                print("Not found table")
            return None

    def flatten_thead(self,html):
        soup = BeautifulSoup(html, "html.parser")
        thead = soup.find("thead")
        
        if not thead:
            return html  # Trả về HTML gốc nếu không tìm thấy <thead>
        
        rows = thead.find_all("tr")
        if len(rows) < 2:
            return html  # Nếu chỉ có một dòng, không cần gộp

        first_row_cells = rows[0].find_all("td")
        second_row_cells = rows[1].find_all("td")

        new_row = soup.new_tag("tr")  # Tạo một dòng mới

        for cell in first_row_cells:
            colspan = int(cell.get("colspan", "1"))  # Lấy giá trị colspan (mặc định = 1)
            rowspan = int(cell.get("rowspan", "1"))  # Lấy giá trị rowspan (mặc định = 1)

            if colspan > 1:
                # Nếu ô có colspan, lấy số ô tương ứng trong dòng thứ 2
                sub_cells = second_row_cells[:colspan]
                second_row_cells = second_row_cells[colspan:]  # Cập nhật danh sách còn lại
                
                for sub_cell in sub_cells:
                    new_cell = soup.new_tag("td")  # Tạo ô mới
                    new_cell.string = f"{cell.text.strip()} - {sub_cell.text.strip()}"
                    new_row.append(new_cell)
            else:
                # Nếu không có colspan, giữ nguyên
                new_row.append(cell)

        # Xóa nội dung cũ và thêm dòng mới vào thead
        thead.clear()
        thead.append(new_row)

        return str(soup)


    async def crawl_local_file_update(self, local_file_path, sign):
        file_url = f"file://{local_file_path}"
        config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=file_url, config=config)

            if result.success:
                flattened_html = self.flatten_thead(result.html)
                soup = BeautifulSoup(flattened_html, "html.parser")
                table = soup.find("table", {"id": sign})

                if table:
                    print("found table")
                    rows = []
                    for row in table.find_all("tr"):
                        cells = [cell.get_text(separator=" ", strip=True) if cell.get_text(strip=True) else "EMPTY" 
                                for cell in row.find_all(["th", "td"])]
                        rows.append(" | ".join(cells))

                    return "\n".join(rows)
                print("Not found table")
            return None
        return None



    def process_file(self, args):
        local_file_path, stock_code, table, signs = args
        numpage = int(re.search(r'(\d+)(?=\.\w+$)', os.path.basename(local_file_path)).group(1))
        print(f"Processing: {local_file_path}, numpage: {numpage}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        for sign in signs:
            markdown_data = loop.run_until_complete(self.crawl_local_file_update(local_file_path, sign))  # Chạy async
            if markdown_data:
                print("markdown_data worked")
                csv_folder = f"parsed_data_raw/csv/{table}/{stock_code}_csv"
                excel_folder = f"parsed_data_raw/excel/{table}/{stock_code}_excel"
                markdown_to_file(markdown_data, stock_code, numpage, sign, csv_folder, "csv")
                markdown_to_file(markdown_data, stock_code, numpage, sign, excel_folder, "excel")
            else:
                print("markdown_data not worked")
        
        loop.close()


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


def markdown_to_file(markdown_text, stock_code, num_page, sign, output_folder, file_type="csv"):
    print(f"Bắt đầu ghi file {file_type.upper()}...")
    if file_type.lower() == "excel":
        file_type = "xlsx"
    os.makedirs(output_folder, exist_ok=True)
    output_filename = os.path.join(output_folder, f"{stock_code}_{sign}_{num_page}.{file_type}")

    # Xử lý dữ liệu từ Markdown
    lines = [line for line in markdown_text.strip().split("\n") if not re.match(r'^-+\|', line)]
    data = [[cell.strip().replace('__', '').replace('--', '') for cell in line.split("|")] for line in lines]

    # Lấy dòng đầu tiên làm tiêu đề
    headers = data[0] if data else []
    rows = data[1:] if len(data) > 1 else []

    # Lọc bỏ cột "EMPTY"
    empty_col_indexes = {i for i, col in enumerate(headers) if col == "EMPTY"}
    filtered_headers = [col for i, col in enumerate(headers) if i not in empty_col_indexes]
    filtered_rows = [
        [cell if cell != "EMPTY" else "" for i, cell in enumerate(row) if i not in empty_col_indexes]
        for row in rows
    ]

    # Tạo DataFrame và xuất ra file
    df = pd.DataFrame(filtered_rows, columns=filtered_headers)
    if file_type == "csv":
        df.to_csv(output_filename, index=False, encoding="utf-8-sig")
    elif file_type == "xlsx":
        df.to_excel(output_filename, index=False)
    
    print(f"File {file_type.upper()} đã lưu: {output_filename}")

async def test_crawl(base_path,table_sign):
    stock_codes = ["ACB", "BCM", "BID"]

    parser = WebPageParser(stock_codes, table_sign, base_path)

    for stock_code in stock_codes:
        for table, signs in table_sign.items():
            folder_path = os.path.join(base_path, table, stock_code)

            if os.path.exists(folder_path):
                sorted_files = sorted(
                    os.listdir(folder_path),
                    key=lambda f: int(re.search(r'(\d+)(?=\.\w+$)', f).group(1)) if re.search(r'(\d+)(?=\.\w+$)', f) else 0
                )

                for file_name in sorted_files:
                    local_file_path = os.path.join(folder_path, file_name)
                    for sign in signs:
                        markdown_data = await parser.crawl_local_file_update(local_file_path, sign)
                        if markdown_data:
                            print(f"\n### Markdown Table for {stock_code} - {file_name} ###\n")
                            print(markdown_data)




if __name__ == "__main__":
    stock_codes = [
        "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
        "LPB", "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB",
        "SSI", "STB",
        "TCB", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"
    ]

    table_sign = {
        # "inc_state": ["tbl-data-KQKD"],
        # "balance": ["tbl-data-CDKT"],
        # "cash_flow": ["tbl-data-LCTT-indirect", "tbl-data-LCTT-direct"], 
        # "cafef-his-1" : ["owner-contents-table"],
        "cafef-his-2" : ["owner-contents-table"],
        "cafef-his-3" : ["owner-contents-table"]
    }

    parser = WebPageParser(stock_codes, table_sign, "html_pages")
    asyncio.run(parser.process())
    # asyncio.run(test_crawl("html_pages",table_sign))
