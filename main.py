from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from calLayout import MainCalLayout
from fesScrollLayout import mainFesLayout
import myCalendar as myCal
import calendar as cal
import os
import pandas as pd
import datetime as dt

#file_path = os.path.join(os.path.dirname(__file__), 'FesCollection', 'FesData.xlsx')
dfMain = pd.read_excel("FesData.xlsx")

Window.size = (360, 640)
Window.clearcolor = (.7,.7,.7,1)

class mainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(mainLayout,self).__init__(**kwargs)
        '''
        Main app - Cal      -
                 - FesDesc  
                 - SwitchButton (swap cal and fesdesc)
        '''
        self.city = "HaNoi"
        self.isCal = True
        self.df = dfMain[dfMain['city'] == self.city]
        self.fesSection = mainFesLayout(size_hint=(1,0.9),pos_hint = {'top' : 1})
        for btn in self.fesSection.cityButtons.children:
            btn.bind(on_press = self.changeCityofCal)

        self.calSection = MainCalLayout()
        self.add_widget(self.calSection)
        self.calSection.showFesBtn.bind(on_press = self.OffCal)
        self.calSection.showFesBtn.bind(on_press = self.fesSection.pop_up_fes_desc)

        sectionBtns =  GridLayout(
            cols = 2,
            size_hint = (1,0.05),
            pos_hint = {"top": 0.05}
        )
        self.add_widget(sectionBtns)

        btn1 = Button(
            text = "CAL",
            background_color = (1,0,0,1)
        )
        btn1.bind(on_press = self.OnCal)
        sectionBtns.add_widget(btn1)

        btn2 = Button(
            text = "FES",
            background_color = (0,1,0,1)
        )
        btn2.bind(on_press = self.OffCal)
        sectionBtns.add_widget(btn2)

        self.fesSection.findDateinCalBtn.bind(on_press = self.OnCal)
        self.fesSection.findDateinCalBtn.bind(on_press = self.findDateInCal)
    
    #def pop_up_fes_desc(self,instance):
        #self.fesSection.pop_up_fes_desc(instance)

    def changeCityofCal(self,instance):
        self.city = instance.text
        self.calSection.changeCity(self.city)

    def findDateInCal(self, instance):
        text = instance.text
        lDate = text[5 : -6] #return Date dd/mm. last remove " solar" or " lunar"
        isLun = text[-5:] == "Lunar"
        if isLun:
            lDay, lMonth = int(lDate[:lDate.find('/')]), int(lDate[lDate.find('/') + 1:])
            year = self.calSection.year
            ly = myCal.YearStL(year,self.calSection.month,1)
            if ly < year and lMonth <= 2:
                ly += 1
            if myCal.has_nonleap_lunardate_passed(year,lMonth,lDay):
                year += 1
            dateOfNextInstance = myCal.nonLeapDateLtS(ly,lMonth,lDay) #return tuple (y,m,d)
            sDay, sMonth = dateOfNextInstance[2], dateOfNextInstance[1]
            self.calSection.changeYearMonth(year,sMonth)

            starting_date = cal.weekday(year,sMonth,1)
            redBtnID = 42 - (starting_date + sDay)
            self.calSection.datesinCalLayout.children[redBtnID].turnRed()
            self.calSection.datesinCalLayout.redButton = self.calSection.datesinCalLayout.children[redBtnID]
        else:
            sDay, sMonth = int(lDate[:lDate.find('/')]), int(lDate[lDate.find('/') + 1:])
            sYear = myCal.curYear()
            if dt.date(sYear,sMonth,sDay) < dt.date.today():
                sYear += 1
            self.calSection.changeYearMonth(sYear,sMonth)
            btnID = self.calSection.datesinCalLayout.findButton(sDay)
            self.calSection.datesinCalLayout.redButton = self.calSection.datesinCalLayout.children[btnID]
            self.calSection.datesinCalLayout.redButton.turnRed()

    def OnCal(self,instance):
        if self.isCal :
            return
        self.add_widget(self.calSection)
        self.remove_widget(self.fesSection)
        self.isCal = True
    
    def OffCal(self,instance):
        if not self.isCal:
            return
        self.add_widget(self.fesSection)
        self.remove_widget(self.calSection)
        self.isCal = False
    
        

class MainApp(App):
    def build(self):      
        return mainLayout(
            size_hint = (1,1)
        )


if __name__ == "__main__":
    MainApp().run()