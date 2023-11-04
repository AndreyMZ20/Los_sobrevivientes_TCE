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
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.accordion import Accordion, AccordionItem

from functions import *
import random

#------------------ CLASE CUADRO TITULO ------------------#
class TopFrame(BoxLayout):
    def __init__(self, **kwargs):
        super(TopFrame, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50  # Ajusta esto a la altura que desees para el marco superior
        self.add_widget(Label(text='Baseband Digital Modem', font_size=35))

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
                self.input_class_instance.binary_label.text = 'Type the string to modulate'
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
        kivy_color = hex_to_kivy_color('154360')
        with self.canvas.before:
            Color(*kivy_color)  # Fondo personalizado
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

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
        self.binary_label = Label(text='Welcome! Type the string to modulate', markup=True)
        self.add_widget(self.binary_label)

        # Agrega el botón al BoxLayout
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.my_button = Button(text='Random number', size_hint_x=0.35, size_hint_y=0.55, background_normal='', background_color=(26/255.0, 119/255.0, 177/255.0, 1)) 
        self.my_button.bind(on_press=self.generate_random_hex)  # Vincula la función generate_random_hex al botón
        anchor_layout.add_widget(self.my_button)
        self.add_widget(anchor_layout)

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
        self.checkbox_codsimb = {}

        for opcion in opciones:
            # Crear un CheckBox y un Label para cada opción
            if opcion == 'RZ (Return-to-zero)':
                checkbox = CheckBox(group='group', active=True)
            elif opcion == 'NRZ (Non-Return to Zero)':
                checkbox = CheckBox(group='group', active=False)  # Este CheckBox estará desactivado al inicio
            else:
                checkbox = CheckBox(group='group', active=False)  # Este CheckBox estará desactivado al inicio
            
            label = Label(text=opcion, halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))  # Set 'text_size' to maintain the alignment
            
            # Agregar el CheckBox y el Label al GridLayout
            grid.add_widget(checkbox)
            grid.add_widget(label)

            # Agregar la instancia de CheckBox y su Label correspondiente al diccionario
            self.checkbox_codsimb[checkbox] = label

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
        kivy_color = hex_to_kivy_color('1C6F73')
        with self.canvas.before:
            Color(*kivy_color)  # Fondo personalizado
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Agregar el label al BoxLayout
        label1 = Label(text='STEP 3: Root of raised cosines', bold=True)
        label1.size_hint_y = None
        label1.height = 100  
        self.add_widget(label1)

        # Agregar otro label justo arriba del Slider
        self.add_widget(Label(text='Roll-off value:'))

        # Agregar el Slider al BoxLayout
        slider = Slider(min=0, max=1, value=0.5, step=0.01)
        self.add_widget(slider)

        # Agregar un Label para mostrar el valor del Slider
        self.roll_off_value = Label(text="{:.2f}".format(slider.value))
        
        # Mover el Label que se actualiza con el Slider un poco más arriba
        self.roll_off_value.size_hint_y = None
        self.roll_off_value.height = 50

        self.add_widget(self.roll_off_value)

        # Actualizar el valor del Label cuando el Slider cambie
        slider.bind(value=lambda instance, value: setattr(self.roll_off_value, 'text', "{:.2f}".format(value)))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

#------------------ CLASE CANAL ------------------#
class MySlider(Slider):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.scroll_enabled = False
        return super(MySlider, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.parent.scroll_enabled = True
        return super(MySlider, self).on_touch_up(touch)
    
class AdvancedSettingsPopup(Popup):
    def __init__(self, canal_instance, num_sliders, **kwargs):
        super(AdvancedSettingsPopup, self).__init__(**kwargs)
        self.title = 'Advanced Configuration (Magnitude and phase)'
        self.size_hint = (0.75, 0.75)  # Ajusta el tamaño del Popup al 70% del tamaño de la ventana
        self.canal = canal_instance

        # Crear un GridLayout con tres columnas
        self.grid = GridLayout(cols=6, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        # Crear los Sliders y Labels para cada echo
        self.sliders_mag = []
        self.sliders_phase = []

        # Create labels for each slider
        self.labels_mag = []
        self.labels_phase = []

        # Crear un BoxLayout con orientación vertical
        self.box_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.box_layout.bind(minimum_height=self.box_layout.setter('height'))

        # Crear los Sliders y Labels para cada echo
        for i in range(num_sliders):
            # Crear una nueva fila para cada echo
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None)

            # Primera columna: MAGNITUDES
            label_mag_name = Label(text=f'Mag{i+1}:', size_hint_x=0.3)
            row_layout.add_widget(label_mag_name)

            # Segunda columna: Slider para la magnitud del echo
            slider_mag = MySlider(min=0, max=1, value=self.canal.mag_echo[i], step=0.01)
            slider_mag.bind(value=self.on_slider_value_mag)
            row_layout.add_widget(slider_mag)
            self.sliders_mag.append(slider_mag)

            # Tercera columna: Label para mostrar el valor del Slider
            label_mag = Label(text="{:.2f}".format(slider_mag.value), size_hint_x=0.2)
            row_layout.add_widget(label_mag)
            self.labels_mag.append(label_mag)

            # Cuarta columna: nombre del echo
            label_phase_name = Label(text=f' | Phase{i+1}:', size_hint_x=0.3)
            row_layout.add_widget(label_phase_name)

            # Quinta columna: Slider para la fase del echo
            slider_phase = MySlider(min=0, max=360, value=self.canal.fase_echo[i], step = 1)
            slider_phase.bind(value=self.on_slider_value_phase)
            row_layout.add_widget(slider_phase)
            self.sliders_phase.append(slider_phase)

            # Sexta columna: Label para mostrar el valor del Slider
            label_phase = Label(text=str(int(slider_phase.value)), size_hint_x=0.2)
            row_layout.add_widget(label_phase)
            self.labels_phase.append(label_phase)

            # Agregar la fila al BoxLayout
            self.box_layout.add_widget(row_layout)

        # Crear un BoxLayout con orientación vertical como contenedor principal
        main_layout = BoxLayout(orientation='vertical')

        # Crear un ScrollView para contener el BoxLayout con los Sliders y Labels
        scrollview = ScrollView(size_hint=(1, 0.8))  # Ajusta el size_hint para que no ocupe toda la ventana
        scrollview.scroll_enabled = True
        scrollview.add_widget(self.box_layout)

        # Agregar el ScrollView al contenedor principal
        main_layout.add_widget(scrollview)

        # Crear un GridLayout con dos columnas
        button_layout = GridLayout(cols=2, size_hint=(1, 0.1))

        # Crear el primer botón
        button1 = Button(text='Generate Random')  
        button1.bind(on_press=lambda instance: self.update_values(num_sliders))
        button_layout.add_widget(button1)

        # Crear el segundo botón para cerrar la ventana emergente
        button2 = Button(text='Close')
        button2.bind(on_press=self.dismiss)  # Enlazar el evento 'on_press' al método 'dismiss' para cerrar la ventana emergente
        button_layout.add_widget(button2)

        # Agregar el GridLayout al contenedor principal
        main_layout.add_widget(button_layout)

        # Agregar el contenedor principal al Popup
        self.content = main_layout

    def update_values(self, num_sliders):

        if (num_sliders != 0):
            # Generar nuevos valores aleatorios para mag_echo y fase_echo hasta num_sliders
            self.canal.mag_echo[:num_sliders] = [round(random.random(), 2) for _ in range(num_sliders)]
            self.canal.fase_echo[:num_sliders] = [random.randint(0, 360) for _ in range(num_sliders)]

            # Actualizar los valores de los sliders y sus labels correspondientes
            for i in range(len(self.sliders_mag)):
                self.sliders_mag[i].value = self.canal.mag_echo[i]
                self.labels_mag[i].text = "{:.2f}".format(self.canal.mag_echo[i])
                self.sliders_phase[i].value = self.canal.fase_echo[i]
                self.labels_phase[i].text = str(int(self.canal.fase_echo[i]))

    def on_slider_value_mag(self, instance, value):
        index = self.sliders_mag.index(instance)
        # Update the corresponding label when the slider value changes
        self.labels_mag[index].text = "{:.2f}".format(value)
        self.canal.mag_echo[index] = value

    def on_slider_value_phase(self, instance, value):
        index = self.sliders_phase.index(instance)
        # Update the corresponding label when the slider value changes
        self.labels_phase[index].text = str(int(value))
        self.canal.fase_echo[index] = value

class Canal(BoxLayout):
    def __init__(self, **kwargs):
        super(Canal, self).__init__(**kwargs)
        self.orientation = 'vertical'
        kivy_color = hex_to_kivy_color('841163')
        with self.canvas.before:
            Color(*kivy_color)  # Fondo personalizado
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Crear una lista con 40 números aleatorios en el rango de 0 a 1
        self.mag_echo = [round(random.random(), 2) for _ in range(35)]

        # Crear una lista con 40 números aleatorios en el rango de 0 a 360
        self.fase_echo = [random.randint(0, 360) for _ in range(35)]

        # Crear un Slider y un Label para mostrar su valor
        self.slider = Slider(min=0, max=1, value=0, step=0.01)
        self.slider_label = Label(text="0")
        self.slider.bind(value=self.on_slider_value)

        # Crear un Label para mostrar el estado del CheckBox
        self.checkbox_label = Label(text="Noise level:")

        # Agregar el label al GridLayout
        label2 = Label(text='STEP 4: Channel model', bold=True)
        label2.size_hint_y = None
        label2.height = 100  # Asegúrate de que este valor sea el mismo que el anterior
        self.add_widget(label2)
        
        # Nombres de las opciones
        opciones = ['AWGN', 'ECHO']
                
        # Crear un GridLayout para contener todos los pares de Label y CheckBox
        grid = GridLayout(cols=4, spacing=[-50,0])

        # Crear un diccionario para almacenar las instancias de CheckBox y su Label correspondiente
        self.checkbox_codsimb = {}

        for opcion in opciones:
            # Crear un CheckBox y un Label para cada opción
            if opcion == 'AWGN':
                checkbox = CheckBox(group='group1', active=True)
                checkbox.bind(active=self.on_checkbox_active)  # Agregar un enlace al evento 'active'
            else:
                checkbox = CheckBox(group='group1', active=False)  # Este CheckBox estará desactivado al inicio
                checkbox.bind(active=self.on_checkbox_active)  # Agregar un enlace al evento 'active'
            
            label = Label(text=opcion, halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))  # Set 'text_size' to maintain the alignment
            
            # Agregar el CheckBox y el Label al GridLayout
            grid.add_widget(checkbox)
            grid.add_widget(label)

            # Agregar la instancia de CheckBox y su Label correspondiente al diccionario
            self.checkbox_codsimb[checkbox] = label

        # Crear un BoxLayout para centrar el GridLayout
        box = BoxLayout(orientation='horizontal')
        box.add_widget(grid)  # Agregar el GridLayout al BoxLayout

        # Agregar el BoxLayout al widget principal
        self.add_widget(box)

        # Agregar el Label al widget principal antes del Slider y su Label asociado
        self.add_widget(self.checkbox_label)

        # Agregar el Slider y el Label al widget principal después de los checkboxes
        self.add_widget(self.slider)
        self.add_widget(self.slider_label)

        # Agrega el botón al BoxLayout
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.my_button = Button(text='Advanced settings', size_hint_x=0.35, size_hint_y=0.9, background_normal='', background_color=(135/255.0, 65/255.0, 160/255.0, 1), opacity=0)
        self.my_button.bind(on_press=self.on_button_press) 
        anchor_layout.add_widget(self.my_button)
        self.add_widget(anchor_layout)

    def on_button_press(self, instance):
        # Obtener el valor del label del slider
        slider_value = int(self.slider_label.text)
        # Crear una instancia de AdvancedSettingsPopup y pasar el valor del slider
        self.popup = AdvancedSettingsPopup(self, slider_value)
        # Abrir la ventana emergente
        self.popup.open()

    def on_checkbox_active(self, instance, value):
        if self.checkbox_codsimb[instance].text == 'AWGN':
            if value:
                self.slider.min = 0
                self.slider.max = 1
                self.slider.step = 0.01
                self.checkbox_label.text = "Noise level:"
                self.my_button.opacity = 0  # Hacer invisible el botón cuando 'ECHO' no está 
            else:
                self.slider.min = 0
                self.slider.max = 35
                self.slider.step = 1
                self.checkbox_label.text = "Number of echoes:"
                self.my_button.opacity = 1  # Hacer visible el botón cuando 'ECHO' está activo
        # Restablecer el valor del Slider a cero y actualizar el texto del Label
        self.slider.value = 0
        self.on_slider_value(self.slider, self.slider.value)

    def on_slider_value(self, instance, value):
        # Buscar el CheckBox 'AWGN' en el diccionario
        for checkbox, label in self.checkbox_codsimb.items():
            if label.text == 'AWGN':
                awgn_checkbox = checkbox
                break

        # Formatear el valor del Slider
        if awgn_checkbox.active:
            # Si 'AWGN' está activo, mostrar dos decimales
            self.slider_label.text = "{:.2f}".format(value)
        else:
            # Si 'AWGN' no está activo, no mostrar decimales
            self.slider_label.text = "{:.0f}".format(value)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

#------------------ CLASE BOTON EJECUTAR------------------#       
class BottomFrame(BoxLayout):
    def __init__(self, main_app, input_class_instance, checkbox_codsimb, roll_off,  **kwargs):
        super(BottomFrame, self).__init__(**kwargs)
        self.main_app = main_app
        self.size_hint_y = None
        self.height = 50  # Ajusta esto a la altura que desees para el marco inferior
        self.input_class = input_class_instance
        self.checkbox_codsimb = checkbox_codsimb
        self.roll_off = roll_off
        self.add_widget(Button(text='RUN', size_hint=(0.5, None), height=50,
                               background_normal='', background_color=(0.65, 0, 0, 1),
                               on_press=self.on_button_press))

    def on_button_press(self, instance):
        textbox_value = self.input_class.hex_input.text
        if textbox_value == '':
            self.input_class.binary_label.text = '[color=ff0000]ERROR: No data available[/color]'
            Clock.schedule_once(self.reset_label_text, 3)
        else:
            active_checkbox = next((checkbox for checkbox in self.checkbox_codsimb if checkbox.active), None)
            if active_checkbox != None:
                roll_off = float(self.roll_off.text)
                tipo_cod_simb = self.checkbox_codsimb[active_checkbox].text if active_checkbox else None
                # Codifica el valor del textbox
                signal, bit_string = encode(textbox_value, tipo_cod_simb)
                # Aplica el coseno alzado
                signal_rcc = cose_alzado_func(roll_off, signal)
                # Abrir ventana de resultados
                App.get_running_app().stop()  # Detiene la aplicación actual
                result(self.main_app, signal, bit_string, tipo_cod_simb, signal_rcc).run()  # Ejecuta la nueva aplicación
            else:
                self.input_class.binary_label.text = '[color=ff0000]ERROR: Select a binary encoder[/color]'
                Clock.schedule_once(self.reset_label_text, 3)

    def reset_label_text(self, dt):
        self.input_class.binary_label.text = '[color=ffffff]Type the string to modulate[/color]'

#------------------ CLASE RESULTADO ------------------#
class result(App):
    def __init__(self, main_app, signal, bit_string, tipo_cod_simb, signal_rcc, **kwargs):
        super(result, self).__init__(**kwargs)
        self.main_app = main_app
        self.signal = signal
        self.bit_string = bit_string
        self.tipo_cod_simb = tipo_cod_simb
        self.current_plot = None
        self.signal_rcc = signal_rcc

    def build(self):
        root = BoxLayout(orientation='horizontal')

        menu = Accordion(orientation='vertical', size_hint_x=0.2)
        
        item_result = AccordionItem(title='Results', collapse=True)
        item_result.background_normal = 'results_color.png'
        item_result.background_selected = 'results_color.png'
        submenu_result = GridLayout(cols=1)
        kivy_color = hex_to_kivy_color('2E96B5')
        submenu_result.add_widget(Button(text='General results',
                                            on_press=self.on_save_button_press,
                                            size_hint_y=None,
                                            height=40, 
                                            background_normal='', background_color=kivy_color))
        kivy_color = hex_to_kivy_color('2E7FB5')
        submenu_result.add_widget(Button(text='Data obtained',
                                            on_press=self.on_back_button_press,
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        item_result.add_widget(submenu_result)
        menu.add_widget(item_result)

        item_result = AccordionItem(title='Modulation', collapse=True)
        item_result.background_normal = 'mod_color.png'
        item_result.background_selected = 'mod_color.png'
        submenu_result = GridLayout(cols=1)
        kivy_color = hex_to_kivy_color('2E52B5')
        submenu_result.add_widget(Button(   text='Symbol Encoding',
                                            on_press=lambda instance: self.plot_cod_simb(instance, 'Modulation'),
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        kivy_color = hex_to_kivy_color('2E3CB5')
        submenu_result.add_widget(Button(   text='Root of Raised Cosines',
                                            on_press=lambda instance: self.plot_rcc(instance, 'Modulation'),
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        kivy_color = hex_to_kivy_color('362EB5')
        submenu_result.add_widget(Button(   text='Channel',
                                            on_press=self.plot,
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        item_result.add_widget(submenu_result)
        menu.add_widget(item_result)

        item_result = AccordionItem(title='Demodulation', collapse=True)
        item_result.background_normal = 'dem_color.png'
        item_result.background_selected = 'dem_color.png'
        submenu_result = GridLayout(cols=1)
        kivy_color = hex_to_kivy_color('632EB5')
        submenu_result.add_widget(Button(   text='Attached filter',
                                            on_press=self.plot,
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        kivy_color = hex_to_kivy_color('7A2EB5')
        submenu_result.add_widget(Button(   text='FIR Equalizer',
                                            on_press=self.plot,
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        kivy_color = hex_to_kivy_color('902EB5')
        submenu_result.add_widget(Button(   text='Error detection \n and correction',
                                            on_press=self.plot,
                                            size_hint_y=None,
                                            height=60, 
                                            background_normal='', background_color=kivy_color))
        kivy_color = hex_to_kivy_color('A72EB5')
        submenu_result.add_widget(Button(   text='symbol decoder',
                                            on_press=self.plot,
                                            size_hint_y=None,
                                            height=40, 
                                            background_normal='', background_color=kivy_color))
        item_result.add_widget(submenu_result)
        menu.add_widget(item_result)

        item_result = AccordionItem(title='Options', collapse=True)
        item_result.background_normal = 'opt_color.png'
        item_result.background_selected = 'opt_color.png'
        submenu_result = GridLayout(cols=1)
        kivy_color = hex_to_kivy_color('B52E96')
        submenu_result.add_widget(Button(   text='Save all',
                                            on_press=self.on_save_button_press,
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        kivy_color = hex_to_kivy_color('B52E7F')
        submenu_result.add_widget(Button(   text='Back',
                                            on_press=self.on_back_button_press,
                                            size_hint_y=None,
                                            height=40,
                                            background_normal='', background_color=kivy_color))
        item_result.add_widget(submenu_result)
        menu.add_widget(item_result)

        item_result = AccordionItem(title='')
        item_result.opacity = 0
        #item_result.height = 500  # Esto establecerá la altura del item en 500 píxeles
        #item_result.size_hint_y = None  # Esto es necesario para que 'height' no sea ignorado
        menu.add_widget(item_result)

        root.add_widget(menu)

        self.plot_area = BoxLayout(orientation='vertical', size_hint_x=0.8)
        root.add_widget(self.plot_area)

        # Título
        self.title_label = Label(text='General Results', size_hint=(1, 0.1), halign='center', font_size=30)
        self.plot_area.add_widget(self.title_label)

        return root

    def plot(self, instance, menu_name):
        self.title_label.text =menu_name + '\n' + instance.text
        plt.plot([1, 2, 3, 4, 5], [1, 3, 2, 4, 3])
        self.plot_area.add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    def plot_cod_simb(self, instance, menu_name):
        self.title_label.text =menu_name + '\n' + instance.text
        if self.current_plot:
            self.plot_area.remove_widget(self.current_plot)

        if self.tipo_cod_simb == 'RZ (Return-to-zero)':
            plot_rz(self, self.signal, self.bit_string)
        elif self.tipo_cod_simb == 'NRZ (Non-Return to Zero)':
            plot_nrz(self, self.signal, self.bit_string)
        else:
            plot_manchester(self, self.signal, self.bit_string)

    def plot_rcc(self, instance, menu_name):
        self.title_label.text =menu_name + '\n' + instance.text
        if self.current_plot:
            self.plot_area.remove_widget(self.current_plot)
        graficar_rcc(self, self.signal_rcc)

    def on_back_button_press(self, instance):
        App.get_running_app().stop()  # Detiene la aplicación actual
        Class_Main().run()  # Crea una nueva instancia de la aplicación principal y la ejecuta

    def on_save_button_press(self, instance):
        # Aquí es donde manejas lo que sucede cuando se presiona el botón 'Save all'
        pass
    


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

        bottom_frame = BottomFrame(main_app, widget1, widget2.checkbox_codsimb, widget3.roll_off_value, size_hint=(1, 0.1), pos_hint={"y": 0})
        layout.add_widget(bottom_frame)

        return layout

if __name__ == '__main__':
    main_app = Class_Main()
    main_app.run()