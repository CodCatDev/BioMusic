import asyncio
import requests
from pyrogram import Client
from pyrogram.raw import functions, types
from config import API_ID, API_HASH, LFM_API_KEY, LFM_USER, DEFAULT_TEXT

# v1.0

app = Client(
    "bio-music-v1",
    api_id=API_ID,
    api_hash=API_HASH,
    device_model="Bio-Music",
    system_version="Ubuntu 22.04",
    app_version="Bio-Music, v1.0, by CodCatDev"
)

def get_now_playing():
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LFM_USER}&api_key={LFM_API_KEY}&format=json&limit=1"
    try:
        r = requests.get(url).json()
        track = r['recenttracks']['track'][0]
        
        if "@attr" in track and track["@attr"]["nowplaying"] == "true":
            song_name = track["name"]
            song_artist = track["artist"]["#text"]
            text = f"🎧 {song_artist} - {song_name}"
            
            if len(text) > 64:
                text = text[:61] + "..."
            return text
    except:
        pass
    return DEFAULT_TEXT

async def main():
    async with app:
        last_loc = ""
        while True:
            new_loc = get_now_playing()
            if new_loc != last_loc:
                try:
                    await app.invoke(
                        functions.account.UpdateBusinessLocation(
                            address=new_loc
                        )
                    )
                    last_loc = new_loc
                    print(f"New Song - {new_loc}")
                except Exception as e:
                    print(f"err - {e}")
                    
            await asyncio.sleep(7)

app.run(main())
