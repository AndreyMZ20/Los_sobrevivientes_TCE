from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

class result(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', size_hint_y=0.15)
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.66)
        self.modulation_button = Button(text='Modulación')
        self.modulation_button.bind(on_press=self.on_modulation_press)
        button_layout.add_widget(self.modulation_button)
        button_layout.add_widget(Button(text='Canal'))
        button_layout.add_widget(Button(text='Demodulación'))
        main_layout.add_widget(button_layout)

        secondary_button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.33, opacity=0)
        self.symbol_encoding_button = Button(text='Codificación de Símbolo')
        self.rcc_button = Button(text='RCC')
        secondary_button_layout.add_widget(self.symbol_encoding_button)
        secondary_button_layout.add_widget(self.rcc_button)
        main_layout.add_widget(secondary_button_layout)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(main_layout)
        layout.add_widget(Widget())  # Widget vacío para ocupar el espacio restante

        return layout

    def on_modulation_press(self, instance):
        self.modulation_button.background_color = (1, 0, 0, 1)  # Cambia el color del botón a rojo
        self.symbol_encoding_button.parent.opacity = 1  # Hace visible el botón 'Codificación de Símbolo'
        self.rcc_button.parent.opacity = 1  # Hace visible el botón 'RCC'

if __name__ == '__main__':
    result().run()
