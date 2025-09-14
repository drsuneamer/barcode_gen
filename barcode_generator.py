import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from barcode import Code128
from barcode.writer import ImageWriter
import io
import sys
import os

def resource_path(relative_path):
    """ PyInstaller로 묶였을 때 리소스 경로 처리 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def generate_barcode(event=None):  # event 추가로 엔터에도 대응
    code = entry.get().strip()
    if not code:
        messagebox.showwarning("입력 오류", "코드를 입력하세요.")
        return
    try:
        buffer = io.BytesIO()
        writer = ImageWriter()
        writer.font_path = resource_path("fonts/DejaVuSansMono.ttf")
        writer.text = ""  # 텍스트 없이 바코드만 생성

        barcode = Code128(code, writer=writer)
        barcode.write(buffer)
        buffer.seek(0)
        image = Image.open(buffer).convert("RGB")
        image.thumbnail((400, 200))
        img_tk = ImageTk.PhotoImage(image)
        label_image.config(image=img_tk)
        label_image.image = img_tk
        label_image.barcode_image = image  # 저장용
    except Exception as e:
        messagebox.showerror("에러 발생", str(e))

def save_image():
    if not hasattr(label_image, "barcode_image"):
        messagebox.showwarning("저장 오류", "먼저 바코드를 생성하세요.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG 이미지", "*.png")])
    if filepath:
        label_image.barcode_image.save(filepath)
        messagebox.showinfo("저장 완료", f"이미지가 저장되었습니다:\n{filepath}")

# 배경색 변수
BG_COLOR = "#f0E1C4"

# GUI 세팅
root = tk.Tk()
root.title("Barcode Generator")
root.geometry("500x400")
root.iconbitmap(resource_path("bcd_logo_small.ico"))
root.configure(bg=BG_COLOR)

label = tk.Label(root, text="바코드에 사용할 코드 입력:", bg=BG_COLOR)
label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14), justify='center', bg="white")
entry.pack(pady=5)
entry.bind('<Return>', generate_barcode)  # 엔터 입력시 바코드 생성 바로 실행

btn_generate = tk.Button(root, text="바코드 생성", command=generate_barcode, bg=BG_COLOR, activebackground=BG_COLOR)
btn_generate.pack(pady=10)

label_image = tk.Label(root, bg=BG_COLOR)
label_image.pack(pady=10)

btn_save = tk.Button(root, text="이미지 저장", command=save_image, bg=BG_COLOR, activebackground=BG_COLOR)
btn_save.pack(pady=10)

root.mainloop()