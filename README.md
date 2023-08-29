# ZakiDLP (A GUI for yt-dlp)
#### Based on yt-dlp, the cli program that downloads from [various websites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).
#### You can download the exe file from []

## Workflow
- Input url.
- Choose a radio button that you need.
- Choose your quailty.
- Choose save location.
- Start download.
  
## Requirements
- You need no requirements

## Features
- Currently, my app works fine with YouTube, SoundCould, for a single media or a playlist AND it works on windows only.
- To pause the downloading, just close the app :)
- To resume whenever you want, just choose same settings, and it will continue from where it stopped.
- For the `same` file, you can't download it with different qualities, as the tool `yt-dlp` see that it is the same, instead rename the old one and it will download the new one.
- For video that is in a playlist, you can download the full playlist using this link as if it were the playlist link.

###  For single media:
  - Duration of the file.
  - The file Title.
  - The file extension.
  - The file size.
  - Printing "Item downloaded" only when download completed.
  - For audio:
    - I"ll show you all available audio options with them sizes.
  -  For video:
      - I'll show you `first`: videos that has already audio with it, `second`: the highest and lowest size video options for each quality that already has no audio, and I'll merge the best audio file with it, with them sizes -after adding the best audio size to the size of the video only.
      - Extension for videos that will be merged specified by the tool `yt-dlp`, the tool will choose the best ext depending on the merging process
      - There is a horizontal line between them
      -  ![image](https://github.com/AbdelrhmanUZaki/ZakiDLP/assets/99971020/1f864752-445a-4189-bc38-22c7e9fc1f9d) 
     
### For playlists:
  - Playlist title.
  - Number of items.
  - Uploader name.
  - Index of current downloading file.
  - Resolution.
  - Printing "Item downloaded" after each item download completed.
  - An info messagebox with sound to inform you that the full playlist has been downloaded.
  - For Audios:
    - You'll have two options High/Low (audio quality)
  - For videos:
    - All will be in .mp4 extension. 
    - You'll see the usual list 144p, 240p...etc, and the tool will try to download that quality, each video quality in playlist will be printed to you
    - ![image](https://github.com/AbdelrhmanUZaki/ZakiDLP/assets/99971020/0dc16bed-34d9-4a38-9296-d275f4300b97)
        - If the selected quality is not available for the specific video in the playlist, I'll try to find the best quality lower than specified quality..
        - If there is no qualities lower than it, the higher quality than it will be downloaded.
        
### Over time I will add more websites with more features inshallah.

- Pics of the app
  ![image](https://github.com/AbdelrhmanUZaki/ZakiDLP/assets/99971020/470df401-d021-4ca5-8ca5-cb8318b2b63d)
  ![image](https://github.com/AbdelrhmanUZaki/ZakiDLP/assets/99971020/59f34c8d-f10a-4351-9634-f1e046123c68)
