import base64
import re
import requests
import fitz  # PyMuPDF
import os


logo = """ 
\033[1;36m                     ██░ ██  ▄▄▄       ▄████▄   ██░ ██  ██▓ ███▄ ▄███▓ ▄▄▄       ███▄    █ 
                    ▓██░ ██▒▒████▄    ▒██▀ ▀█  ▓██░ ██▒▓██▒▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ 
                    ▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▒██▀▀██░▒██▒▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒
\033[1;93m                    ░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒░▓█ ░██ ░██░▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒
                    ░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░░▓█▒░██▓░██░▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░
                    ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░ ▒ ░░▒░▒░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ 
                    ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒    ▒ ░▒░ ░ ▒ ░░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░
                    ░  ░░ ░  ░   ▒   ░         ░  ░░ ░ ▒ ░░      ░     ░   ▒      ░   ░ ░ 
                    ░  ░  ░      ░  ░░ ░       ░  ░  ░ ░         ░         ░  ░         ░ 
                                    ░                                                              
                                TOOL DOWNLOAD TÀI LIỆU THƯ VIỆN SỐ UTE BY @ductuongug                   
"""


def clean_base64(raw_text: str) -> str:
    """Làm sạch chuỗi: chỉ giữ lại ký tự Base64 hợp lệ (A-Z, a-z, 0-9, +, /, =)"""
    return re.sub(r'[^A-Za-z0-9+/=]', '', raw_text)

def clean_url(raw_url: str) -> str:
    """Lấy dãy số cuối cùng trước .html."""
    m = re.search(r"(\d+)(?=\.html?$)", raw_url)
    return m.group(1) if m else ""

def download_and_extract(url: str, output_pdf: str = "extracted.pdf", render: bool = False, page_num: int = 1):
    print(f"Đang tải nội dung từ: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Lỗi khi tải URL: {e}")
        print("Có thể server chặn request từ bên ngoài, hoặc link hết hạn.")
        return

    raw_text = response.text
    clean_str = clean_base64(raw_text)
    
    print(f"Độ dài chuỗi Base64 sau clean: {len(clean_str)} ký tự")

    try:
        pdf_bytes = base64.b64decode(clean_str, validate=True)
    except base64.binascii.Error as e:
        print(f"Lỗi decode Base64: {e}")
        print("Chuỗi không phải Base64 hợp lệ hoặc không phải PDF.")
        return

    # Lưu file PDF
    with open(output_pdf, "wb") as f:
        f.write(pdf_bytes)
    
    file_size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    print(f"PDF đã lưu thành công: {output_pdf} ({file_size_mb:.2f} MB)")

    # Kiểm tra và render (nếu yêu cầu)
    try:
        doc = fitz.open(output_pdf)
        print(f"PDF hợp lệ – Tổng {doc.page_count} trang.")
        
        if render and doc.page_count > 0:
            page_idx = page_num - 1
            if page_idx < 0 or page_idx >= doc.page_count:
                print(f"Trang {page_num} không tồn tại → render trang 1 thay thế.")
                page_idx = 0
            page = doc.load_page(page_idx)
            pix = page.get_pixmap(dpi=150)  # Độ phân giải tốt để xem rõ
            image_path = f"page_{page_num}.png"
            pix.save(image_path)
            print(f"Đã render trang {page_num} thành ảnh: {image_path}")
        
        doc.close()
    except Exception as e:
        print(f"Lưu PDF thành công nhưng không mở được (có thể không phải PDF): {e}")

def main():
    print(logo)
    
    url = input("Nhập URL: ").strip()
    if not url:
        print("URL không được để trống!")
        return
    
    output_pdf = input("Nhập tên file PDF đầu ra (Enter để dùng mặc định 'extracted.pdf'): ").strip()
    if not output_pdf:
        output_pdf = "extracted.pdf"
    
    render_choice = input("Có render trang 1 thành ảnh PNG để xem trước không? (y/n, mặc định y): ").strip().lower()
    render = render_choice != 'n'
    
    cleaned_id = clean_url(url)
    if cleaned_id:
        download_and_extract(f"https://thuvienso.hcmute.edu.vn/doc/loadpdf2?id={cleaned_id}", output_pdf, render)

if __name__ == "__main__":
    main()