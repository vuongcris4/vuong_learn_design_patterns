from abc import ABC, abstractmethod
from typing import List

# --- 1. The Component Interface (Giao diện chung) ---
# Đây là "ngôn ngữ chung" mà cả File và Folder đều phải "nói".
class IFileSystemComponent(ABC):
    """
    Định nghĩa các hoạt động chung cho cả đối tượng đơn giản (File)
    và phức tạp (Folder).
    """
    @abstractmethod
    def get_size(self) -> int:
        """Trả về kích thước của thành phần (tính bằng KB)."""
        pass

# --- 2. The Leaf (Đối tượng "Lá") ---
# Đây là đối tượng riêng lẻ, cơ bản của hệ thống. Nó không có "con".
class File(IFileSystemComponent):
    def __init__(self, name: str, size: int):
        self._name = name
        self._size = size

    def get_size(self) -> int:
        # Đối với một file, việc lấy kích thước rất đơn giản: chỉ cần trả về kích thước của nó.
        print(f"  (File '{self._name}', size: {self._size}KB)")
        return self._size
    
    # def __str__(self):
    #     return self.name

# --- 3. The Composite (Đối tượng "Nhóm" hay "Phức hợp") ---
# Đây là đối tượng có thể chứa các đối tượng "Lá" hoặc các "Nhóm" khác.
class Folder(IFileSystemComponent):
    def __init__(self, name: str):
        self._name = name
        self._children: List[IFileSystemComponent] = []

    def add(self, component: IFileSystemComponent) -> None:
        self._children.append(component)

    def remove(self, component: IFileSystemComponent) -> None:
        self._children.remove(component)

    """thông qua cơ chế delegation và recursion"""
    def get_size(self) -> int:
        # Đây là nơi phép màu của Composite xảy ra.
        # Kích thước của một thư mục bằng TỔNG kích thước của tất cả các thành phần con bên trong nó.
        print(f"--- Calculating size for Folder '{self._name}' ---")
        total_size = 0
        for child in self._children:
            # Nó gọi đệ quy get_size() trên từng thành phần con.
            # Nó không cần quan tâm 'child' là File hay Folder, vì cả hai đều có phương thức này.
            total_size += child.get_size()
        
        print(f"--- Total size for Folder '{self._name}' is {total_size}KB ---")
        return total_size
    
    # def __str__(self):
    #     return list(self._children)

# --- 4. The Client Code ---
if __name__ == "__main__":
    # Tạo các đối tượng "Lá" (Files)
    file1 = File("resume.docx", 150)
    file2 = File("photo.jpg", 500)
    file3 = File("archive.zip", 2048)
    file4 = File("song.mp3", 4096)

    # Tạo các đối tượng "Nhóm" (Folders)
    # và xây dựng một cấu trúc cây
    subfolder1 = Folder("Work")
    subfolder1.add(file1)

    subfolder2 = Folder("Private")
    subfolder2.add(file2)
    subfolder2.add(file4)

    root_folder = Folder("MyDocuments")
    root_folder.add(subfolder1)
    root_folder.add(subfolder2)
    root_folder.add(file3)
    
    print("="*30)
    # Client có thể đối xử với tất cả các thành phần một cách như nhau.
    
    # Lấy kích thước của một file đơn lẻ
    print(f"Kích thước của file2 là: {file2.get_size()}KB\n")

    # Lấy kích thước của cả một thư mục con
    # Client không cần biết bên trong subfolder2 có gì, chỉ cần gọi get_size()
    print(f"Tổng kích thước của subfolder2 là: {subfolder2.get_size()}KB\n")
    
    # Lấy kích thước của toàn bộ cây thư mục
    print(f"Tổng kích thước của thư mục gốc là: {root_folder.get_size()}KB")