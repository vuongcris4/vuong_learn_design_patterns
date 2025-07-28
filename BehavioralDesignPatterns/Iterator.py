from collections.abc import Iterable, Iterator

# --- 1. The Iterator (Đối tượng "con trỏ" duyệt) ---
# Lớp này chứa logic của việc duyệt qua tập hợp.
"""
Iterator: Là con trỏ hay ngón tay chỉ vào từng phần tử. Nó chứa logic của việc duyệt.
nó biết phần tử hiện tại là gì _position
làm thế nào để đi tới phần tử tiếp theo
và khi nào kết thúc StopIteration
"""
class AlphabeticalOrderIterator(Iterator):
    def __init__(self, collection: 'WordCollection', reverse: bool = False):
        self._collection = collection._words
        self._reverse = reverse
        # Vị trí hiện tại của con trỏ duyệt
        self._position: int = -1 if reverse else 0

    def __next__(self):
        """
        Phương thức này được vòng lặp 'for' gọi liên tục.
        Nó trả về phần tử tiếp theo trong tập hợp.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            # Khi không còn phần tử, ném ra StopIteration để báo hiệu kết thúc.
            raise StopIteration()
        
        return value

# --- 2. The Aggregate (Đối tượng "chứa" dữ liệu) ---
# Lớp này chứa dữ liệu và có khả năng tạo ra các iterator.
"""
Aggregate/Iterable là cái thùng chứa dữ liệu. Nhiệm vụ chính của nó là cung cấp
một hoặc nhiều cách để duyệ qua dữ liệu đó bằng cách trả về một đối tượng Iterator
từ phương thức __iter__()
"""
class WordCollection(Iterable):
    def __init__(self):
        self._words: list[str] = []

    def add_word(self, word: str):
        self._words.append(word)

    def __iter__(self) -> AlphabeticalOrderIterator:
        """
        Đây là phương thức được gọi khi vòng lặp 'for' bắt đầu.
        Nó trả về một đối tượng iterator mới.
        """
        # Sắp xếp các từ trước khi duyệt
        self._words.sort()
        return AlphabeticalOrderIterator(self)
    
    def get_reverse_iterator(self) -> AlphabeticalOrderIterator:
        """Cung cấp một cách duyệt khác."""
        self._words.sort()
        return AlphabeticalOrderIterator(self, reverse=True)


# --- 3. The Client Code ---
if __name__ == "__main__":
    # Tạo một tập hợp
    collection = WordCollection()
    collection.add_word("First")
    collection.add_word("Third")
    collection.add_word("Second")
    collection.add_word("Fourth")

    print("--- Duyệt xuôi theo thứ tự bảng chữ cái ---")
    # Client chỉ cần dùng vòng lặp for một cách tự nhiên.
    # Python sẽ tự động gọi collection.__iter__() để lấy iterator.
    for word in collection:
        print(word)

    print("\n--- Duyệt ngược theo thứ tự bảng chữ cái ---")
    # Client có thể yêu cầu một kiểu duyệt khác.
    for word in collection.get_reverse_iterator():
        print(word)

    print("\n--- Hiểu rõ hơn về cách 'for' hoạt động ---")
    # Vòng lặp for thực chất làm những việc sau:
    # 1. Lấy iterator từ tập hợp
    my_iterator = iter(collection) # Tương đương collection.__iter__()
    
    # 2. Liên tục gọi next() trên iterator
    print(f"Phần tử đầu tiên: {next(my_iterator)}") # Tương đương my_iterator.__next__()
    print(f"Phần tử thứ hai: {next(my_iterator)}")
    
    # 3. Cho đến khi gặp StopIteration thì dừng lại
    try:
        while True:
            print(f"Phần tử tiếp theo: {next(my_iterator)}")
    except StopIteration:
        print("Đã duyệt hết các phần tử.")