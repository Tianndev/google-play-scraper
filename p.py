from rich.panel import Panel as panel
from rich import print as prints
from google_play_scraper import *
import random,time,os,csv,sys
from datetime import datetime,timezone
from rich.console import Console

rc = random.choice
rr = random.randint
console = Console()

###-----[ MENU WARNA PRINT RICH ]-----###
RED = "[#FF0000]"
GREEN = "[#00FF00]"
BLUE = "[#0000FF]"
YELLOW = "[#FFFF00]"
CYAN = "[#00FFFF]"
MAGENTA = "[#FF00FF]"
ORANGE = "[#FFA500]"
PINK = "[#FF1493]"
PURPLE = "[#800080]"
WHITE = "[#FFFFFF]"
BLACK = "[#000000]"
DARK_BLUE = "[#000080]"
LIGHT_GREEN = "[#90EE90]"
LIGHT_YELLOW = "[#FFFFE0]"
LIGHT_CYAN = "[#E0FFFF]"
LIGHT_MAGENTA = "[#FF77FF]"
LIGHT_ORANGE = "[#FFD700]"
LIGHT_PINK = "[#FFB6C1]"
LIGHT_PURPLE = "[#BA55D3]"
LIGHT_GRAY = "[#D3D3D3]"
DARK_GREEN = "[#006400]"

cocote = rc([
    RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PINK, PURPLE, BLACK,
    DARK_BLUE, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_CYAN, LIGHT_MAGENTA,
    LIGHT_ORANGE, LIGHT_PINK, LIGHT_PURPLE, LIGHT_GRAY, DARK_GREEN
])

warr = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, PINK, PURPLE, LIGHT_GREEN]

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def print_reviews_to_csv(reviews, app_id):
    filename = f"reviews_{app_id}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Username', 'Rating', 'Comment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for review in reviews:
            username = review['userName']
            star_rating = int(review.get('score', 0))
            bintang = "★" * star_rating + "☆" * (5 - star_rating)
            comment = review.get('content', '').strip()
            if not comment:
                comment = "Pelanggan tidak memberikan ulasan"
            writer.writerow({'Username': username, 'Rating': bintang, 'Comment': comment})
    return filename

def print_panel():
    clear()
    text = rf"""{GREEN}
       _______                      ____                __ 
      /_  __(_)___ _____  ____     / __ \___ _   __   _/ _)
       / / / / __ `/ __ \/ __ \   / / / / _ \ | / /  / | | 
      / / / / /_/ / / / / / / /  / /_/ /  __/ |/ /  | || | 
     /_/ /_/\__,_/_/ /_/_/ /_/  /_____/\___/|___/   | |_/
                                                   (___/)    
                                                  
{WHITE} [ Script For {RED}Google Play Store{WHITE} Scraper | Developed By {LIGHT_ORANGE}Tiann Dev[bold blue]𓄀[/] {WHITE}]"""

    prints(panel(text, title="[white](⁠╥⁠﹏⁠╥⁠)[/]", style="bold white"))

    # Options
    options = [
        "[1] Cari Aplikasi di Google Play Store",
        "[2] Dapatkan Detail Aplikasi",
        "[3] Lihat & Simpan Ulasan Aplikasi",
        "[4] Izin yang Diminta oleh Aplikasi",
        "[0] Keluar"
    ]

    prints(panel("\n".join(options), title="Main Menu", style="bold white"))

# Main function
def main():
    while True:
        print_panel()
        choice = input(f"[%] Masukkan pilihan Anda: ")

        if choice == '1':
            prints(panel(f"{RED}Harap untuk menyalin Package ID dari aplikasi yang Anda pilih di Google Play Store untuk keperluan selanjutnya.\nContoh query Pencarian: {GREEN}Instagram", title=f"[yellow]Warning!", style="bold white"))
            query = input(f"[%] Masukkan Query pencarian: ")
            results = search(query)
            for idx, result in enumerate(results, start=1):
                panel_text = f"Nama: {GREEN}{result['title']}\n{WHITE}Package Id: {GREEN}{result['appId']}{WHITE}"
                prints(panel(panel_text, title=f"{idx}", style="bold white"))
            prints(panel(panel(f"Proses telah selesai, Silakan jalankan ulang program untuk menggunakan kembali fitur-fitur ini. {LIGHT_ORANGE}@tiann_dev", title="Selesai [bold green]✓[/]", style="bold white")))
            break
        elif choice == '2':
            prints(panel(f"{RED}Harap masukkan Package ID dari aplikasi yang Anda pilih di Google Play Store, bukan nama aplikasi.\nContoh Package ID: {GREEN}com.instagram.android", title="[yellow]Warning!", style="bold white"))
            app_id = input("[%] Masukkan ID aplikasi Google Play Store: ")
            result = app(app_id)
            categories = ', '.join(category['name'] for category in result.get('categories', [])) or 'Not found'
            prints(panel(
                f"{WHITE}Nama Aplikasi: {GREEN}{result.get('title', 'Not found')}\n"
                f"{WHITE}Deskripsi: {GREEN}{result.get('summary', 'Not found')}\n"
                f"{WHITE}Jumlah instalasi Aplikasi: {GREEN}{result.get('installs', 'Not found')}\n"
                f"{WHITE}Jumlah instalasi minimum: {GREEN}{result.get('minInstalls', 'Not found'):,.0f}\n"
                f"{WHITE}Jumlah instalasi sebenarnya: {GREEN}{result.get('realInstalls', 'Not found')}\n"
                f"{WHITE}Nilai rata-rata peringkat aplikasi: {GREEN}{result.get('score', 'Not found')}\n"
                f"{WHITE}Jumlah peringkat yang diterima: {GREEN}{result.get('ratings', 'Not found'):,.0f}\n"
                f"{WHITE}Jumlah ulasan yang diterima: {GREEN}{result.get('reviews', 'Not found'):,.0f}\n"
                f"{WHITE}Histogram peringkat: {GREEN}{', '.join(map(str, result.get('histogram', 'Not found')))}\n"
                f"{WHITE}Harga aplikasi dalam mata uang: {GREEN}{result.get('price', 'Not found')}\n"
                f"{WHITE}Apakah aplikasi gratis?: {GREEN}{'Iya' if result.get('free', False) else 'Tidak'}\n"
                f"{WHITE}Mata uang aplikasi: {GREEN}{result.get('currency', 'Not found')}\n"
                f"{WHITE}Apakah aplikasi sedang dalam penawaran?: {GREEN}{'Iya' if result.get('sale', False) else 'Tidak'}\n"
                f"{WHITE}Apakah aplikasi menawarkan pembelian dalam aplikasi?: {GREEN}{'Iya' if result.get('offersIAP', False) else 'Tidak'}\n"
                f"{WHITE}Kisaran harga untuk pembelian dalam aplikasi: {GREEN}{result.get('inAppProductPrice', 'Not found')}\n"
                f"{WHITE}Nama pengembang: {GREEN}{result.get('developer', 'Not found')}\n"
                f"{WHITE}ID pengembang: {GREEN}{result.get('developerId', 'Not found')}\n"
                f"{WHITE}Email pengembang: {GREEN}{result.get('developerEmail', 'Not found')}\n"
                f"{WHITE}Situs web pengembang: {GREEN}{result.get('developerWebsite', 'Not found')}\n"
                f"{WHITE}Alamat pengembang: {GREEN}{result.get('developerAddress', 'Not found')}\n"
                f"{WHITE}Tautan ke kebijakan privasi aplikasi: {GREEN}{result.get('privacyPolicy', 'Not found')}\n"
                f"{WHITE}Genre aplikasi: {GREEN}{result.get('genre', 'Not found')}\n"
                f"{WHITE}Kategori-kategori aplikasi: {GREEN}{categories}\n"
                f"{WHITE}URL ikon aplikasi: {GREEN}{result.get('icon', 'Not found')}\n"
                f"{WHITE}Rating konten aplikasi: {GREEN}{result.get('contentRating', 'Not found')}\n"
                f"{WHITE}Apakah aplikasi didukung oleh iklan?: {GREEN}{'Iya' if result.get('adSupported', False) else 'Tidak'}\n"
                f"{WHITE}Apakah aplikasi mengandung iklan?: {GREEN}{'Iya' if result.get('containsAds', False) else 'Tidak'}\n"
                f"{WHITE}Tanggal rilis aplikasi: {GREEN}{result.get('released', 'Not found')}\n"
                f"{WHITE}Waktu terakhir aplikasi diperbarui: {GREEN}{datetime.fromtimestamp(int(result.get('updated', 'Not found')), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S') if result.get('updated', 'Not found') != 'Not found' else 'Not found'}\n"
                f"{WHITE}Versi aplikasi: {GREEN}{result.get('version', 'Not found') if result is not None else 'Not found'}\n"
                f"{WHITE}Package Id aplikasi: {GREEN}{result.get('appId', 'Not found')}\n"
                f"{WHITE}URL Google Play Store aplikasi: {GREEN}{result.get('url', 'Not found')}\n",
                title="Detail Aplikasi", style="bold cyan"
            ))
            break
        elif choice == '3':
            prints(panel(f"{RED}Masukan package id aplikasi yang akan anda lihat & simpan ulasannya\nContoh Package ID: {GREEN}com.instagram.android", title="[yellow]Warning!", style="bold white"))
            app_id = input("Masukkan ID aplikasi Google Play Store: ")
            
            result, _ = reviews(
                app_id,
                lang='id',
                count=1000
            )
            if not result:
                frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧']
                with console.status("[bold cyan]Mengumpulkan ulasan...") as status:
                    while not result:
                        for frame in frames:
                            time.sleep(1)
                            console.print(f"\r{frame} Mengumpulkan ulasan...", end="")

            prints(panel(f"[bold green]Ulasan berhasil dikumpulkan!", style="bold white"))  
            idx = 0
            for review in result:
                username = review['userName']
                star_rating = int(review.get('score', 0))
                bintang = "★" * star_rating + "☆" * (5 - star_rating)
                comment = review.get('content', '').strip()
                if not comment:
                    comment = "Pelanggan tidak memberikan ulasan"
                idx += 1
                prints(panel(f"{WHITE}Username: {GREEN}{username}\n{WHITE}Rating: {YELLOW}{bintang}\n{WHITE}Comment: {GREEN}{comment}\n", title=f"{idx}", style="bold white"))
            prints(panel(f"{WHITE}Apakah Anda ingin mencetak ulasan ke file CSV?", title=f"[yellow]Konfirmasi?", style="bold white"))
            if input(" Pilih: (y/n): ").strip().lower() == 'y':
                filename = print_reviews_to_csv(result, app_id)
                prints(panel(f"{GREEN}Ulasan telah dicetak ke file CSV: {filename}", title=f"[green]Sukses", style="bold white"))
            break
        elif choice == '4':
            prints(panel(f"{RED}Masukkan package id aplikasi yang akan anda lihat permissionnya\nContoh Package ID: {GREEN}com.instagram.android", title="[yellow]Warning!", style="bold white"))
            while True:
                app_id = input(f"[%] Masukkan ID aplikasi Google Play Store: ")
                result = permissions(app_id,
                    lang='id',
                    country='id'
                )
                if result:
                    formatted_permissions = "\n".join([f"{WHITE}{key}:{PINK} {', '.join(value)}" for key, value in result.items()])
                    permission_panel_text = f"Permissions yang diminta oleh {GREEN}{app_id}:\n\n{formatted_permissions}"
                    prints(panel(permission_panel_text, title="[bold cyan]Permissions[/]", style="bold white"))
                    break
                else:
                    prints(panel(f"{RED}[!] ID aplikasi tidak valid atau tidak ditemukan. Silakan coba lagi.", title="[yellow]Error[/]", style="bold white"))
            break

        elif choice == '0':
            prints(panel(f"{GREEN}Selamat Tinggal ...", title="[green]Good Bye[/]", style="bold white"))
            break
        else:
            prints(panel(f"{RED}[!] Pilihan Tidak Valid!. Silakan coba lagi.", title="[yellow]Error[/]", style="bold white"))
            time.sleep(3)

if __name__ == "__main__":
    main()
