"""
A file with the most popular genres. 
Obtained from http://everynoise.com/everynoise1d.cgi?scope=mainstream%20only&vector=popularity. 
Copied all rows into a .txt file and then extracted to this file.
"""

most_genres = ["pop", "pop rap", "dance pop", "rap", "rock", "post-teen pop", "latin", "hip hop", "trap", "modern rock", "edm",
                    "tropical house", "pop rock", "latin pop", "reggaeton", "electropop", "melodic rap", "southern hip hop", "album rock",
                    "mellow gold", "post-grunge", "soft rock", "neo mellow", "classic rock", "alternative metal", "r&b", "indie pop", "uk pop",
                    "tropical", "permanent wave", "electro house", "contemporary country", "urban contemporary", "alternative rock", "nu metal",
                    "hard rock", "rock en espanol", "singer-songwriter", "alternative r&b", "adult standards", "gangster rap", "viral pop",
                    "underground hip hop", "indietronica", "german hip hop", "canadian pop", "grupera", "k-pop", "country", "folk rock",
                    "indie rock", "atl hip hop", "indie poptimism", "country road", "french hip hop", "reggaeton flow", "australian pop",
                    "latin alternative", "big room", "europop", "mexican pop", "regional mexican", "art rock", "dance rock", "chamber pop",
                    "latin rock", "new wave pop", "banda", "trap latino", "funk carioca", "soul", "pop urbaine", "latin hip hop", "indie folk",
                    "house", "norteno", "psychedelic rock", "stomp and holler", "art pop", "latin arena pop", "garage rock", "vapor trap", "hip pop",
                    "metal", "spanish pop", "sertanejo universitario", "chicago rap", "roots rock", "emo rap", "progressive house", "boy band",
                    "pop punk", "new wave", "indie r&b", "pop edm", "blues rock", "italian hip hop", "folk", "neo soul", "funk", "conscious hip hop",
                    "regional mexican pop", "indie soul", "canadian hip hop", "progressive electro house", "dfw rap", "colombian pop",
                    "lo-fi beats", "motown", "background music", "quiet storm", "miami hip hop", "german pop", "new romantic", "modern country rock",
                    "new rave", "escape room", "ranchera", "emo", "k-pop boy group", "swedish pop", "new americana", "ccm", "glam rock", "rap metal",
                    "cumbia", "toronto rap", "disco", "j-pop", "mpb", "italian pop", "metropopolis", "brill building pop", "uk hip hop", "punk", "brostep", 
                    "alternative dance", "piano rock", "pagode", "electronica", "vocal jazz", "argentine rock", "east coast hip hop", "deep pop r&b", 
                    "italian arena pop", "lounge", "worship", "sertanejo", "hollywood", "francoton", "christian music", "hoerspiel", "indonesian pop", 
                    "sertanejo pop", "dutch pop", "hardcore hip hop", "talent show", "rap conscient", "g funk", "focus", "uk dance", "world worship", 
                    "heartland rock", "social media pop", "metalcore", "sleep", "perreo", "folk-pop", "brazilian hip hop", "rap rock", "baile pop", 
                    "dutch hip hop", "desi pop", "vapor soul", "lgbtq+ hip hop", "opm", "pop nacional", "groove metal", "chillhop", "indie anthem-folk", 
                    "modern alternative rock", "deep big room", "cali rap", "electronic trap", "dark trap", "soundtrack", "dirty south rap", "acoustic pop", 
                    "west coast rap", "country rock", "modern bollywood", "christian alternative rock", "nova mpb", "turkish pop", "british invasion", 
                    "cantautor", "alternative hip hop", "dance-punk", "classical", "detroit hip hop", "glam metal", "classic soul", "funk ostentacao", 
                    "brazilian edm", "yacht rock", "disco house", "turkish rock", "german cloud rap", "puerto rican pop", "country pop", "melodic metalcore", 
                    "scorecore", "trap queen", "trap espanol", "canadian contemporary r&b", "baroque pop", "latin viral pop", "brazilian rock", "filmi", 
                    "trap argentino", "mexican rock", "rock-and-roll", "indiecoustica", "calming instrumental", "anthem worship", "german rock", "funk metal", 
                    "anime", "british soul", "k-pop girl group", "freak folk", "melancholia", "j-rock", "grime", "otacore", "speed metal", "synthpop", 
                    "bedroom pop", "new jack swing", "bass trap", "atl trap", "argentine hip hop", "bolero", "mandopop", "screamo", "easy listening", 
                    "comic", "show tunes", "progressive rock", "nc hip hop", "deep tropical house", "symphonic rock", "australian indie", "britpop", 
                    "dream pop", "french pop", "protopunk", "bubblegum pop", "compositional ambient", "deep german hip hop", "chillwave", "australian danc"]

# Limit popular genres to the first 30
popular_genres = set(most_genres[:30])
