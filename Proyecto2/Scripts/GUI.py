from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button  
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Line, Color
import random

class TopFrame(BoxLayout):
    def __init__(self, **kwargs):
        super(TopFrame, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50  # Ajusta esto a la altura que desees para el marco superior
        self.add_widget(Label(text='Modem digital en banda base', font_size=35))
        

class Cod_Binaria(GridLayout):
    def __init__(self, **kwargs):
        super(Cod_Binaria, self).__init__(**kwargs)
        self.cols = 1
        #self.size_hint = (0.5, 0.5)  # Ajusta esto para cambiar el tamaño del cuadro
        #self.pos_hint = {"top": 1, "right": 1}  # Ajusta esto para cambiar la posición del cuadro
        with self.canvas.before:
            Color(0.0, 0.25, 0.5, 1)  # Fondo azul oscuro
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Agregar el label al GridLayout
        self.add_widget(Label(text='Codificacion de simbolos:'))
        
        # Nombres de las opciones
        opciones = ['RZ', 'NRZ', 'MCH']
        
        # Agregar los botones de radio al GridLayout
        for opcion in opciones:
            grid = GridLayout(cols=2)
            grid.add_widget(Label(text=opcion))
            grid.add_widget(CheckBox(group='group'))
            self.add_widget(grid)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Canal(GridLayout):
    def __init__(self, **kwargs):
        super(Canal, self).__init__(**kwargs)
        self.cols = 1
        #self.size_hint = (0.5, 0.5)  # Ajusta esto para cambiar el tamaño del cuadro
        #self.pos_hint = {"top": 1, "right": 1}  # Ajusta esto para cambiar la posición del cuadro
        with self.canvas.before:
            Color(0.0, 0.25, 0.5, 1)  # Fondo azul oscuro
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Agregar el label al GridLayout
        self.add_widget(Label(text='Codificacion de simbolos:'))
        
        # Nombres de las opciones
        opciones = ['RZ', 'NRZ', 'MCH']
        
        # Agregar los botones de radio al GridLayout
        for opcion in opciones:
            grid = GridLayout(cols=2)
            grid.add_widget(Label(text=opcion))
            grid.add_widget(CheckBox(group='group'))
            self.add_widget(grid)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class RCC(GridLayout):
    def __init__(self, **kwargs):
        super(RCC, self).__init__(**kwargs)
        self.cols = 1
        #self.size_hint = (0.5, 0.5)  # Ajusta esto para cambiar el tamaño del cuadro
        with self.canvas.before:
            Color(0.0, 0.25, 0.5, 1)  # Fondo azul oscuro
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Agregar el label al GridLayout
        self.add_widget(Label(text='Codificacion de simbolos:'))
        
        # Nombres de las opciones
        opciones = ['RZ', 'NRZ', 'MCH']
        
        # Agregar los botones de radio al GridLayout
        for opcion in opciones:
            grid = GridLayout(cols=2)
            grid.add_widget(Label(text=opcion))
            grid.add_widget(CheckBox(group='group'))
            self.add_widget(grid)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class HexInput(TextInput):
    def __init__(self, input_class_instance, **kwargs):
        super(HexInput, self).__init__(**kwargs)
        self.halign = 'center'
        self.multiline = False
        self.height = 38  # Ajusta este valor según tus necesidades
        self.size_hint_y = None
        self.size_hint_x = 0.5  # Ajusta este valor a 0.5 para que sea la mitad del ancho de su widget padre
        self.input_class_instance = input_class_instance  # Guarda la referencia al objeto input_class
        self.bind(text=self.on_text)

    def insert_text(self, substring, from_undo=False):
        hex_chars = "0123456789abcdefABCDEF"
        s = ''.join([c for c in substring if c in hex_chars])
        if len(self.text + s) > 8:  # Limita la longitud del texto a 8 caracteres
            return
        else:
            return super(HexInput, self).insert_text(s, from_undo=from_undo)

    def on_text(self, instance, value):
        # Usa la referencia guardada para acceder a binary_label
        try:
            if value == '':
                self.input_class_instance.binary_label.text = ''
            elif value == '0':
                self.input_class_instance.binary_label.text = '0000'
            else:
                binary_value = '_'.join(['{:04}'.format(int(bin(int(c, 16))[2:])) for c in value])
                self.input_class_instance.binary_label.text = binary_value
        except ValueError:
            pass

class input_class(BoxLayout):
    def __init__(self, **kwargs):
        super(input_class, self).__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas.before:
            Color(0.0, 0.25, 0.5, 1)  # Fondo azul oscuro
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Agregar el label al BoxLayout
        self.add_widget(Label(text='Digite la cadena a transmitir (Hexadecimal):'))

        # Agregar el TextInput al BoxLayout
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.hex_input = HexInput(self)
        anchor_layout.add_widget(self.hex_input)
        self.add_widget(anchor_layout)

        # Agregar el Label para mostrar el valor binario
        self.binary_label = Label(text='')
        self.add_widget(self.binary_label)

        # Agrega el botón al BoxLayout
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.my_button = Button(text='Generar número aleatorio', size_hint_x=0.5, size_hint_y=0.5, background_normal='', background_color=(0/255.0, 0/255.0, 139/255.0, 1)) 
        self.my_button.bind(on_press=self.generate_random_hex)  # Vincula la función generate_random_hex al botón
        anchor_layout.add_widget(self.my_button)
        self.add_widget(anchor_layout)
        


    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def generate_random_hex(self, instance):
        random_hex = ''.join([random.choice('0123456789ABCDEF') for _ in range(8)])
        self.hex_input.text = random_hex

        
class BottomFrame(BoxLayout):
    def __init__(self, **kwargs):
        super(BottomFrame, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50  # Ajusta esto a la altura que desees para el marco inferior
        self.add_widget(Button(text='Mi Botón', size_hint=(0.5, None), height=50,
                               background_normal='', background_color=(0.5, 0, 0, 1))) 

class MyApp(App):
    def build(self):
        self.title = 'Modem digital en banda base'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        top_frame = TopFrame(size_hint=(1, 0.1), pos_hint={"top": 1})
        layout.add_widget(top_frame)

        # Crea un GridLayout para contener los widgets
        grid_layout = GridLayout(cols=2, rows=2, spacing=20, padding=[20, 20, 20, 20])   # Ajusta el valor de 'spacing' según necesites

        widget1 = input_class(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget1)

        widget2 = Canal(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget2)

        widget3 = RCC(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget3)
        
        widget4 = Cod_Binaria(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget4)

        layout.add_widget(grid_layout) 

        bottom_frame = BottomFrame(size_hint=(1, 0.1), pos_hint={"y": 0})
        layout.add_widget(bottom_frame)

        return layout

if __name__ == '__main__':
    MyApp().run()