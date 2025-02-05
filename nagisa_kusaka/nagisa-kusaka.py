import tkinter as tk
from PIL import Image, ImageTk


class DraggableImageWindow:
    def __init__(self, image_path, scale=1.0):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.wm_attributes("-topmost", 1)  # Делаем окно поверх всех

        self.image_path = image_path
        self.image = None
        self.photo = None
        self.label = None
        self.offset_x = 0
        self.offset_y = 0
        self.scale = scale  # Переменная для изменения размера

        self.load_image()
        self.bind_events()

    def load_image(self):
        try:
            self.image = Image.open(self.image_path)
            self.image = self.image.resize(
                (int(self.image.width * self.scale), int(self.image.height * self.scale))
            )
            self.photo = ImageTk.PhotoImage(self.image)
            self.label = tk.Label(self.root, image=self.photo, bg="white")
            self.label.image = self.photo
            self.label.pack()

            width = self.image.width
            height = self.image.height
            x = (self.root.winfo_screenwidth() - width) // 2
            y = (self.root.winfo_screenheight() - height) // 2
            self.root.geometry(f"{width}x{height}+{x}+{y}")
        except FileNotFoundError:
            print(f"Ошибка: файл изображения не найден: {self.image_path}")
            self.root.destroy()
        except Exception as e:
            print(f"Ошибка при обработке изображения: {e}")
            self.root.destroy()

    def bind_events(self):
        if self.label:
            self.label.bind("<ButtonPress-1>", self.start_drag)
            self.label.bind("<B1-Motion>", self.drag)
            self.label.bind("<ButtonRelease-1>", self.stop_drag)
            self.label.bind("<Double-Button-1>", self.close_window)  # Закрытие окна

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        x = self.root.winfo_x() + (event.x - self.offset_x)
        y = self.root.winfo_y() + (event.y - self.offset_y)
        self.root.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        pass

    def close_window(self, event):
        self.root.destroy()  # Закрыть окно при двойном нажатии

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    image_file = "image (64).png"  # Замените на путь к вашему PNG файлу
    scale_factor = 0.8  # Задайте масштаб
    window = DraggableImageWindow(image_file, scale_factor)
    window.run()

