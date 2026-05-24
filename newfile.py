import subprocess
import sys

# Pehle check karenge Kivy install hai ya nahi
try:
    import kivy
except ImportError:
    print("Kivy install ho raha hai...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "kivy"])

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class AdvancedCalculatorApp(App):
    def build(self):
        # Ek list banayi hai jisme saari history save hoti rahegi
        self.history_list = []

        # Main layout (Vertical)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. Main Display Screen
        self.display = TextInput(
            multiline=False, 
            readonly=True, 
            halign='right', 
            font_size=55,
            background_color=(0.95, 0.95, 0.95, 1),
            size_hint=(1, 0.25)
        )
        main_layout.add_widget(self.display)

        # 2. Buttons ka Grid (4 columns)
        buttons_grid = GridLayout(cols=4, spacing=10, size_hint=(1, 0.75))

        # Buttons ki list—isme 'H' button daal diya hai History ke liye
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+',
            'History'  # Ye raha tumhara khas button!
        ]

        for button_text in buttons:
            # History button ko Orange color denge takia alag se chamke
            if button_text == 'History':
                btn_color = (1, 0.5, 0, 1)
                # History button ko poori ek line (4 columns) jitna bada karne ke liye
                size_h = (4, 1) 
            elif button_text in ['=', 'C']:
                btn_color = (0.2, 0.6, 1, 1)
                size_h = (1, 1)
            else:
                btn_color = (0.25, 0.25, 0.25, 1)
                size_h = (1, 1)

            btn = Button(
                text=button_text, 
                font_size=28,
                background_color=btn_color,
                size_hint=size_h
            )
            btn.bind(on_press=self.on_button_click)
            buttons_grid.add_widget(btn)

        main_layout.add_widget(buttons_grid)
        return main_layout

    # History dekhne ke liye Pop-up Window
    def show_history_popup(self):
        # Agar koi history nahi hai toh user ko batao
        if not self.history_list:
            history_text = "Abhi tak koi hisab nahi kiya gaya hai!"
        else:
            # Saari history ko ek ke niche ek jodne ke liye (\n)
            history_text = "\n".join(self.history_list)

        # Pop-up ke andar ka layout
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ScrollView lagaya hai takia agar lambi history ho toh ungli se scroll ho sake
        scroll = ScrollView()
        history_label = Label(text=history_text, font_size=22, halign='center', size_hint_y=None)
        history_label.bind(texture_size=history_label.setter('size')) # Auto size adjust
        scroll.add_widget(history_label)
        
        popup_layout.add_widget(scroll)

        # Pop-up band karne ka button
        close_btn = Button(text='Close', size_hint=(1, 0.2), background_color=(0.8, 0.2, 0.2, 1))
        popup_layout.add_widget(close_btn)

        # Pop-up window ko taiyar karna
        popup = Popup(title='Calculation History', content=popup_layout, size_hint=(0.8, 0.7))
        close_btn.bind(on_press=popup.dismiss) # Button dabate hi pop-up band
        
        popup.open() # Pop-up ko screen par dikhana

    # Button click handle karne ka logic
    def on_button_click(self, instance):
        current_text = self.display.text
        button_text = instance.text

        if button_text == 'History':
            # Agar History button dabaya toh popup khulega
            self.show_history_popup()
            
        elif button_text == 'C':
            self.display.text = ''
            
        elif button_text == '=':
            if current_text:
                try:
                    result = str(eval(current_text))
                    # Naye hisab ko background me list me save kar rahe hain
                    self.history_list.append(f"{current_text} = {result}")
                    self.display.text = result
                except Exception:
                    self.display.text = 'Error'
        else:
            if current_text == 'Error':
                self.display.text = button_text
            else:
                self.display.text = current_text + button_text

if __name__ == '__main__':
    AdvancedCalculatorApp().run()
