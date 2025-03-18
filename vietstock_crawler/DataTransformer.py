import pandas as pd
import os
from datetime import datetime

class DataTransformer:
    def __init__(self, stock_codes, table_names, input_folder="financial_reports", output_folder="processed_data"):
        self.stock_codes = stock_codes
        self.table_names = table_names
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_financial_report(self, stock_code, table_name):
        input_csv = os.path.join(self.input_folder, table_name, f"{table_name}_csv", f"{stock_code}_financial_report1.csv")
        if not os.path.exists(input_csv):
            print(f"⚠️ File không tồn tại: {input_csv}")
            return None

        df = pd.read_csv(input_csv, header=0).dropna(how='all')
        quarters = df.columns[1:]

        records = []
        for _, row in df.iterrows():
            indicator = str(row.iloc[0]).strip()
            if indicator in ["Giai đoạn", "Hợp nhất", "Kiểm toán", "Công ty kiểm toán", "Ý kiến kiểm toán"]:
                continue

            for quarter in quarters:
                quarter_formatted = quarter.replace("/", "")
                report_id = f"{stock_code}BCKQKD{quarter_formatted}"
                value = str(row[quarter]).replace(",", "")

                if value in ["", "nan", "None"]:
                    continue

                ingestion_date = updated_date = datetime.now().strftime("%Y-%m-%d")
                records.append([report_id, indicator, value, ingestion_date, updated_date])

        df_result = pd.DataFrame(records, columns=["report_id", "index", "value", "ingestion_date", "updated_date"])

        output_path = os.path.join(self.output_folder, f"processed_{table_name}")
        os.makedirs(output_path, exist_ok=True)

        output_csv = os.path.join(output_path, f"{stock_code}_processed_income_statement.csv")
        df_result.to_csv(output_csv, index=False, encoding="utf-8")

        print(f"✅ File đã được lưu tại: {output_csv}")
        return df_result

    def run(self):
        for stock_code in self.stock_codes:
            for table_name in self.table_names:
                print(f"🔄 Đang xử lý: {stock_code} - {table_name}")
                self.process_financial_report(stock_code, table_name)

if __name__ == "__main__":
    stock_codes = [
        "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
        "LPB", "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", "STB",
        "TCB", "TPB", "VCB", "VHM", "VIC", "VJC", "VNM", "VPB", "VRE"
    ]

    table_names = {"inc_state", "balance", "cash_flow"}

    transformer = DataTransformer(stock_codes, table_names)
    transformer.run()
