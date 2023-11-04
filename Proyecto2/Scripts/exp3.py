from kivy.app import App
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

class MyApp(App):
    def build(self):
        root = BoxLayout(orientation='horizontal')

        menu = Accordion(orientation='vertical', size_hint_x=0.2)

        item_modulacion = AccordionItem(title='Modulación')
        submenu_modulacion = GridLayout(cols=1)
        submenu_modulacion.add_widget(Button(text='Codificador de símbolos',
                                             on_press=self.plot,
                                             size_hint_y=None,
                                             height=40))
        submenu_modulacion.add_widget(Button(text='RCC',
                                             on_press=self.plot,
                                             size_hint_y=None,
                                             height=40))
        item_modulacion.add_widget(submenu_modulacion)
        menu.add_widget(item_modulacion)

        item_modulacion = AccordionItem(title='Demodulación')
        submenu_modulacion = GridLayout(cols=1)
        submenu_modulacion.add_widget(Button(text='Decoficador de símbolos',
                                             on_press=self.plot,
                                             size_hint_y=None,
                                             height=40))
        submenu_modulacion.add_widget(Button(text='Filtro ',
                                             on_press=self.plot,
                                             size_hint_y=None,
                                             height=40))
        item_modulacion.add_widget(submenu_modulacion)
        menu.add_widget(item_modulacion)
        
        item_modulacion = AccordionItem(title='Canal')
        menu.add_widget(item_modulacion)

        root.add_widget(menu)

        self.plot_area = BoxLayout(orientation='vertical', size_hint_x=0.8)
        root.add_widget(self.plot_area)

        return root

    def plot(self, instance):
        plt.plot([1, 2, 3, 4, 5], [1, 3, 2, 4, 3])
        self.root.children[0].add_widget(FigureCanvasKivyAgg(plt.gcf()))

MyApp().run()
