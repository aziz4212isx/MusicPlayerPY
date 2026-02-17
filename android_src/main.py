from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import threading
import yt_dlp

# Set window size for testing on desktop (resembles phone)
Window.size = (360, 640)

class AndroidMusicPlayer(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        
        self.sound = None
        
        screen = MDScreen()
        
        # Main Layout
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Title
        title = MDLabel(
            text="YouTube Music Player",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=50
        )
        
        # URL Input
        self.url_input = MDTextField(
            hint_text="Paste YouTube URL here",
            mode="rectangle",
            size_hint_y=None,
            height=50
        )
        
        # Thumbnail Image (Placeholder)
        self.thumbnail = AsyncImage(
            source='https://www.youtube.com/img/desktop/yt_1200.png',
            size_hint=(1, 0.4)
        )
        
        # Status Label
        self.status_label = MDLabel(
            text="Ready",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=30
        )
        
        # Buttons Layout
        btn_layout = MDBoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=50)
        
        play_btn = MDRaisedButton(
            text="PLAY",
            size_hint_x=0.5,
            on_release=self.play_video
        )
        
        stop_btn = MDRaisedButton(
            text="STOP",
            size_hint_x=0.5,
            md_bg_color=(1, 0, 0, 1),
            on_release=self.stop_audio
        )
        
        btn_layout.add_widget(play_btn)
        btn_layout.add_widget(stop_btn)
        
        # Add widgets to main layout
        layout.add_widget(title)
        layout.add_widget(self.thumbnail)
        layout.add_widget(self.url_input)
        layout.add_widget(self.status_label)
        layout.add_widget(btn_layout)
        layout.add_widget(MDLabel()) # Spacer
        
        screen.add_widget(layout)
        return screen

    def play_video(self, instance):
        url = self.url_input.text
        if not url:
            self.status_label.text = "Please enter a URL"
            return
            
        self.status_label.text = "Processing..."
        # Run in thread to not freeze UI
        threading.Thread(target=self.process_video, args=(url,)).start()

    def process_video(self, url):
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                thumbnail = info.get('thumbnail', '')
                stream_url = info.get('url')
                
                # Update UI on main thread
                Clock.schedule_once(lambda dt: self.update_ui(title, thumbnail), 0)
                
                # Play audio on main thread
                if stream_url:
                    Clock.schedule_once(lambda dt: self.start_audio(stream_url), 0)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error(str(e)), 0)

    def update_ui(self, title, thumbnail):
        self.status_label.text = f"Playing: {title}"
        if thumbnail:
            self.thumbnail.source = thumbnail

    def start_audio(self, url):
        self.stop_audio(None) # Stop any playing audio
        try:
            self.sound = SoundLoader.load(url)
            if self.sound:
                self.sound.play()
            else:
                self.status_label.text = "Error: Could not load audio stream"
        except Exception as e:
            self.status_label.text = f"Playback Error: {str(e)}"

    def stop_audio(self, instance):
        if self.sound:
            self.sound.stop()
            self.status_label.text = "Stopped"

    def show_error(self, error_message):
        self.status_label.text = f"Error: {error_message}"

if __name__ == '__main__':
    AndroidMusicPlayer().run()
