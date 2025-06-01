import random

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
import requests
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.button import MDFillRoundFlatButton


class MagicButton(MagicBehavior, MDFillRoundFlatButton):
    pass



class DisplayScreen(Screen):
    quote_text = StringProperty("Press the button to get a quote.")
    button_text = StringProperty("Get Quote")  # <== Add this line
    button_labels = ["Refresh", "Reload", "More", "Next", "Another", "Again"]


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

                
        except requests.RequestException as e:
            self.quote_text = "Failed to fetch quote."

class QuoteApp(MDApp):
    def build(self):
        Builder.load_file('quote.kv')
        sm = ScreenManager()
        sm.add_widget(DisplayScreen(name="mainscreen"))
        return sm

if __name__ == '__main__':
    QuoteApp().run()
