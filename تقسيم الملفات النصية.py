import os

def split_and_save_text_chunks(file_path, output_dir, chunk_size=500):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    words = text.split()
    # أنشئ المجلد إذا لم يكن موجودًا
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(0, len(words), chunk_size):
        chunk_words = words[i:i+chunk_size]
        chunk_text = " ".join(chunk_words)
        # تسمية ملف الإخراج
        out_file_name = f"chunk_{i//chunk_size + 1}.txt"
        out_file_path = os.path.join(output_dir, out_file_name)
        
        with open(out_file_path, 'w', encoding='utf-8') as out_f:
            out_f.write(chunk_text)

# مثال على الاستخدام
file_path = r"C:\Users\Aymen\Desktop\My_Book\الرد على المنطقيين.txt"
output_dir = r"C:\Users\Aymen\Desktop\My_Book\chunks"
split_and_save_text_chunks(file_path, output_dir, 500)
