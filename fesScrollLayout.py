from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import pandas as pd
import os


#file_path = os.path.join(os.path.dirname(__file__), 'FesCollection', 'FesData.xlsx')
df = pd.read_excel("FesData.xlsx")

available_city = ["CaoBang", "HaNoi", "QuangNinh", "TPHCM"]

Window.size = (360, 640)
Window.clearcolor = (.7,.7,.7,1)

class ScrollableText(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Create a ScrollView
        scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)

        # Create a Label with long text
        text = ""
        self.label = Label(
            text=text,
            font_size = 20,
            size_hint_y=None,
            text_size=(Window.width * 0.95, None),
            halign='left',
            valign='top',
            padding=(10, 10),
            color = (0,0,0,1)
        )

        # Dynamically update label height based on text size
        self.label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        # Make text wrap dynamically when window resizes
        self.label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))

        # Add label into scrollview
        scroll_view.add_widget(self.label)

        # Add scrollview into main layout
        self.add_widget(scroll_view)

class mainFesLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(mainFesLayout,self).__init__(**kwargs)
        self.size_hint=(1,0.95)
        self.pos_hint = {"top" : 1}
        #self - fesFinder (default city: hanoi) - fesscroll - fesdesc
        #     - cityLayout (pop upp) - cityscroll - cityButtons
        #                            - exitButton + label
        # list of button to select city
        self.defaultCity = "HaNoi"
        self.isFesList = True
        self.isCityList = False
        
        #CITY LAYOUT
        self.cityButtons = GridLayout(cols=1, spacing=10, size_hint_y = None)
        self.cityButtons.bind(minimum_height=self.cityButtons.setter('height'))

        for city in available_city:
            btn = Button(text = f"{city}",
                         size_hint_y=None, 
                         height=100
                    )
            btn.bind(on_press = self.select_city)
            self.cityButtons.add_widget(btn)    
        self.cityButtons.add_widget(Button(text = "check",
                                      size_hint_y = None,
                                      height = 100)) 

        self.scroll = ScrollView(
            size_hint=(1, 0.9),
            pos_hint = {"top":0.85}
            )                   
        self.scroll.add_widget(self.cityButtons) 
        
        self.cityLayout = FloatLayout(size_hint = (1,0.9),pos_hint = {'top':1})
        self.cityLayout.add_widget(self.scroll)
        self.cityLayout.add_widget(Label(text = "Which city", size_hint = (1, 0.1) ,pos_hint = {"top" : 0.95}))
        
        self.exitButton1 = Button(text = "Back", size_hint = (0.4,0.05), pos_hint ={"top": 1})
        self.exitButton1.bind(on_press = self.back_to_fes_list1)
        self.cityLayout.add_widget(self.exitButton1)

        #FESFINDER
        self.fesList = fesFinder(self.defaultCity ,size_hint = (1,0.95),pos_hint = {"top" : 0.95})
        for btn in self.fesList.layout.children:
            btn.bind(on_press = self.pop_up_fes_desc)

        self.add_widget(self.fesList)

        self.actChooseCity = Button(text = f'cur city is {self.defaultCity}', size_hint= (1,0.05), pos_hint = {'top':1})
        self.actChooseCity.bind(on_press = self.pop_up_city_layout)
        self.add_widget(self.actChooseCity)

        #FESDESCRIPTION
        self.fesDescLayout = FloatLayout(size_hint = (1,0.9),pos_hint = {'top':1})

        self.desc_label = ScrollableText(pos_hint = {'top': 0.9},size_hint= (1,0.9))
        self.fesDescLayout.add_widget(self.desc_label)

        self.exitButton2 = Button(text = "Back", size_hint = (0.4,0.05), pos_hint ={"top": 1})
        self.exitButton2.bind(on_press = self.back_to_fes_list2) 
        self.fesDescLayout.add_widget(self.exitButton2)  
    
        self.findDateinCalBtn =  Button(text = "", size_hint = (0.4,0.05), pos_hint ={"top": 0.95, "right" : 1})
        self.fesDescLayout.add_widget(self.findDateinCalBtn)
    
    def pop_up_fes_desc(self,instance:Button): 
        if self.isFesList:
            self.remove_widget(self.fesList)
            self.remove_widget(self.actChooseCity)
            self.add_widget(self.fesDescLayout)
            self.isFesList = False
        
        if self.isCityList:
            self.remove_widget(self.cityLayout)
            self.add_widget(self.fesDescLayout)
            self.isCityList =False
        
        curFes = instance.text[:instance.text.find('\n')]
        fes = self.fesList.subset[self.fesList.subset['Festival'] == curFes]['Festival'].iloc[0]
        fes_desc = self.fesList.subset[self.fesList.subset['Festival'] == curFes]['desc'].iloc[0]
        day =  self.fesList.subset[self.fesList.subset['Festival'] == curFes]['day'].iloc[0]
        month =  self.fesList.subset[self.fesList.subset['Festival'] == curFes]['month'].iloc[0]
        isLun =  self.fesList.subset[self.fesList.subset['Festival'] == curFes]['LunarorSolar'].iloc[0] == 0
        
        self.desc_label.label.text = f'{fes}\n\n{fes_desc}'
        self.findDateinCalBtn.text = f'Find {day}/{month} {"Lunar" if isLun else "Solar"}'
        


    def back_to_fes_list2(self,instance):
        self.desc_label.text = ''
        self.remove_widget(self.fesDescLayout)
        self.isFesList = True
        self.add_widget(self.fesList)
        self.add_widget(self.actChooseCity)        

    def pop_up_city_layout(self,instance:Button):
        self.remove_widget(self.fesList)
        self.remove_widget(self.actChooseCity)
        self.add_widget(self.cityLayout)
        self.isFesList = False
        self.isCityList = True
    
    def back_to_fes_list1(self,instance:Button):
        self.add_widget(self.fesList)
        self.add_widget(self.actChooseCity)
        self.remove_widget(self.cityLayout)
        self.isFesList = True
        self.isCityList = False

    def select_city(self,instance:Button):
        self.defaultCity = instance.text
        self.fesList.change_city(self.defaultCity)
        self.actChooseCity.text = f'cur city is {self.defaultCity}'
        
        for btn in self.fesList.layout.children:
            btn.bind(on_press = self.pop_up_fes_desc)
        self.add_widget(self.fesList)
        self.add_widget(self.actChooseCity)
        self.remove_widget(self.cityLayout) 
        self.isFesList = True
        self.isCityList = False   


class fesFinder(FloatLayout):
    def __init__(self, input_city,**kwargs):
        super(fesFinder,self).__init__(**kwargs)
        self.first = True
        self.change_city(input_city)
    
    def change_city(self,input_city):
        if not self.first:
            self.clean_up()
        else:
            self.first = False
 
        self.input_city = input_city
        self.subset = df[df["city"].isin([self.input_city,'A'])]

        self.layout = GridLayout(cols=1, spacing=10, size_hint_y = None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        lsChooser = ["Lunar Calendar","Solar Calendar"]
        for row in self.subset.itertuples(index=False):
            btn = Button(text=f"{row.Festival}\n{row.day}/{row.month} {lsChooser[row.LunarorSolar]}", 
                         size_hint_y=None, 
                         height=200
                        )
            self.layout.add_widget(btn)
        self.layout.add_widget(Button(text = "check",size_hint_y = None,height = 100))
        
        self.scroll = ScrollView(
            size_hint=(1, 1),
            pos_hint = {"top":1}
            )
        self.scroll.add_widget(self.layout)
        self.add_widget(self.scroll)
    
    def clean_up(self):
        self.remove_widget(self.scroll)
        del self.scroll        


class fesScrollScreen(App):
    def build(self):
        return mainFesLayout(size_hint=(1,0.9), pos_hint = {"top" : 1})

if __name__ == "__main__":
    fesScrollScreen().run()