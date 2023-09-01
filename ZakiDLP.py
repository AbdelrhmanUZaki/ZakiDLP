"""
A GUI version of yt-dlp built in PyQt5 to make it easier to use.
"""

from os.path import join, dirname
from re import search
from threading import Thread
from yt_dlp import YoutubeDL
from validators import url as validate
from humanize import naturalsize
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication, QDesktopWidget
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from webbrowser import open

Form_CLASS, _ = loadUiType(join(dirname(__file__), "main.ui"))



class MainApp(QMainWindow, Form_CLASS):
    """
    main class for my app
    till now 29-8-2023 it is the only class
    """
    before_download_playlist = pyqtSignal(int, str, int, str)
    full_playlist_downloaded = pyqtSignal()
    download_completed = pyqtSignal()
    download_error = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui_components()
        self.handel_radio_btns()
        self.handel_buttons()
        self.connect_signals()
        self.location = None
        self.id = None
        self.url = None
        self.dash = "----------------------------------"

    def open_link(self):
        """
        to open my GitHub account when a user presses on it
        """
        open("https://github.com/AbdelrhmanUZaki/")

    def ui_components(self):
        """
        to set up UI components that need written code
        :return:
        """
        self.center()
        self.Info_TE.setReadOnly(True)

    def show_message_box(self):
        """
        This function show message box to user with info I need when he clicks
         the supported websites in the file menu
        :return:
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Supported websites")
        msg_box.setText("Current supported websites:\n\n1. Youtube [single media/playlist]"
                        "\n\n2. Soundcloud [single media/playlist]")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    def center(self):
        """
        To center the app in the middle of the screen
        :return:
        """
        # Get the main window's geometry
        qr = self.frameGeometry()

        # Get the center point of the screen
        cp = QDesktopWidget().availableGeometry().center()

        # Move the main window's center to the screen center
        qr.moveCenter(cp)

        # Set the top-left point of the main window to the calculated position
        self.move(qr.topLeft())

    def connect_signals(self):
        """
        this is signal-slot in pyqt5 - It is used to do something,
         when another something happens
        I used it to change the UI after downloading finished
        :return:
        """
        self.download_completed.connect(self.handle_download_completed)
        self.full_playlist_downloaded.connect(self.handel_full_downloaded)
        self.download_error.connect(self.handle_download_error)
        self.before_download_playlist.connect(self.playlist_items_info)

        self.actionSupported_websites.triggered.connect(self.show_message_box)
        self.actionGitHub.triggered.connect(self.open_link)

    def handel_full_downloaded(self):
        """
        This function used to show a message box to user to inform
         him that the full playlist finished
        :return:
        """
        QMessageBox.information(self, "Success", "Playlist downloaded successfully")

    def playlist_items_info(self, index, item_title, item_duration, resolution):
        """
        to print the current playlist item -that is downloading- info
        :param index: index for the current item
        :return:
        """
        self.Info_TE.append(f"Current item: {item_title}")
        self.Info_TE.append(f"Item number : {index}")
        self.Info_TE.append(f"Duration    : {self.format_duration(item_duration)}")
        self.Info_TE.append(f"Resolution  : {resolution}")

    def handle_download_completed(self):
        """
        Updating the UI after finished downloading
        :return:
        """
        self.percent_lbl.setText("0%")
        self.Info_TE.append(f" {self.dash}  Item Downloaded  {self.dash} ")

    def handel_radio_btns(self):
        """
        To get action when user chooses any of the radio buttons on the screen
        :return:
        """
        self.Single_aud_rad.clicked.connect(self.single_aud)
        self.Single_vid_rad.clicked.connect(self.single_vid)
        self.Playlist_aud_rad.clicked.connect(self.playlist_aud)
        self.Playlist_vid_rad.clicked.connect(self.playlist_vid)

    def handel_buttons(self):
        """
        To handel all buttons for my program.
        :return:
        """
        # Connect to the function
        self.Download_btn.clicked.connect(self.download_selected_option)
        # Connect the button to the function
        self.Location_btn.clicked.connect(self.browse_and_set_path)

    def download_selected_option(self):
        """
        To check which radio button that user selects,
        and depend on this, I'll download with the specific way
        cause downloading for single media, differs that
        downloading a playlist
        :return:
        """
        if self.Single_aud_rad.isChecked():
            self.download_single()
        elif self.Single_vid_rad.isChecked():
            self.download_single()
        elif self.Playlist_aud_rad.isChecked():

            download_thread_playlist = Thread(target=self.download_playlist)
            download_thread_playlist.start()

        elif self.Playlist_vid_rad.isChecked():
            download_thread_playlist = Thread(target=self.download_playlist)
            download_thread_playlist.start()

        else:
            QMessageBox.critical(self, "Error", "First choose your format type")

    def get_url(self):
        """
         Getting url to download
        :return:
        """
        if self.url_LE.text():
            if validate(self.url_LE.text()):
                self.url = self.url_LE.text()
                return
            QMessageBox.critical(self, "Error", "Invalid URL\n\n"
                                                "You will counter another error messages")
            self.url_LE.clear()
        else:
            QMessageBox.critical(self, "Error", "URL can't be empty\n\n"
                                                "You will counter another error messages")

    def single_opts_function(self):
        """
        Creating single dictionary, create an object for single downloading
        :return:
        """
        self.single_opts = {'noplaylist': True, 'quiet': True}
        self.ydl = YoutubeDL(self.single_opts)

    def browse_and_set_path(self):
        """
        Create browse dialog to ge save location.
        :return:
        """
        # Show a folder dialog for choosing a folder location
        folder_dialog = QFileDialog.getExistingDirectory(self, "Save location", "")
        chosen_folder_path = folder_dialog

        if chosen_folder_path:
            # Set the chosen path in the QLineEdit
            self.location_LE.setText(chosen_folder_path)
            self.location = chosen_folder_path

    def single_aud(self):
        """
        Functions that will be executed when user selects single audio radio button
        :return:
        """
        self.get_url()
        self.single_general_flow()  # dict, obj, formats
        self.sa_download_flow()  # format, output template (location)

    def single_vid(self):
        """
        Functions that will be executed when user selects single video radio button
        :return:
        """
        self.get_url()
        self.single_general_flow()  # dict, obj, extract formats
        self.sv_download_flow()

    def playlist_aud(self):
        """
        Functions that will be executed when user selects playlist audio radio button
        :return:
        """
        self.get_url()
        self.playlist_general_flow()
        self.playlist_audio_download_flow()

    def playlist_vid(self):
        """
        Functions that will be executed when user selects playlist video radio button
        :return:
        """
        self.get_url()
        self.playlist_general_flow()
        self.playlist_video_download_flow()

    def single_output_template(self):
        """
        Set output template for single file downloading
        :return:
        """
        self.single_opts['outtmpl'] = {'default': f"{self.location}/%(title)s.%(ext)s"}

    def user_format_choice(self):
        """
        Getting the format_id for the selected item from the combo box
        :return:
        """
        selected_index = self.Quality_ComboB.currentIndex()
        selected_item = self.Quality_ComboB.itemText(selected_index)
        return selected_item

    def get_id_sa(self, selected_item):
        """
        Get ID corresponding to the single audio that user selects from the quality dropdown list
        :param selected_item:
        :return:
        """
        for key, value in self.audio_dict.items():
            if value == selected_item:
                self.id = key
                break

    def get_id_sv(self, selected_item):
        """
        search for the id that user selected is item from the combo box
        It will first search on the self.quality_dict_vid_merged dict, and if it is not there, then
        it must be in the other dict -self.quality_dict_vid-
        :param selected_item: Item which user selects
        :return:
        """
        for res, sizes in self.quality_dict_vid_merged.items():
            for size_key, size_data in sizes.items():
                size_display = f"{res}, {self.format_size(size_data['size'])}"

                if size_display == selected_item:
                    self.id = f"{size_data['id']}+ba"
                    return

        for key, value in self.quality_dict_vid.items():
            if value == selected_item:
                self.id = key
                return

    def set_id_single(self):
        """
        Set the id for the single file from user to download
        :return:
        """
        self.single_opts['format'] = self.id

    def extract_single_formats(self):
        """
        Extracting single file's info that I only need to print to user
        :return:
        """
        self.info_single = self.ydl.extract_info(self.url, download=False)
        self.single_formats = self.info_single.get('formats', [])
        self.single_item_title = self.info_single.get('title', 'Title unknown')
        self.single_item_uploader = self.info_single.get('uploader', 'Uploader unknown')
        self.single_item_duration = self.info_single.get('duration', 'Duration unknown')

    def print_headers_single(self):
        """
        print info for single files
        :return:
        """
        self.Info_TE.clear()
        self.Info_TE.append(f"Title    : {self.single_item_title}")
        self.Info_TE.append(f"Duration : {self.format_duration(self.single_item_duration)}")
        self.Info_TE.append(f"Uploader : {self.single_item_uploader}")

    def single_audio_formats(self):
        """
        Extract audio only formats
        """
        found_any_quality = False
        self.print_headers_single()
        self.audio_dict = {}
        self.Quality_ComboB.clear()

        for self.single_format in self.single_formats:
            format_id = self.single_format.get('format_id', 'N/A')
            ext = self.single_format.get('ext', 'N/A')
            vcodec = self.single_format.get('vcodec', 'N/A')
            acodec = self.single_format.get('acodec', 'N/A')
            filesize = self.single_format.get('filesize')
            filesize_approx = self.single_format.get('filesize_approx')

            # getting tbr 'Total Bit Rate' to calc the size manually - if size is
            # not available - via calc_size function
            tbr = self.single_format.get('tbr')

            # Exclude formats with mhtml protocol
            # vcodec == 'none' to only select audio options without a video
            if vcodec == 'none' and acodec != 'none':
                size = filesize or filesize_approx or self.calc_size(tbr)
                self.audio_dict[format_id] = f"{ext}, {self.format_size(size)}"
            found_any_quality = True

        if not found_any_quality:
            QMessageBox.warning(self, "Warning", "No audio options available")

        self.append_aud_info()

    def append_aud_info(self):
        """
        Adding audio options to the quality dropdown list
        :return:
        """
        for format_data in self.audio_dict.values():
            self.Quality_ComboB.addItem(format_data)

    def append_vid(self):
        """
        Adding video with audio options to the quality dropdown list
        :return:
        """
        for format_data in self.quality_dict_vid.values():
            self.Quality_ComboB.addItem(format_data)

    def update_merged(self):
        """
        This function to update self.quality_dict_vid_merged with new size
        after adding the size of best audio to it
        :return:
        """
        for res, info in self.quality_dict_vid_merged.items():
            info['highest_size']['size'] += self.ba_size
            info['lowest_size']['size'] += self.ba_size

    def append_vid_merged(self):
        """
        append video that was merged with the best audio to the quality dropdown list
        :return:
        """
        line = "-" * 40
        self.Quality_ComboB.addItem(f"{line}")

        for res, info in self.quality_dict_vid_merged.items():
            highest_size = info['highest_size']['size']
            lowest_size = info['lowest_size']['size']

            self.Quality_ComboB.addItem(f"{res}, {self.format_size(lowest_size)}")
            self.Quality_ComboB.addItem(f"{res}, {self.format_size(highest_size)}")

    def single_video_formats(self):
        """
        Getting all formats for single video
        exclude m3u8 formats - as its size is unknown -
        exclude mhtml ext as it's a html pages
        Store info for videos that has audio in a dict, and
        videos that hasn't an audio in another dict
        For videos that has no audio, I'll get the highest and
        lowest size for each quality
        :return:
        """

        self.quality_dict_vid = {}
        self.quality_dict_vid_merged = {}
        self.Quality_ComboB.clear()

        # getting needed info
        for self.single_format in self.single_formats:
            format_id = self.single_format.get('format_id', 'N/A')
            ext = self.single_format.get('ext', 'N/A')
            vcodec = self.single_format.get('vcodec', 'N/A')
            acodec = self.single_format.get('acodec', 'N/A')
            protocol = self.single_format.get('protocol', 'N/A')
            res = self.single_format.get('resolution', 'N/A')
            filesize = self.single_format.get('filesize')
            tbr = self.single_format.get('tbr')

            self.formatting_videos(format_id, ext, vcodec, acodec, protocol, res, filesize, tbr)

    def formatting_videos(self, format_id, ext, vcodec, acodec, protocol, res, filesize, tbr):
        """
        To exclude and get only formats as I need
        :return:
        """
        # vcodec != 'none' to exclude audio formats
        if 'm3u8' not in protocol and 'mhtml' not in ext and vcodec != 'none':
            size = filesize or self.single_format.get('filesize_approx') or self.calc_size(tbr)

            if acodec != 'none':
                # format has an audio already
                self.store_quality_dict(format_id, ext, res, size)
            else:
                # video has no audio
                self.getting_h_l(res, size, format_id)

    def getting_h_l(self, res, size, format_id):
        """
         Getting highest and lowest size of each res.
        """
        if res in self.quality_dict_vid_merged:
            # Update highest_size if the new size is larger
            if size > self.quality_dict_vid_merged[res]['highest_size']['size']:
                self.quality_dict_vid_merged[res]['highest_size'] = {'id': format_id, 'size': size}
            # Update lowest_size if the new size is smaller
            elif size < self.quality_dict_vid_merged[res]['lowest_size']['size']:
                self.quality_dict_vid_merged[res]['lowest_size'] = {'id': format_id, 'size': size}
        else:
            # Initialize the dictionary with both highest_size and lowest_size
            self.quality_dict_vid_merged[res] = {
                'highest_size': {'id': format_id, 'size': size},
                'lowest_size': {'id': format_id, 'size': size}
            }

    def store_quality_dict(self, format_id, ext, res, size):
        """
        store the video - that has audio already - data in its dict
        :return:
        """
        self.quality_dict_vid[format_id] = f"{ext}, {res}, {self.format_size(size)}"

    def video_with_audio(self):
        """
        Printing the data for video formats that has an audio with it
        :return:
        """
        self.print_headers_single()
        self.append_vid()

    def video_merged(self):
        """
        Process on video that will be merged with the best audio
        Getting the data for those formats from self.quality_dict_vid_merged dictionary
        Adding the best audio size to size for each format
        :return:
        """
        self.update_merged()
        self.append_vid_merged()

        if not any(self.quality_dict_vid_merged) and not any(self.quality_dict_vid):
            QMessageBox.warning(self, "Warning", "No video options available")

    def get_ba_size(self):
        """
        Getting the best audio size to sum it with the video
         formats that has no audio already
        :return:
        """
        self.ba_size = 0
        for self.single_format in self.single_formats:
            # vcodec == 'none' => means that it's an audio not video or something else
            # acodec != 'none' => means that it's an audio not video or something else

            filesize = self.single_format.get('filesize')
            approx_size = self.single_format.get('filesize_approx')
            tbr = self.single_format.get('tbr')

            if (self.single_format.get('vcodec') == 'none' and
                    self.single_format.get('acodec') != 'none'):
                size = filesize or approx_size or self.calc_size(tbr)
                if not isinstance(size, str) and size is not None:
                    if size > self.ba_size:
                        self.ba_size = size

    def calc_size(self, tbr):
        """
        ONLY for single (audio/video).
        Calculate the size manually if it's not being presented
        tbr in kilobits in seconds
        multiply in 1024 to convert it to bits
        division on 8 to convert it to bytes
        """
        duration = self.info_single.get('duration', 'Duration unknown')

        if tbr is not None:
            if duration != 'Duration unknown':
                final_try_size = int(duration * tbr * (1024 / 8))
                return final_try_size
            return "Size unknown"
        return "Size unknown"

    def format_duration(self, duration):
        """
        Format duration in a beautiful way to be readable by changing the unit.
        :param duration: unit in second
        :return: duration
        """
        if duration == "Duration unknown":
            return "Duration unknown"

        duration /= 60
        if duration > 60:
            duration /= 60
            return f"{duration:.2f} Hour"  # convert to Hour
        return f"{duration:.2f} Min"  # convert to Min

    def format_size(self, size):
        """
         Format size in a beautiful way to be readable by changing the unit.
        :param size: unit in bytes
        :return:
        """
        try:
            size = naturalsize(size)
            return size
        except Exception:
            # return f"Size unknown"
            return size

    def single_general_flow(self):
        """
        It's a single general flow for all single items.
        :return:
        """
        self.single_opts_function()
        try:
            self.extract_single_formats()
        except Exception as error:
            QMessageBox.critical(self, "Error", "Exception while extracting"
                                                f" single formats\nError: {error}")

    def sa_download_flow(self):
        """
        All functions I need to download a single audio
        Except setting location, I'll do it in browse function
        :return:
        """
        try:
            self.single_audio_formats()
        except Exception as error:
            QMessageBox.critical(self, "Error", "Exception while getting list of"
                                                f" audio formats\nError: {error}")

    def sv_download_flow(self):
        """
        All functions I need to download a single video
        :return:
        """

        try:
            self.single_video_formats()
        except Exception as error:
            QMessageBox.critical(self, "Error", "Exception while getting list"
                                                f" of video formats\nError: {error}")

        try:
            self.get_ba_size()
        except Exception as error:
            QMessageBox.critical(self, "Error", "Exception while getting"
                                                f" best audio size\nError: {error}")

        try:
            self.video_with_audio()
        except Exception as error:
            QMessageBox.critical(self, "Error", "Exception while getting video"
                                                f" that has an audio info\nError: {error}")

        try:
            self.video_merged()
        except Exception as error:
            QMessageBox.critical(self, "Merge error", "Exception while adding"
                                                      f" the size of best audio\n{error}")

        try:
            self.single_output_template()
        except Exception as error:
            QMessageBox.critical(self, "Merge error", "Exception while setting"
                                                      f" the single video output template {error}")

    def download_single(self):
        """
        - Check if user selects the single aud or vid radio button,
         then I'll get the id corresponding to the item
        that the user selects from the quality dropdown list 
        - an actual downloading process will be on a thread, to keep
         the UI responsive, and to let me update it as I need
        :return:
        """
        selected_item = self.user_format_choice()

        if self.Single_aud_rad.isChecked():
            self.get_id_sa(selected_item)

        elif self.Single_vid_rad.isChecked():
            self.get_id_sv(selected_item)

        self.set_id_single()
        self.single_output_template()

        download_thread = Thread(target=self.thread_for_single_download)
        download_thread.start()

    def thread_for_single_download(self):
        """
        The thread for only downloading single midea
        :return: 
        """
        try:
            self.single_opts['progress_hooks'] = [self.update_progress]
            with YoutubeDL(self.single_opts) as ydl:
                ydl.download(self.url)
                self.download_completed.emit()
        except Exception as error:
            self.download_error.emit(str(error))

    def handle_download_error(self, error_message):
        """
        To update the UI with error in case it happens while downloading
        :param error_message:
        :return:
        """
        QMessageBox.critical(self, "Error", "Error while downloading"
                                            f" a file\n{error_message}")

    def update_progress(self, data):
        """
        update the label "percent_lbl" with current progress
        :param data: 
        :return: 
        """
        if data['status'] == 'downloading':
            try:
                percent_str = data['_percent_str']
                extracted_number = self.extract_number(percent_str)
                self.percent_lbl.setText(extracted_number)

            except ValueError as error:
                self.download_error.emit(str(error))

    def extract_number(self, text):
        """
        To get only the number with percent of the progress without any
         additional text that yt-dlp stores the data with
        """
        pattern = r"(\d+\.\d+%)"
        match = search(pattern, text)
        if match:
            return match.group(1)
        return ""

    # playlist part

    def playlist_opts_function(self):
        """
        - Creating playlist dictionary and its object
        - I extract with 'extract_flat': 'in_playlist' to make
         the extraction fastest as possible.
        - This type of extraction is only return info about
         the playlist, not its entries.
        - Some websites include additional info about the
         entries - like YouTube-
        - To get the playlist entries info, I used another
         dict {self.playlist_opts_manual} with other options while looping on them
        """
        self.playlist_opts = {'extract_flat': 'in_playlist', 'quiet': True}
        self.ydl_playlist = YoutubeDL(self.playlist_opts)
        self.playlist_opts_manual = {'quiet': True}

    def playlist_audio_quality(self):
        """
        Asking user only to choose either to download the
         full playlist with the best audio available
        or with the worst
        :return:
        """
        self.append_playlist_aud()

    def append_playlist_aud(self):
        """
        append playlist audio options to the dropdown list
        :return:
        """
        self.Quality_ComboB.clear()
        audio_options = ["High audio quality", "Low audio quality"]
        for choice in audio_options:
            self.Quality_ComboB.addItem(choice)

    def playlist_video_quality(self):
        """
        Asking user to choose the quality to download
         the full playlist with it
        If the selected quality is available for any
         video, I'll download it.
        If it's not, I'll download the first quality
         that is lower than the selected quality
        If there is no quality lower than the selected
         quality, I'll download the first quality that
         is greater than selected
        :return:
        """
        self.append_playlist_vid()

    def append_playlist_vid(self):
        """
        append playlist video option to the quality dropdown list
        :return:
        """
        self.Quality_ComboB.clear()
        self.options = ("144p", "240p", "360p", "480p", "720p", "1080p")
        for choice in self.options:
            self.Quality_ComboB.addItem(choice)

    def set_playlist_aud_id(self, selected_item):
        """
        Store the id for audio that corresponding to which user option select
        :param selected_item: item text to compare
        :return:
        """
        if selected_item == "High audio quality":
            self.playlist_opts_manual['format'] = 'ba'
        elif selected_item == "Low audio quality":
            self.playlist_opts_manual['format'] = 'wa'
        else:
            QMessageBox.critical(self, "Error", "choose an option from the dropdown list")

    def set_playlist_vid_id(self, selected_item):
        """
        Store the id for video that corresponding to which user option select.
        :param selected_item: item text to compare
        :return:
        """
        for quality_choice in self.options:
            if quality_choice == selected_item:
                # to delete the p letter, 720p => 720
                quality_choice = quality_choice[:-1]
                self.playlist_opts_manual['format_sort'] = [f"res:{quality_choice}"]
                break
        else:
            QMessageBox.critical(self, "Error", "choose an option from the dropdown list")
        self.convert_ext()

    def convert_ext(self):
        """
        to convert all playlist videos into mp4 after downloading
        :return:
        """
        self.playlist_opts_manual['final_ext'] = 'mp4'
        self.playlist_opts_manual['postprocessors'] =\
            [{'key': 'FFmpegVideoRemuxer', 'preferedformat': 'mp4'}]

    def extract_playlist_info(self):
        """
        Extract all info about the playlist itself
        :return:
        """
        self.info_playlist = self.ydl_playlist.extract_info(self.url, download=False)

    def playlist_num_items(self):
        """
        Get number of playlist items
        :return: numbers
        """
        return len(self.info_playlist.get('entries', []))

    def playlist_title_function(self):
        """
        Get the playlist title.
        :return: title
        """
        self.playlist_title = self.info_playlist.get('title', 'Title unknown')
        return self.playlist_title

    def playlist_uploader(self):
        """
        Get the playlist uploader name
        :return:
        """
        uploader = self.info_playlist.get('uploader', 'Unknown Uploader')
        return uploader

    def playlist_general_flow(self):
        """
        Playlist general flow either it's an audio or video
        :return:
        """
        self.playlist_opts_function()
        try:
            self.extract_playlist_info()
        except Exception as error:
            QMessageBox.critical(self, "Error", "Exception while"
                                                f" extracting playlist info\n{error}")

        try:
            self.print_playlist_info()
        except Exception as error:
            QMessageBox.critical(self, "Error", "Exception while printing"
                                                f" out playlist info\n{error}")

    def print_playlist_info(self):
        """
        To print the playlist itself info into the GUI text Edit
        :return:
        """
        self.Info_TE.clear()
        self.Info_TE.append(f"Playlist title : {self.playlist_title_function()}")
        self.Info_TE.append(f"Number of items : {self.playlist_num_items()} ")
        self.Info_TE.append(f"Uploader : {self.playlist_uploader()}")
        self.Info_TE.append(f"{self.dash * 2}")

    def playlist_video_download_flow(self):
        """
        Functions needed to download a playlist as videos
        :return:
        """
        self.playlist_video_quality()

    def playlist_audio_download_flow(self):
        """
        Functions needed to download a playlist as audios
        :return:
        """
        self.playlist_audio_quality()

    def download_playlist_item(self, index, entry):
        """
        Manually loop over the playlist items to get
         its info and download it
        I didn't download a full playlist default by
         yt-dlp cause if I need to do that, I won't be able
        to making my app fastest as possible, it will
         be slow cause it collecting data about all its entries,
        so instead, I only return a data from a playlist,
         then manually I do what I need on its entries
        :param index: to count each item with its turn
        :param entry: to get the url of that item
        :return:
        """
        url = entry.get('url')
        if url:
            self.playlist_opts_manual['outtmpl'] =\
                f"{self.location}/{self.playlist_title}/{index} - %(title)s.%(ext)s"
            with YoutubeDL(self.playlist_opts_manual) as ydl:
                video_info = ydl.extract_info(url, download=False)

                item_title = video_info.get('title', f"{url}")
                item_duration = int(video_info.get('duration', 'Duration unknown'))
                resolution = video_info.get('resolution', 'Resolution Unknown ')
                self.before_download_playlist.emit(index, item_title, item_duration, resolution)

                ydl.download([url])
                self.download_completed.emit()

    def download_playlist(self):
        """
        Beginning of the loop to download a full playlist
        :return:
        """
        selected_item = self.user_format_choice()

        if self.Playlist_aud_rad.isChecked():
            self.set_playlist_aud_id(selected_item)

        elif self.Playlist_vid_rad.isChecked():
            self.set_playlist_vid_id(selected_item)

        self.playlist_opts_manual['progress_hooks'] = [self.update_progress]

        # loop over the playlist urls and download it manually
        for index, entry in enumerate(self.info_playlist.get('entries', []), start=1):
            self.download_playlist_item(index, entry)

        self.full_playlist_downloaded.emit()


def main():
    """
    Main function that my app will start from
    :return:
    """
    app = QApplication([])
    downloader = MainApp()
    downloader.show()
    app.exec_()


if __name__ == "__main__":
    main()
