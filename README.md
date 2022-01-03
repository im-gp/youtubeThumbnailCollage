# youtubeThumbnailCollage
A python script to create collages of YouTube playlists or channels.

![EthosLab YouTube Channel Collage Image](https://i.imgur.com/UlRPM8X.jpeg)
*EthosLab YouTube Channel Collage*

YouTube API Key
---

**REQUIRES AN API KEY FROM YOUTUBE TO WORK!!**

Learn how to get one:

- https://developers.google.com/youtube/v3/getting-started
- https://console.cloud.google.com/apis/dashboard

Make sure to set the variable **api_key** to your key.
- api_key = '```abc123```'

User Parameters
---
To change the playlist/channel, adjust the PlaylistID variable.
- playlistID = ```'PLHykAyQQdTart3T8wrDjEnAFEmbVstInA'```
- Original URL: ```https://www.youtube.com/watch?v=6wv84OUmnwg&list=PLHykAyQQdTart3T8wrDjEnAFEmbVstInA```

(*Supports channels and playlist ID's*)

**If the playlist has private videos, there may be some issues.**

There are options to keep/remove the thumbnails and CSV once the script has finished running.
- keepImages = ```True```
- keepCSV = ```True```

By default, the script will create and keep a .CSV and a folder:
- images/
- collage.csv

---
Useful Links:

- [YouTube Python Git](https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md)
- [YouTube v3 Docs](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html)
- [YouTube Developer API Page](https://developers.google.com/youtube/v3/docs)
- [YouTube tutorial used](https://www.youtube.com/watch?v=coZbOM6E47I)
