# Import necessary modules from Kivy library
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Import the text-to-speech library
import pyttsx3
import threading

# Create a class for text-to-voice functionality
class TextToVoice:
    def __init__(self, lang='en', voice_id=None):
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        self.lang = lang
        self.voice_id = voice_id
        self.set_language_and_voice()
        self.is_stopped = False  # Flag to indicate if audio playback is stopped

    def set_language_and_voice(self):
        # Set the language and voice for the text-to-speech engine
        if self.lang:
            self.engine.setProperty('language', self.lang)
        if self.voice_id:
            self.engine.setProperty('voice', self.voice_id)

    def set_speech_rate(self, rate):
        # Set the speech rate (words per minute) for the text-to-speech engine
        self.engine.setProperty('rate', rate)

    def text_to_voice(self, text):
        try:
            # Convert the given text to voice and wait for completion
            self.engine.say(text)
            self.engine.runAndWait()
        except RuntimeError:
            pass  # Catch the exception raised when the stop button is pressed

        # Set the flag to indicate that audio playback is stopped
        self.is_stopped = True

    def stop_voice(self):
        # Stop the ongoing voice playback
        if not self.is_stopped:
            self.engine.stop()

# Create the main application class inheriting from Kivy's App class
class TextToSpeechApp(App):
    def build(self):
        Window.size = (450, 640)
        self.title = 'Text to Speech'
        self.text_to_voice = TextToVoice(lang='en')
        self.speech_rate = 140
        self.is_playing = False

        self.layout = BoxLayout(orientation='vertical')

        # Set the background image
        self.bg_image = Image(source='Background.png', allow_stretch=True, keep_ratio=False)
        self.layout.add_widget(self.bg_image)

        # Add a BoxLayout to hold the text input
        text_input_layout = BoxLayout(size_hint=(1, 0.2))
        self.text_input = TextInput(font_size=20, multiline=True, size_hint=(0.5, 1.5), pos_hint={'center_x': 0.5})
        text_input_layout.add_widget(self.text_input)

        self.layout.add_widget(text_input_layout)

        # Add a Slider for speed adjustment
        self.speed_layout = BoxLayout(size_hint=(1, 0.1), spacing=10, padding=10)
        self.speed_label = Label(text='Speed', size_hint=(0.2, 1))
        self.speed_layout.add_widget(self.speed_label)
        self.speed_slider = Slider(min=100, max=300, value=self.speech_rate, size_hint=(0.8, 1))
        self.speed_slider.bind(value=self.on_speed_slider_value_change)
        self.speed_layout.add_widget(self.speed_slider)
        self.layout.add_widget(self.speed_layout)

        # Add a BoxLayout to hold the buttons
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10, padding=10)

        # Customize the "Play" button
        self.play_button = Button(text='Play', background_normal='', background_color=(0.2, 0.7, 0.3, 1))
        self.play_button.bind(on_press=self.on_play_button_press)
        buttons_layout.add_widget(self.play_button)

        # Customize the "Exit" button
        self.exit_button = Button(text='Exit', background_normal='', background_color=(0.7, 0.2, 0.3, 1))
        self.exit_button.bind(on_press=self.on_exit_button_press)
        buttons_layout.add_widget(self.exit_button)

        self.layout.add_widget(buttons_layout)

        return self.layout

    def on_play_button_press(self, instance):
        # Handle the "Play" button press event
        text = self.text_input.text.strip()
        if text:
            self.is_playing = True
            self.text_to_voice.is_stopped = False  # Reset the flag before playing
            self.text_to_voice.set_speech_rate(self.speech_rate)
            # Start text-to-voice conversion in a separate thread to prevent freezing the UI
            threading.Thread(target=self.text_to_voice.text_to_voice, args=(text,)).start()
            self.is_playing = False
        else:
            self.show_popup("Error", "Please enter some text.")

    def on_exit_button_press(self, instance):
        # Handle the "Exit" button press event
        self.text_to_voice.stop_voice()  # Stop the voice playback
        App.get_running_app().stop()  # Close the Kivy application

    def on_speed_slider_value_change(self, instance, value):
        # Handle the speed slider value change event
        self.speech_rate = value

    def show_popup(self, title, content):
        # Display a popup with the given title and content
        popup_layout = BoxLayout(orientation='vertical')
        popup_label = Label(text=content)
        popup_layout.add_widget(popup_label)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.3))
        popup.open()

# Run the application if this script is executed directly
if __name__ == "__main__":
    TextToSpeechApp().run()
