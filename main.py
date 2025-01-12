from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, \
    Screen  # from kivy.uix.gridlayout import GridLayout # if we were to code entirely in python, without parsing design.kv using Builder.load_file method
import json
from datetime import datetime

Builder.load_file('design.kv')


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "signup_screen"


class SignupScreen(Screen):
    def add_user(self, uname_param, pword_param):
        with open('user.json') as f:
            users = json.load(f)
        users[uname_param] = dict(username=uname_param, password=pword_param,
                                  created=datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
        print(users)
        with open('user.json', 'w') as f:
            json.dump(users, f)


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
