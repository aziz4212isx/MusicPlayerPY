# Android Build Instructions

This directory contains a prototype Android version of the Music Player built with **Kivy** and **KivyMD**.

## Prerequisites
To build an APK for Android, you cannot use Windows directly. You need:
1.  **Linux** (Ubuntu is recommended) or **macOS**.
2.  Or use **Google Colab** / **WSL2** (Windows Subsystem for Linux).

**IMPORTANT / PENTING:**
- **DO NOT use Drive C:** (JANGAN gunakan Disk C).
- Ensure this project and the build process are running on a secondary drive (like **Drive D:**) because the build process consumes significant space and your Drive C is full.
- Pastikan semua proses build dilakukan di drive lain (misalnya D:) untuk menghindari masalah ruang penyimpanan.

## Local Testing (Windows)
**Note:** To run this app locally on Windows, you need **Python 3.10 - 3.12**.
If you are using a newer version (like Python 3.13+), Kivy dependencies might not be available yet.
Buildozer (Android build) will handle its own Python version automatically, so this only affects local testing.

## Build Solution for Windows (Without WSL/Linux)

Since `buildozer` **cannot run on Windows directly** and your C drive is full (preventing WSL installation), the best solution is to use **Google Colab**.

I have created a notebook file for you: `Build_Android_MusicPlayer.ipynb`.

### How to use Google Colab:
1.  Go to [Google Colab](https://colab.research.google.com/).
2.  Click **File** -> **Upload notebook**.
3.  Upload the `Build_Android_MusicPlayer.ipynb` file from this folder.
4.  Follow the instructions inside the notebook:
    -   Run the first cell to install dependencies.
    -   Upload your `main.py`, `buildozer.spec`, and `requirements.txt` to the Colab file area (folder icon on the left).
    -   Run the build command.
    -   Download the APK from the `bin/` folder once finished.

## Build Solution using GitHub Actions (Automated)

You can also use GitHub Actions to build the APK automatically when you push to GitHub.

1.  I have created a workflow file: `github_workflow_build_kivy.yml` in this folder.
2.  **Move this file** to `.github/workflows/` in your repository root.
    -   Example path: `YourRepoRoot/.github/workflows/build_android_kivy.yml`
3.  Push your changes to GitHub.
4.  Go to the **Actions** tab in your GitHub repository.
5.  Select **Build Android Kivy (Python)**.
6.  Once the build finishes (green checkmark), click on it and download the artifact **music-player-kivy-debug** at the bottom of the page.

## Steps to Build (using Linux/WSL only)

1.  **Install Buildozer** (on Linux/WSL):
    ```bash
    pip install buildozer
    sudo apt update
    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    pip3 install --user --upgrade Cython==0.29.33 virtualenv  # Specific Cython version often needed
    ```

2.  **Initialize Buildozer**:
    Inside this `android_src` folder:
    ```bash
    buildozer init
    ```

3.  **Edit `buildozer.spec`**:
    - Change `title` to "Music Player"
    - Change `package.name` to "musicplayer"
    - Change `requirements` to:
      `requirements = python3,kivy,kivymd,yt-dlp,requests,pillow`
    - Add permissions if needed:
      `android.permissions = INTERNET,ACCESS_NETWORK_STATE`

4.  **Build the APK**:
    ```bash
    buildozer android debug
    ```

5.  **Install on Phone**:
    Connect your Android phone via USB (enable USB Debugging) and run:
    ```bash
    buildozer android deploy run
    ```

## Limitations of this Prototype
-   **Audio Playback**: This prototype uses `yt-dlp` to fetch metadata but does not include the complex VLC integration of the desktop version. For Android, you should use Kivy's `SoundLoader` or a native player integration.
-   **UI**: The UI is simplified using Material Design components (KivyMD) which look native on Android, unlike PyQt5 widgets.
