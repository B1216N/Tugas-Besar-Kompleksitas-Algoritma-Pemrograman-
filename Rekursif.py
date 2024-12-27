def detect_anomalies(player_stats):
    """
    Deteksi anomali seperti wallhack atau auto kill berdasarkan data statistik pemain.

    Parameters:
    player_stats (dict): Data statistik pemain, misalnya {
        "player_name": "Player1",
        "shots_fired": 100,
        "kills": 95,
        "visible_enemies": 20
    }.

    Returns:
    tuple: Pesan apakah ada anomali atau tidak, dan nama pemain jika terdeteksi curang.
    """
    player_name = player_stats.get("player_name", "Unknown")
    shots_fired = player_stats.get("shots_fired", 0)
    kills = player_stats.get("kills", 0)
    visible_enemies = player_stats.get("visible_enemies", 0)

    # Deteksi anomali
    if visible_enemies > 0 and kills > visible_enemies:
        return f"Peringatan: {player_name} terdeteksi menggunakan wallhack dan menjadi suspect melakukan cheat!", player_name
    if shots_fired > 0 and kills / shots_fired > 0.8:
        return f"Peringatan: {player_name} terdeteksi menggunakan auto kill dan menjadi suspect melakukan cheat!", player_name

    return f"{player_name} tidak terdeteksi melakukan kecurangan.", None

def update_suspected_cheaters(player_stats, suspected_cheaters):
    """
    Perbarui daftar suspected_cheaters berdasarkan hasil deteksi anomali.

    Parameters:
    player_stats (dict): Data statistik pemain.
    suspected_cheaters (set): Set pemain yang dicurigai melakukan kecurangan.

    Returns:
    str: Pesan hasil deteksi.
    """
    message, cheater = detect_anomalies(player_stats)
    if cheater:
        suspected_cheaters.add(cheater)
    return message

def search_anomaly_recursive(player_name, stats_list, suspected_cheaters, index=0):
    """
    Fungsi rekursif untuk mencari pemain tertentu dalam daftar statistik dan memeriksa anomali mereka.

    Parameters:
    player_name (str): Nama pemain yang akan diperiksa.
    stats_list (list): Daftar statistik semua pemain.
    suspected_cheaters (set): Set pemain yang dicurigai melakukan kecurangan.
    index (int): Indeks saat ini dalam daftar statistik.

    Returns:
    str: Pesan hasil pencarian dan deteksi anomali.
    """
    if index >= len(stats_list):  # Basis rekursi: jika indeks melebihi panjang daftar
        return f"Pemain {player_name} tidak ditemukan dalam daftar statistik."
    
    stats = stats_list[index]
    if stats.get("player_name") == player_name:
        return update_suspected_cheaters(stats, suspected_cheaters)
    
    # Rekursi: Lanjutkan pencarian di indeks berikutnya
    return search_anomaly_recursive(player_name, stats_list, suspected_cheaters, index + 1)

# Daftar pemain yang dicurigai melakukan kecurangan (contoh)
suspected_cheaters = set(["Player1"])

# Daftar statistik pemain (contoh)
stats_list = [
    {"player_name": "Player1", "shots_fired": 100, "kills": 95, "visible_enemies": 20},
    {"player_name": "Player2", "shots_fired": 80, "kills": 10, "visible_enemies": 15},
    {"player_name": "Player3", "shots_fired": 50, "kills": 50, "visible_enemies": 5},
]

# Input nama pemain yang ingin diperiksa
player_name = input("Masukkan nama pemain untuk diperiksa: ")

# Pencarian dan deteksi anomali untuk pemain
anomaly_result = search_anomaly_recursive(player_name, stats_list, suspected_cheaters)
print(anomaly_result)

# Cetak daftar cheaters terbaru
print("\nDaftar pemain yang dicurigai melakukan kecurangan:")
print(sorted(suspected_cheaters))
