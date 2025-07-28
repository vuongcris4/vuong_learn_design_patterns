"""
Visitor Interface: Định nghĩa một phương thức visit() cho mỗi loại Element cụ thể. 
    Ví dụ: visit_circle(), visit_square()
Concrete Visitor: Triển khai các phương thức visit(). Mỗi visitor đại diện cho một
    hoạt động mới mà bạn muốn thêm vào (vd: AreaCalculator, XmlExporter)
Element Interface: Định nghĩa một phương thức accept (visitor)
Concrete Element: Các lớp trong hệ thống (Circle, Square). Chúng triển khai phương thức accept
"""

from __future__ import annotations
from abc import ABC, abstractmethod

# --- Hệ thống phân cấp Visitor ---

class IShapeVisitor(ABC):
    """
    Giao diện Visitor. Khai báo một phương thức visit cho mỗi lớp Concrete Element.
    """
    @abstractmethod
    def visit_circle(self, element: Circle):
        pass

    @abstractmethod
    def visit_square(self, element: Square):
        pass

# --- Hệ thống phân cấp Element ---

class IShape(ABC):
    """Giao diện Element. Khai báo một phương thức accept."""
    @abstractmethod
    def accept(self, visitor: IShapeVisitor):
        pass

# --- Concrete Elements ---
# Các lớp này đã ổn định và chúng ta không muốn sửa đổi chúng.

class Circle(IShape):
    def __init__(self, radius: int):
        self.radius = radius

    def accept(self, visitor: IShapeVisitor):
        """Đây là bước Double Dispatch thứ hai."""
        visitor.visit_circle(self)

class Square(IShape):
    def __init__(self, side: int):
        self.side = side

    def accept(self, visitor: IShapeVisitor):
        visitor.visit_square(self)

# --- Concrete Visitors ---
# Mỗi visitor triển khai một hoạt động mới.

class AreaCalculator(IShapeVisitor):
    """Visitor này tính tổng diện tích của tất cả các hình."""
    def __init__(self):
        self.total_area = 0

    def visit_circle(self, element: Circle):
        self.total_area += 3.14 * (element.radius ** 2)

    def visit_square(self, element: Square):
        self.total_area += element.side ** 2

class XmlExporter(IShapeVisitor):
    """Visitor này "xuất" các hình ra dạng XML."""
    def __init__(self):
        self.xml_output = ""

    def visit_circle(self, element: Circle):
        self.xml_output += f"  <circle radius=\"{element.radius}\" />\n"

    def visit_square(self, element: Square):
        self.xml_output += f"  <square side=\"{element.side}\" />\n"

# --- Client Code ---
if __name__ == "__main__":
    shapes: list[IShape] = [Circle(10), Square(5), Circle(3)]
    
    print("--- Thêm hoạt động TÍNH DIỆN TÍCH mà không sửa đổi các lớp Shape ---")
    area_calculator = AreaCalculator()
    for shape in shapes:
        # Client gọi accept trên shape, và truyền visitor vào.
        shape.accept(area_calculator)
    
    print(f"Tổng diện tích là: {area_calculator.total_area}")

    print("\n" + "="*50 + "\n")
    
    print("--- Thêm hoạt động XUẤT XML mà không sửa đổi các lớp Shape ---")
    xml_exporter = XmlExporter()
    for shape in shapes:
        shape.accept(xml_exporter)

    print("<shapes>\n" + xml_exporter.xml_output + "</shapes>")