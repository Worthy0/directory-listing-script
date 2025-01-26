import os

def list_directory_to_file(path, file, show_hidden=False, prefix=""):
    total_files = 0
    total_dirs = 0
    try:
        items = sorted(os.listdir(path))  # Klasördeki dosyaları ve klasörleri sırala
        for item in items:
            if not show_hidden and item.startswith("."):  # Gizli dosyaları atla
                continue
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # Klasör ise yaz ve içeriği yinelemeli olarak ekle
                file.write(f"{prefix}├── {item}/\n")
                sub_files, sub_dirs = list_directory_to_file(item_path, file, show_hidden, prefix + "│   ")
                total_files += sub_files
                total_dirs += sub_dirs + 1  # Kendisi de bir klasör
            else:
                # Dosya ise yaz
                file.write(f"{prefix}├── {item}\n")
                total_files += 1
    except PermissionError:
        file.write(f"{prefix}├── [Permission Denied]\n")
    except FileNotFoundError:
        file.write(f"{prefix}├── [Not Found]\n")
    return total_files, total_dirs

def main():
    print("Hangi dizini listelemek istiyorsunuz? (Varsayılan: Desktop)")
    directory = input("Dizin yolu: ").strip()

    if not directory:
        # Varsayılan olarak Desktop dizinini kullan
        directory = os.path.join(os.path.expanduser("~"), "Desktop")

    if not os.path.exists(directory):
        print("Geçersiz bir dizin yolu girdiniz!")
        return

    # Kullanıcıdan gizli dosyaların gösterilmesini isteyip istemediğini sor
    while True:
        choice = input("Gizli dosyaları göstermek istiyor musunuz? (e/h): ").strip().lower()
        if choice in ["e", "h"]:
            show_hidden = (choice == "e")
            break
        else:
            print("Lütfen sadece 'e' (evet) veya 'h' (hayır) harflerini kullanın.")

    output_file = os.path.join(directory, "directory_list.txt")

    # Dosyayı hem okuma hem yazma modunda aç
    with open(output_file, "w+", encoding="utf-8") as file:
        # Dizin adını başa ekle
        file.write(f"{directory}/\n")
        total_files, total_dirs = list_directory_to_file(directory, file, show_hidden)

        # Toplam dosya ve klasör sayısını en üste ekle
        file.seek(0, 0)  # Dosyanın başına git
        summary = (
            f"Toplam dosya sayısı: {total_files}\n"
            f"Toplam klasör sayısı: {total_dirs}\n"
            "-----------------------------------\n"
        )
        content = file.read()  # Yazılan mevcut içeriği oku
        file.seek(0, 0)  # Tekrar başa git
        file.write(summary + content)  # Özet bilgisini başa ekle

    print(f"Dizin çıktısı '{output_file}' dosyasına kaydedildi.")
    print(f"Toplam dosya sayısı: {total_files}")
    print(f"Toplam klasör sayısı: {total_dirs}")

if __name__ == "__main__":
    main()
