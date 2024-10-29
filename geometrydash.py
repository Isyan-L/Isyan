import pygame
import sys
import random

pygame.init()

# Konstanta
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Warna rintangan
YELLOW = (255, 255, 0)  # Warna karakter kuning
ORANGE = (255, 165, 0)  # Warna karakter oranye
GREEN = (0, 255, 0)  # Warna karakter hijau
PINK = (255, 20, 147)  # Warna karakter pink
PURPLE = (128, 0, 128)  # Warna karakter ungu

# Mengatur layar
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Geometry Dash Clone')
CLOCK = pygame.time.Clock()

# Memuat gambar latar belakang
background_img = pygame.image.load('bd.jpeg')
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Sesuaikan ukuran latar belakang
selection_background_img = pygame.image.load('lay.jpeg')  # Memuat gambar latar belakang untuk pemilihan warna
selection_background_img = pygame.transform.scale(selection_background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Sesuaikan ukuran
main_background_img = pygame.image.load('lay1.jpeg')  # Latar belakang untuk layout pertama
main_background_img = pygame.transform.scale(main_background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Sesuaikan ukuran
level_background_img = pygame.image.load('lay2.jpeg')  # Latar belakang untuk layout kedua
level_background_img = pygame.transform.scale(level_background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Sesuaikan ukuran

# Kelas Pemain
class Player:
    def __init__(self, color, speed):
        self.rect = pygame.Rect(100, WINDOW_HEIGHT - 70, 50, 50)  # Posisi dan ukuran kotak
        self.velocity_y = 0
        self.jumping = False
        self.jump_count = 0  # Menambahkan hitungan lompatan
        self.color = color  # Menyimpan warna karakter
        self.speed = speed  # Kecepatan karakter

    def jump(self):
        # Mengizinkan lompatan jika karakter belum mencapai batas maksimum
        if self.jump_count < 2:  # Maksimal 2 lompatan
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True
            self.jump_count += 1

    def update(self):
        # Mengaplikasikan gravitasi
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Menghentikan pemain di tanah
        if self.rect.y >= WINDOW_HEIGHT - 70:
            self.rect.y = WINDOW_HEIGHT - 70
            self.jumping = False
            self.jump_count = 0  # Reset hitungan lompatan saat menyentuh tanah

    def draw(self):
        pygame.draw.rect(canvas, self.color, self.rect)  # Mengganti warna karakter sesuai pilihan

# Kelas Rintangan
class Obstacle:
    def __init__(self, speed):
        self.rect = pygame.Rect(WINDOW_WIDTH, WINDOW_HEIGHT - 70, 30, 50)  # Memperkecil lebar rintangan menjadi 30
        self.speed = speed  # Kecepatan rintangan

    def update(self):
        self.rect.x -= self.speed  # Bergerak ke kiri dengan kecepatan yang ditentukan

    def draw(self):
        pygame.draw.rect(canvas, BLUE, self.rect)  # Mengganti warna rintangan menjadi biru

# Fungsi untuk menampilkan layout utama
def show_main_menu():
    while True:
        canvas.blit(main_background_img, (0, 0))  # Menggambar latar belakang layout utama
        
        # Menampilkan judul game
        font = pygame.font.SysFont('Arial', 72)
        title_surface = font.render('GEOMETRY DASH', True, PURPLE)
        canvas.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 200))

        # Menampilkan pencipta game
        creator_surface = font.render('ISYAN LEREK', True, PURPLE)
        canvas.blit(creator_surface, (WINDOW_WIDTH // 2 - creator_surface.get_width() // 2, 300))

        # Menampilkan tombol MAIN
        main_button_surface = font.render('MAIN', True, BLACK)
        main_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 400, 200, 50)
        pygame.draw.rect(canvas, WHITE, main_button_rect)
        canvas.blit(main_button_surface, (main_button_rect.x + 20, main_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if main_button_rect.collidepoint(mouse_x, mouse_y):
                    return  # Kembali ke layout pilihan level

        pygame.display.update()
        CLOCK.tick(FPS)

# Fungsi untuk menampilkan pilihan level
def show_level_selection():
    while True:
        canvas.blit(level_background_img, (0, 0))  # Menggambar latar belakang layout level
        
        # Menampilkan pilihan level
        font = pygame.font.SysFont('Arial', 36)
        title_surface = font.render('Pilih Level:', True, WHITE)
        canvas.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 50))

        # Menampilkan tombol level
        levels = [("Level 1", 5), ("Level 2", 10), ("Level 3", 15), ("Level 4", 20), ("Level 5", 25)]
        level_buttons = []
        for index, (level_name, speed) in enumerate(levels):
            button_surface = font.render(level_name, True, BLACK)
            button_rect = pygame.Rect(150, 150 + index * 60, 500, 50)
            pygame.draw.rect(canvas, WHITE, button_rect)
            canvas.blit(button_surface, (button_rect.x + 20, button_rect.y + 10))
            level_buttons.append((button_rect, speed))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for button_rect, speed in level_buttons:
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        return speed  # Kembali dengan kecepatan level yang dipilih

        pygame.display.update()
        CLOCK.tick(FPS)

# Fungsi untuk menampilkan layar pemilihan warna
def show_color_selection():
    selected_color = YELLOW  # Warna default
    while True:
        canvas.blit(selection_background_img, (0, 0))  # Menggambar latar belakang pemilihan warna
        
        # Menampilkan teks
        font = pygame.font.SysFont('Arial', 36)
        title_surface = font.render('Pilih Warna Karakter:', True, WHITE)
        canvas.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 50))

        # Menampilkan pilihan warna
        colors = [(YELLOW, "Kuning"), (ORANGE, "Oranye"), (GREEN, "Hijau"), (PINK, "Pink"), (PURPLE, "Ungu")]
        for index, (color, name) in enumerate(colors):
            pygame.draw.rect(canvas, color, (150 + index * 120, 200, 100, 50))  # Menampilkan kotak warna
            color_text = font.render(name, True, BLACK)
            canvas.blit(color_text, (150 + index * 120 + 10, 210))  # Menampilkan nama warna

            # Menambahkan tanda untuk warna yang dipilih
            if color == selected_color:
                pygame.draw.rect(canvas, BLACK, (150 + index * 120, 200, 100, 50), 3)  # Menambahkan border hitam pada pilihan yang dipilih

        # Menampilkan tombol Start
        start_button_surface = font.render('Start', True, BLACK)  # Tulisan pada tombol Start
        start_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, 350, 100, 50)
        pygame.draw.rect(canvas, WHITE, start_button_rect)
        canvas.blit(start_button_surface, (start_button_rect.x + 10, start_button_rect.y + 10))

        # Menampilkan tombol Exit
        exit_button_surface = font.render('Exit', True, BLACK)  # Tulisan pada tombol Exit
        exit_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, 420, 100, 50)
        pygame.draw.rect(canvas, WHITE, exit_button_rect)
        canvas.blit(exit_button_surface, (exit_button_rect.x + 10, exit_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Tekan ESC untuk keluar
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Cek jika klik pada pilihan warna
                for index, (color, _) in enumerate(colors):
                    if 150 + index * 120 <= mouse_x <= 150 + index * 120 + 100 and 200 <= mouse_y <= 250:
                        selected_color = color
                # Cek jika klik pada tombol Start
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    return selected_color  # Kembali dengan warna yang dipilih
                # Cek jika klik pada tombol Exit
                if exit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # Keluar dari aplikasi

        pygame.display.update()
        CLOCK.tick(FPS)

# Fungsi untuk menjalankan game
def game_loop(player_color, player_speed):
    player = Player(player_color, player_speed)
    obstacles = []
    score = 0

    while True:
        canvas.blit(background_img, (0, 0))  # Menggambar latar belakang

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Update dan gambar pemain
        player.update()
        player.draw()

        # Menambah rintangan
        if random.randint(1, 100) <= 2:  # 2% peluang untuk menambah rintangan
            obstacles.append(Obstacle(player.speed))  # Menggunakan kecepatan karakter untuk rintangan

        # Update dan gambar rintangan
        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw()
            # Hapus rintangan yang sudah keluar dari layar
            if obstacle.rect.x < -50:
                obstacles.remove(obstacle)
                score += 1  # Tambah skor saat berhasil melewati rintangan

            # Cek tabrakan
            if player.rect.colliderect(obstacle.rect):
                show_game_over_message(score)  # Tampilkan pesan kalah
                return  # Mengembalikan ke layar pemilihan warna

        # Gambar skor
        font = pygame.font.SysFont('Arial', 24)
        score_surface = font.render(f'Score: {score}', True, WHITE)
        canvas.blit(score_surface, (10, 10))

        pygame.display.update()
        CLOCK.tick(FPS)

# Fungsi untuk menampilkan pesan game over
def show_game_over_message(score):
    font = pygame.font.SysFont('Arial', 48)
    message_surface = font.render('Kamu Kalah!', True, WHITE)
    score_surface = font.render(f'Skor Anda: {score}', True, WHITE)

    # Menampilkan pesan di tengah layar
    while True:
        canvas.blit(background_img, (0, 0))  # Menggambar latar belakang
        canvas.blit(message_surface, (WINDOW_WIDTH // 2 - message_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
        canvas.blit(score_surface, (WINDOW_WIDTH // 2 - score_surface.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
        
        pygame.display.update()
        CLOCK.tick(FPS)

        # Tunggu selama 1 detik
        pygame.time.delay(1000)

        # Kembali ke layar pemilihan warna setelah 1 detik
        break

# Menjalankan game
while True:
    show_main_menu()  # Menampilkan layout utama
    player_speed = show_level_selection()  # Menampilkan layar pilihan level dan mendapatkan kecepatan
    selected_color = show_color_selection()  # Menampilkan layar pemilihan warna
    game_loop(selected_color, player_speed)  # Memulai game dengan warna dan kecepatan yang dipilih