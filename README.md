# Video Recorder Application

## Overview
This application captures video from an HTTP stream and allows you to start and stop recording the video with a user-friendly GUI. The recorded videos are saved in the `Videos` folder with a timestamp format as filenames.

## Features
- Real-time video stream display.
- Start and stop recording with a button.
- Videos are saved with a timestamp filename in the `Videos` folder.
- User-friendly GUI using `tkinter`.

## Prerequisites
- Python 3.x
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/markbenazet/live-feed.git
    cd live-feed
    ```

2. Navigate to the `setup` folder and install the required dependencies:
    ```sh
    cd setup
    pip install -r requirements.txt
    ```

3. Ensure the video URL in `config.py` is correct:
    ```python
    # setup/config.py
    VIDEO_URL = "http://your-actual-video-stream-url"
    ```

## Usage
1. Navigate to the `src` folder:
    ```sh
    cd ../src
    ```

2. Run the application:
    ```sh
    python gui.py
    ```

3. The GUI will open, displaying the video stream. Use the buttons to start/stop recording and to exit the application.

## How It Works
- The application captures video from the provided HTTP stream URL using OpenCV.
- The GUI is built using `tkinter` for a user-friendly interface.
- When you start recording, the video is saved in the `Videos` folder outside the `src` directory with a filename based on the current timestamp.

## Troubleshooting
- Ensure the video stream URL is correct and accessible.
- Ensure you have internet access and necessary permissions to access the video stream.

## License
This project is licensed under the MIT License.
