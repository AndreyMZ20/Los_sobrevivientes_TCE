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
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from functions import *
import random

#------------------ CLASE CUADRO TITULO ------------------#
class TopFrame(BoxLayout):
    def __init__(self, **kwargs):
        super(TopFrame, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50  # Ajusta esto a la altura que desees para el marco superior
        self.add_widget(Label(text='Baseband digital modem', font_size=35))

#------------------ CLASES DE ENTRADA ------------------#
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
        kivy_color = hex_to_kivy_color('0B5345')
        with self.canvas.before:
            Color(*kivy_color)  # Fondo personalizado
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.frases = ['Kenobi: -It\'s over, Anakin!', 'Kenobi: -I have the high ground!', 'Anakin: -You underestimate my power...!',
                       'Kenobi knowing what is about to happen:...don\'t try it...', 'Anakin: aAAAAAAAAAAAAAAARGH!', 'Kenobi: -YOU WERE THE CHOSEN ONE!!',
                       'Kenobi: -It was said that you would destroy the sith...', 'Kenobi: -NOT JOIN THEM!', 'Kenobi: -TO BRING BALANCE TO THE FORCE...',
                       'Kenobi: NOT LEAVE IT IN DARKNESS!', 'Vader: -...I HATE YOU!!!', 'Kenobi: -You were my brother...', 'Kenobi: -Anakin...i loved you...!',
                       "......."]  # Tus frases
        self.indice_frase = 0
        Clock.schedule_interval(self.actualizar_frase, 3)  # Programar para cada 5 segundos

        # Agregar el label al BoxLayout
        label1 = Label(text='STEP 1: String to transmit (Hexadecimal)', bold=True)
        label1.size_hint_y = None
        label1.height = 100  
        self.add_widget(label1)

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
        self.my_button = Button(text='Generate random number', size_hint_x=0.5, size_hint_y=0.5, background_normal='', background_color=(0/255.0, 0/255.0, 139/255.0, 1)) 
        self.my_button.bind(on_press=self.generate_random_hex)  # Vincula la función generate_random_hex al botón
        anchor_layout.add_widget(self.my_button)
        self.add_widget(anchor_layout)

    def actualizar_frase(self, dt):
        if self.hex_input.text == '':  # Solo actualizar si el TextInput está vacío
            self.binary_label.text = self.frases[self.indice_frase]
            self.indice_frase = (self.indice_frase + 1) % len(self.frases)  # Circular a través de las frases
        else:
            self.indice_frase = 0  # Reinicia el índice de la frase si el TextInput no está vacío

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def generate_random_hex(self, instance):
        random_hex = ''.join([random.choice('0123456789ABCDEF') for _ in range(8)])
        self.hex_input.text = random_hex

#------------------ CLASE CODIFICACION BINARIA ------------------#
class Cod_Binaria(BoxLayout):
    def __init__(self, **kwargs):
        super(Cod_Binaria, self).__init__(**kwargs)
        self.orientation = 'vertical'
        kivy_color = hex_to_kivy_color('4A235A')
        with self.canvas.before:
            Color(*kivy_color)  # Fondo personalizado
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Agregar el label al GridLayout
        label2 = Label(text='STEP 2: Symbol encoding', bold=True)
        label2.size_hint_y = None
        label2.height = 100  # Asegúrate de que este valor sea el mismo que el anterior
        self.add_widget(label2)
        
        # Nombres de las opciones
        opciones = ['RZ (Return-to-zero)', 'NRZ (Non-Return to Zero)', 'Manchester']
        
        # Crear un GridLayout para contener todos los pares de Label y CheckBox
        grid = GridLayout(cols=2, spacing=[-100,0])

        # Crear un diccionario para almacenar las instancias de CheckBox y su Label correspondiente
        self.checkbox_dict = {}

        for opcion in opciones:
            # Crear un CheckBox y un Label para cada opción
            if opcion == 'RZ (Return-to-zero)':
                checkbox = CheckBox(group='group', active=True)
            elif opcion == 'NRZ (Non-Return to Zero)':
                checkbox = CheckBox(group='group', active=True)  # Este CheckBox estará activo al inicio
            else:
                checkbox = CheckBox(group='group')
            
            label = Label(text=opcion, halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))  # Set 'text_size' to maintain the alignment
            
            # Agregar el CheckBox y el Label al GridLayout
            grid.add_widget(checkbox)
            grid.add_widget(label)

            # Agregar la instancia de CheckBox y su Label correspondiente al diccionario
            self.checkbox_dict[checkbox] = label

        # Crear un BoxLayout para centrar el GridLayout
        box = BoxLayout(orientation='horizontal')
        box.add_widget(grid)  # Agregar el GridLayout al BoxLayout
        box.add_widget(Widget(size_hint_x=0.2))  # Widget vacío para ocupar espacio en la parte derecha

        # Agregar el BoxLayout al widget principal
        self.add_widget(box)

        # Agregar un Widget vacío debajo del GridLayout para moverlo hacia arriba
        self.add_widget(Widget(size_hint_y=0.5))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

#------------------ CLASE RCC ------------------#
class RCC(BoxLayout):
    def __init__(self, **kwargs):
        super(RCC, self).__init__(**kwargs)
        self.orientation = 'vertical'
        kivy_color = hex_to_kivy_color('154360')
        with self.canvas.before:
            Color(*kivy_color)  # Fondo personalizado
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Agregar el label al BoxLayout
        label1 = Label(text='STEP 1: Root of raised cosines', bold=True)
        label1.size_hint_y = None
        label1.height = 100  
        self.add_widget(label1)

        # Agregar otro label justo arriba del Slider
        self.add_widget(Label(text='Roll-off value:'))

        # Agregar el Slider al BoxLayout
        slider = Slider(min=0, max=1, value=0.5)
        self.add_widget(slider)

        # Agregar un Label para mostrar el valor del Slider
        slider_value = Label(text="{:.2f}".format(slider.value))
        
        # Mover el Label que se actualiza con el Slider un poco más arriba
        slider_value.size_hint_y = None
        slider_value.height = 50

        self.add_widget(slider_value)

        # Actualizar el valor del Label cuando el Slider cambie
        slider.bind(value=lambda instance, value: setattr(slider_value, 'text', "{:.2f}".format(value)))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size





#------------------ CLASE CANAL ------------------#
class Canal(GridLayout):
    def __init__(self, **kwargs):
        super(Canal, self).__init__(**kwargs)
        self.cols = 1
        #self.size_hint = (0.5, 0.5)  # Ajusta esto para cambiar el tamaño del cuadro
        #self.pos_hint = {"top": 1, "right": 1}  # Ajusta esto para cambiar la posición del cuadro
        kivy_color = hex_to_kivy_color('841163')
        with self.canvas.before:
            Color(*kivy_color)  # Fondo personalizado
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

#------------------ CLASE BOTON EJECUTAR------------------#       
class BottomFrame(BoxLayout):
    def __init__(self, input_class_instance, checkbox_dict, **kwargs):
        super(BottomFrame, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50  # Ajusta esto a la altura que desees para el marco inferior
        self.input_class = input_class_instance
        self.checkbox_dict = checkbox_dict
        self.add_widget(Button(text='Mi Botón', size_hint=(0.5, None), height=50,
                               background_normal='', background_color=(1, 0, 0, 1),
                               on_press=self.on_button_press))

    def on_button_press(self, instance):
        textbox_value = self.input_class.hex_input.text
        if textbox_value != '':
            active_checkbox = next((checkbox for checkbox in self.checkbox_dict if checkbox.active), None)
            active_label_text = self.checkbox_dict[active_checkbox].text if active_checkbox else None
            # Codifica el valor del textbox y traza la señal
            signal, bit_string = encode(textbox_value, active_label_text)
            print(signal)
            print(bit_string)
            #plot_signal(signal, bit_string)


#------------------ CLASE PRINCIPAL ------------------#
class Class_Main(App):
    def build(self):
        self.title = 'Modem digital en banda base'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        top_frame = TopFrame(size_hint=(1, 0.1), pos_hint={"top": 1})
        layout.add_widget(top_frame)

        # Crea un GridLayout para contener los widgets
        grid_layout = GridLayout(cols=2, rows=2, spacing=20, padding=[20, 20, 20, 20])   # Ajusta el valor de 'spacing' según necesites

        widget1 = input_class(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget1)

        widget2 = Cod_Binaria(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget2)

        widget3 = RCC(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget3)

        widget4 = Canal(size_hint=(0.45, 0.45))  # Ajusta esto para cambiar el tamaño del cuadro
        grid_layout.add_widget(widget4)

        layout.add_widget(grid_layout) 

        bottom_frame = BottomFrame(widget1, widget2.checkbox_dict, size_hint=(1, 0.1), pos_hint={"y": 0})
        layout.add_widget(bottom_frame)

        return layout

if __name__ == '__main__':
    Class_Main().run()
