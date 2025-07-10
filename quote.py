import random
import os
import requests

from kivy.graphics import Rectangle
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDFillRoundFlatButton


class MagicButton(MagicBehavior, MDFillRoundFlatButton):
    pass


class DisplayScreen(Screen):
    quote_text = StringProperty("Press the button to get a quote.")
    button_text = StringProperty("Get Quote")  # <== Add this line
    button_labels = ["Refresh", "Reload", "More", "Next", "Another", "Again"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_image_path = 'bg.jpg'
        self.fetch_bg_image()

        with self.canvas.before:
            self.bg = Rectangle(source=self.bg_image_path, size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

    def fetch_bg_image(self):
        """
        Fetches bg.png from a remote URL and saves it locally.
        """
        url = 'https://github.com/DGuruGod/quoteApp/blob/master/bg.jpg'  # Replace this with your actual URL for bg.png
        try:
            if not os.path.exists(self.bg_image_path):
                response = requests.get(url)
                response.raise_for_status()
                with open(self.bg_image_path, 'wb') as f:
                    f.write(response.content)
                print("Background image downloaded successfully.")
            else:
                print("Background image already exists locally.")
        except requests.RequestException as e:
            print(f"Failed to fetch background image: {e}")
            # You can fallback to a default local image or handle it as you want

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos


    def get_quote(self):
        try:
            r = requests.get('https://api.kanye.rest')
            r.raise_for_status()
            q = r.json()
            self.quote_text = q['quote']

            # Update button text to a new label
            available_labels = [label for label in self.button_labels if label != self.button_text]
            if available_labels:
                self.button_text = random.choice(available_labels)

        except requests.RequestException:
            self.quote_text = "Failed to fetch quote."


class QuoteApp(MDApp):
    def build(self):
        Builder.load_file('quote.kv')
        sm = ScreenManager()
        sm.add_widget(DisplayScreen(name="mainscreen"))
        return sm


if __name__ == '__main__':
    QuoteApp().run()
