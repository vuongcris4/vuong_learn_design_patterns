from abc import ABC, abstractmethod

# --- HỆ THỐNG PHÂN CẤP 1: IMPLEMENTATION (Các giao diện) ---

class ITheme(ABC):
    """
    Giao diện Implementor.
    Định nghĩa các phương thức mà mọi theme cụ thể phải có.
    """
    @abstractmethod
    def get_background_color(self) -> str:
        pass
    
    @abstractmethod
    def get_font_color(self) -> str:
        pass

class LightTheme(ITheme):
    """Một Concrete Implementor."""
    def get_background_color(self) -> str:
        return "Màu trắng"
    
    def get_font_color(self) -> str:
        return "Màu đen"

class DarkTheme(ITheme):
    """Một Concrete Implementor khác."""
    def get_background_color(self) -> str:
        return "Màu đen"
    
    def get_font_color(self) -> str:
        return "Màu trắng"

# --- HỆ THỐNG PHÂN CẤP 2: ABSTRACTION (Các trang web) ---

class WebPage(ABC):
    """
    Lớp Abstraction.
    Nó chứa một tham chiếu đến một đối tượng Implementor (theme).
    Đây chính là "Cây cầu".
    """
    def __init__(self, theme: ITheme):
        self._theme = theme

    @abstractmethod
    def get_content(self) -> str:
        pass

class AboutPage(WebPage):
    """Một Refined Abstraction."""
    def get_content(self) -> str:
        return (f"Trang Giới thiệu.\n"
                f"  - Màu nền: {self._theme.get_background_color()}\n"
                f"  - Màu chữ: {self._theme.get_font_color()}")

class HomePage(WebPage):
    """Một Refined Abstraction khác."""
    def get_content(self) -> str:
        return (f"Trang Chủ.\n"
                f"  - Màu nền: {self._theme.get_background_color()}\n"
                f"  - Màu chữ: {self._theme.get_font_color()}")

# --- Client Code ---
if __name__ == "__main__":
    # Tạo ra các đối tượng triển khai (các theme)
    light_theme = LightTheme()
    dark_theme = DarkTheme()
    
    # Client có thể kết hợp bất kỳ Abstraction nào với bất kỳ Implementation nào.
    
    print("--- Tạo các trang với Light Theme ---")
    about_light = AboutPage(light_theme)
    home_light = HomePage(light_theme)
    print(about_light.get_content())
    print(home_light.get_content())

    print("\n--- Tạo các trang tương tự với Dark Theme ---")
    # Chúng ta không cần tạo lớp mới, chỉ cần "tiêm" một theme khác vào.
    about_dark = AboutPage(dark_theme)
    home_dark = HomePage(dark_theme)
    print(about_dark.get_content())
    print(home_dark.get_content())