
import csv
from getpass import getpass
from pathlib import Path
from yandex_music import Client

OUTPUT = Path(__file__).resolve().parent / "yandex_liked.csv"

print("Авторизация в Яндекс Музыке")
token = getpass("Вставь токен Яндекс Музыки: ")

client = Client(token).init()

print("Получаем понравившиеся треки...")
liked = client.users_likes_tracks()
tracks = liked.tracks

print(f"Получено треков: {len(tracks)}")

with OUTPUT.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Artist", "Album", "Yandex ID"])

    for index, short_track in enumerate(tracks, 1):
        try:
            track = short_track.fetch_track()

            artists = ", ".join(
                artist.name for artist in (track.artists or [])
            )
            albums = ", ".join(
                album.title for album in (track.albums or [])
            )

            writer.writerow([
                track.title,
                artists,
                albums,
                track.id
            ])

            print(f"[{index}/{len(tracks)}] {track.title}")

        except Exception as error:
            print(f"[{index}] Ошибка: {error}")

print(f"\nЭкспорт завершён: {OUTPUT}")
