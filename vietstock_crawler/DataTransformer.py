import os
import pandas as pd

class DataTransformer:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.csv_dir = os.path.join(base_dir, "csv")
        self.output_dir = os.path.join(base_dir, "processed_csv")
        os.makedirs(self.output_dir, exist_ok=True)

    def process_csv_files(self):
        """Duyệt qua các thư mục con trong `csv_dir` để xử lý các file CSV."""
        for category in ["cash_flow", "inc_state"]:
            category_path = os.path.join(self.csv_dir, category)
            if not os.path.exists(category_path):
                continue
            
            for stock_folder in os.listdir(category_path):
                stock_path = os.path.join(category_path, stock_folder)
                if os.path.isdir(stock_path):
                    self.process_stock_folder(stock_path, category)

    def process_stock_folder(self, folder_path: str, category: str):
        """Xử lý tất cả các file CSV trong một thư mục cụ thể."""
        stock_name = os.path.basename(folder_path).replace("_csv", "")
        
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                file_path = os.path.join(folder_path, file)
                self.process_csv_file(file_path, stock_name, category, file)

    def process_csv_file(self, file_path: str, stock_name: str, category: str, original_filename: str):
        """Đọc file CSV, xử lý dữ liệu và lưu kết quả."""
        try:
            df = pd.read_csv(file_path)
            # Thêm cột phân loại
            df["Stock"] = stock_name
            df["Category"] = category
            
            # Tạo tên file mới
            processed_filename = original_filename.replace(".csv", "_processed.csv")
            output_file = os.path.join(self.output_dir, processed_filename)
            
            df.to_csv(output_file, index=False)
            print(f"Processed: {output_file}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    base_dir = "./parsed_data_raw"
    transformer = DataTransformer(base_dir)
    transformer.process_csv_files()
