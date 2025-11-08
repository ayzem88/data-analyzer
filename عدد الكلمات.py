class TextAnalyzer:
    def __init__(self, file_path):
        """قم بتهيئة المحلل مع مسار الملف"""
        self.file_path = file_path
        self.tokens = []

    def read_file(self):
        """قم بقراءة الملف وتخزين البيانات في قائمة التوكنز"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # تقسيم السطر إلى توكنز بناءً على المسافات
                    self.tokens.extend(line.split())
        except FileNotFoundError:
            print("الملف المطلوب غير موجود")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {e}")

    def count_tokens(self):
        """إرجاع عدد التوكنز الموجودة في الملف"""
        return len(self.tokens)

# استخدام الكلاس
if __name__ == "__main__":
    analyzer = TextAnalyzer("كتاب.txt")
    analyzer.read_file()
    print(f"عدد التوكنز في الملف: {analyzer.count_tokens()}")
