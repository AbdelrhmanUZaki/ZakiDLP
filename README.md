<style>
  .image-container {
    display: flex; /* Use flexbox for layout */
  }
  .image-container img {
    width: 50%; /* Each image takes 50% of the container's width */
    height: auto; /* Maintain aspect ratio */
  }
</style>

# ZakiDLP (A GUI for yt-dlp)
#### Based on [yt-dlp](https://github.com/yt-dlp/yt-dlp), a cli program that downloads media from [various websites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Getting Started
#### You can download [the current version](https://github.com/AbdelrhmanUZaki/ZakiDLP/releases/download/v1.0.0/ZakiDLP.v1.0.0.zip) as one file.

## How to use:
- Input url.
- Choose a radio button that you need [ Single/Playlist | Audio/Video ]
- Choose your quailty.
- Choose save location.
- Start download.
  
## Requirements
- You need no requirements

## Features
- Currently, my app works fine with YouTube, SoundCloud, for a single media or a playlist AND it works on windows only.
- To pause the downloading, just close the app :)
- To resume whenever you want, just choose same settings, and it will continue from where it stopped.
- For the same file with the same extension, you can't download it with different qualities, as the tool `yt-dlp` see that it is the same -and printing that it downloaded it but actually it is the old one- so instead, rename the old one and it will download the new one.
- For video that is in a playlist, you can download the full playlist using this link as if it were the playlist link.

###  For single media:
  - The file Duration.
  - The file Title.
  - The file extension (for audio/video that has audio originally)
  - The file size.
  - Informing you when download completed.
  - For audio:
    - You'll see all available audio options with them sizes.
  -  For video:
      - `first`: Videos that has already audio with it,
      - `second`: The highest and lowest size video options for each quality that already has no audio, and `ZakiDLP` will merge the best audio file with it, with them sizes, after adding the best audio size to the size of the video only to get the actuall size that will be downloaded.
      - Extension for videos that will be merged specified by the tool `yt-dlp`, the tool will choose the best ext depending on the merging process
      - There is a horizontal line To separete them.
      -  ![image](https://github.com/AbdelrhmanUZaki/ZakiDLP/assets/99971020/1f864752-445a-4189-bc38-22c7e9fc1f9d) 
     
### For playlists:
  - All playlist will be downloaded in a file with its name.
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
    - You'll see the usual list 144p, 240p...etc, and the tool will try to download that quality,
    - Each video quality in playlist will be printed to you to know the actuall res that any video will be in.
    - ![image](https://github.com/AbdelrhmanUZaki/ZakiDLP/assets/99971020/0dc16bed-34d9-4a38-9296-d275f4300b97)
    - If the selected quality is not available for the specific video in the playlist, the best quality lower than specified one will be downloaded.
    - If there is no qualities lower than it, the higher quality than it will be downloaded.
        
### Over time I will add more websites with more features inshallah.

- Pics of the app:

