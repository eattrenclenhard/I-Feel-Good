from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, \
    Screen  # from kivy.uix.gridlayout import GridLayout # if we were to code entirely in python, without parsing design.kv using Builder.load_file method
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
from glob import glob
from pathlib import Path
from random import choice
from datetime import datetime
from kivy.logger import Logger, LOG_LEVELS

# log_handler = open('feel_good.log', 'a')
# Logger._log = log_handler.write
Logger.setLevel(LOG_LEVELS["info"])

Builder.load_file('design.kv')


class LoginScreen(Screen):
    def to_signup(self):
        self.manager.current = "signup_screen"

    def login(self, uname_param, pword_param):
        with open('user.json') as f:
            users = json.load(f)

        if uname_param in users.keys():
            f = users[uname_param]['password']
            if pword_param == users[uname_param]['password']:
                Logger.info(f'User `{uname_param}` authenticated')
                self.manager.current = 'login_success_screen'
        else:
            Logger.info(
                f'User `{uname_param}` and password `{pword_param}` does not match any record found in database.')
            self.ids.login_wrong.text = 'wrong username or password'  # conditional update


class LoginSuccessScreen(Screen):
    def logout(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    def get_quote(self, feeling_param):
        feeling_param = feeling_param.lower()
        Logger.info(f'User is `{feeling_param}`!')
        available_feelings = (glob('quotes/*.txt'))
        available_feelings = [Path(p).stem for p in available_feelings]
        Logger.info(f'Available feelings are `{available_feelings}`')
        if feeling_param in available_feelings:
            with open(f'quotes/{feeling_param}.txt', encoding='utf-8') as f:
                quotes = f.readlines()
            quote = choice(quotes)
            Logger.info(f'Quote of the day `{quote}`')
            self.ids.quoteoftheday.text = quote
        else:
            Logger.error(f'Feeling `{feeling_param}` is not supported yet')


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class SignupScreen(Screen):
    def add_user(self, uname_param, pword_param):
        with open('user.json') as f:
            users = json.load(f)
        users[uname_param] = dict(username=uname_param, password=pword_param,
                                  created=datetime.now().strftime('%Y-%m-%d %H-%M-%S'))

        with open('user.json', 'w') as f:
            json.dump(users, f)

        self.manager.current = 'signup_success_screen'


class SignupSuccessScreen(Screen):
    def to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"


class RootWidget(ScreenManager):
    pass


class FeelGood(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    FeelGood().run()

# this app uses a mixture of kivy and python syntax
# kivy file is hierarchy based
# 1) App (FeelGood)
# 2) ScreenManager (RootWidget)
# 3)
