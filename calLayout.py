from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import myCalendar as myCal
import calendar as cal
import os
import pandas as pd


#file_path = os.path.join(os.path.dirname(__file__), 'FesCollection', 'FesData.xlsx')
dfMain = pd.read_excel("FesData.xlsx")
df = dfMain[dfMain['city'] =='A']
#lunDf = dfMain[dfMain['city'] =='TPHCM']

fesinMonthLookUp = []
for i in range(12):
    fesinMonthLookUp.append([])
for row in df.itertuples(index=False):
    fesinMonthLookUp[row.month-1].append(row)

# Optional for desktop preview
Window.size = (360, 640)
Window.clearcolor = (.7,.7,.7,1)

class SquareButton(Button):
    """A custom Button that always stays square."""
    def on_size(self, *args):
        # make height equal to width to maintain square shape
        self.height = self.width 
    def turnRed(self):
        self.background_color = (1,0,0,1)
    def turnGreen(self):
        self.background_color = (0,1,0,1)
    def turnYellow(self):
        self.background_color = (1,1,0,1)
    def turnNormal(self):
        self.background_color = (0.2,0.6,0.9,1)
    def turnGrey(self):
        self.background_color = (0.85,0.85,0.85,1)

class MainCalLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(MainCalLayout,self).__init__(**kwargs)
        self.year = myCal.curYear()
        self.month = myCal.curMonth()
        self.size_hint=(1,0.95)
        self.pos_hint = {"top":1}
        self.rows = 4
        self.selectedFesBtn = 0

        self.MonthLabel = Label(
            text = f"{self.year} - {myCal.monthInWord(self.month)}",
            size_hint = (1,0.1),
            pos_hint = {"top":0.99},
            color = (0,0,0,1),
            bold = True,
            font_size='40sp'
        )
        self.add_widget(self.MonthLabel)
        
        self.adjacentMonth = GridLayout(
            cols = 2,
            spacing = 5,
            padding = 10,
            size_hint = (1, 0.1),
            pos_hint = {"top":0.9}
        )
        self.add_widget(self.adjacentMonth)
        self.prevButton = Button(                
            text="<",
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),                
            font_size=14,
            bold=True
        )
        self.prevButton.bind(on_press = self.showPrevMonth)
        self.adjacentMonth.add_widget(self.prevButton)

        self.nextButton = Button(                
            text=">",
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=14,
            bold=True
        )
        self.nextButton.bind(on_press = self.showNextMonth)
        self.adjacentMonth.add_widget(self.nextButton)

        self.datesinCalLayout = calGrid(
            city = "HaNoi",
            year = 2025,
            month = 10,
            pos_hint = {"top":0.8}
        )
        self.add_widget(self.datesinCalLayout)
        self.bindGreenBtn()
        self.bindYellowBtn()

        self.yearFinder = GridLayout(
            cols = 2,
            spacing = 5,
            padding = 10,
            size_hint = (1, 0.1),
            pos_hint = {"top":0.1}
        )
        self.add_widget(self.yearFinder)
        
        self.yearSearchBar = TextInput(multiline = True)
        self.yearFinder.add_widget(self.yearSearchBar)
        
        self.submitYearBtn = Button(
            text="Find year",
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            font_size=14,
            bold=True            
        )
        self.submitYearBtn.bind(on_press = self.submitYear)
        self.yearFinder.add_widget(self.submitYearBtn)

        self.showFesBtn = Button(
            text = '',
            font_size = 16,
            size_hint = (1,0.1),
            pos_hint = {'top' : 0.2}
        )


    def changeCity(self,city):
        self.unbindGreenBtn()
        self.unbindYellowBtn()
        self.datesinCalLayout.changeCity(city)

        self.bindGreenBtn()
        self.bindYellowBtn()

    def bindYellowBtn(self):
        for day in self.datesinCalLayout.yellowBtns:
            if day[1] in self.datesinCalLayout.greenBtns:
                continue
            btnID = self.datesinCalLayout.findButton(day[1])  
            self.datesinCalLayout.children[btnID].bind(on_press = self.popUpLunFesName)

    def unbindYellowBtn(self):   
        for day in self.datesinCalLayout.yellowBtns:
            if day[1] in self.datesinCalLayout.greenBtns:
                continue            
            btnID = self.datesinCalLayout.findButton(day[1])  
            self.datesinCalLayout.children[btnID].unbind(on_press = self.popUpLunFesName)  
      
    def popUpLunFesName(self,instance):
        day = int(instance.text[:instance.text.find('\n')])
        if self.selectedFesBtn == day:
            return
        for fes in self.datesinCalLayout.yellowBtns:
            if day != fes[1]:
                continue
            idx = instance.text.find('\n')
            self.showFesBtn.text = f"{fes[0]}\n{instance.text[idx+2:]} Lunar"
        if not self.selectedFesBtn:
            self.add_widget(self.showFesBtn)
        self.selectedFesBtn = day

    def bindGreenBtn(self):
        starting_date = cal.weekday(self.year,self.month,1) 
        for day in self.datesinCalLayout.greenBtns:
            btnID = 42 - (day + starting_date)
            self.datesinCalLayout.children[btnID].bind(on_press = self.popUpFesName)
    
    def unbindGreenBtn(self):
        starting_date = cal.weekday(self.year,self.month,1) 
        for day in self.datesinCalLayout.greenBtns:
            btnID = 42 - (day + starting_date)
            self.datesinCalLayout.children[btnID].unbind(on_press = self.popUpFesName)    

    def popUpFesName(self,instance):
        day = int(instance.text[:instance.text.find('\n')])
        if self.selectedFesBtn == day:
            return
        for fes in fesinMonthLookUp[self.month -1]:
            if fes.day != day:
                continue
            self.showFesBtn.text = f'{fes.Festival}\n{fes.day}/{fes.month} {"Solar"}'
            break
        if not self.selectedFesBtn:
            self.add_widget(self.showFesBtn)
        self.selectedFesBtn = day

    def changeYearMonth(self,year,month):
        self.selectedFesBtn = 0 #pos
        self.remove_widget(self.showFesBtn)
        self.unbindYellowBtn()
        self.unbindGreenBtn()

        self.year, self.month = year,month
        self.datesinCalLayout.changeMonth(year,month)
        self.bindYellowBtn()
        self.bindGreenBtn()
        self.MonthLabel.text = f"{self.year} - {myCal.monthInWord(self.month)}"

    def submitYear(self,instance):
        yearInput = self.yearSearchBar.text
        self.yearSearchBar.text = ""
        if  len(yearInput) >6 or len(yearInput) == 0:
            return 
        for char in yearInput:
            if char not in "0123456789":
                return
        self.yearSearchBar.text = ""
        if int(yearInput) > 9999:
            self.yearSearchBar.text = "idk the future bruv"
        self.year = min(int(yearInput), 9999)
        self.changeYearMonth(self.year,self.month)

    def showPrevMonth(self,instance):
        self.year = self.year - 1 if self.month == 1 else self.year
        self.month = self.month - 1 if self.month > 1 else 12
        self.changeYearMonth(self.year,self.month)

    def showNextMonth(self,instance):
        self.year = self.year + 1 if self.month == 12 else self.year
        self.month = self.month + 1 if self.month < 12 else 1
        self.changeYearMonth(self.year,self.month)
    
class calGrid(GridLayout):
    def __init__(self,city,year, month,**kwargs):
        super(calGrid,self).__init__(**kwargs)
        self.year = year
        self.month = month
        self.city = city
        self.dF = dfMain[dfMain['city'].isin(['A', self.city])]
        self.lunDf = self.dF[self.dF['LunarorSolar'] == 0]
        self.solDf = self.dF[self.dF['LunarorSolar'] == 1]

        self.cols = 7
        self.spacing = 5
        self.padding = 10
        self.size_hint= (1,1.3)
        self.redButton = None
        self.greenBtns = []
        self.yellowBtns = []
        num_buttons = 42
        # evenly divide horizontal space among 7 columns
        button_width = 1 / 7 - 0.02
          
        for day in ("Mon","Tue","Wed","Thu","Fri","Sat","Sun"):
            self.add_widget(SquareButton(text = day, size_hint = (button_width, None)))

        starting_date = cal.weekday(year,month,1) 
        len_month = myCal.monthLen(year,month) #How many days of a month

        for i in range(1, num_buttons + 1):
            btn = SquareButton(
                text="",
                size_hint=(button_width, None),  # height handled in on_size
                background_color=(0.2, 0.6, 0.9, 1),
                color=(1, 1, 1, 1),
                font_size=14,
                bold=True
            )
            if starting_date < i <= len_month + starting_date:
                curDay = i- starting_date
                lunarDate = myCal.dayMonthStL(self.year,self.month,curDay)
                btn.text = f"{i- starting_date}\n {lunarDate}"
                if i == myCal.curDay() + starting_date:
                    btn.turnRed()
                    self.redButton = btn
                btn.bind(on_press=self.press)
                    
            else:
                btn.turnGrey()
            self.add_widget(btn)
        self.checkLunFesInMonth()
        self.checkSolFesInMonth()
    
    def findButton(self, day):
        starting_date = cal.weekday(self.year,self.month,1) 
        btnID = 42 - (day + starting_date)
        return btnID
    
    def checkSolFesInMonth(self):
        curMonthSolFes = self.solDf[self.solDf['month'] == self.month]
        for fes in curMonthSolFes.itertuples(index=False):
            day = fes.day
            btnID = self.findButton(day)
            self.children[btnID].turnGreen()
            self.greenBtns.append(day)
    
    def checkLunFesInMonth(self):
        if myCal.isInLeapMonth(self.year,self.month,myCal.monthLen(self.year,self.month)) and myCal.isInLeapMonth(self.year,self.month,1):
            return
        
        if myCal.isInLeapMonth(self.year,self.month,1):
            lDay,lMonth = 1 ,myCal.MonthStL(self.year,self.month,1) + 1
        else:
            lDay,lMonth,ly = myCal.DayStL(self.year,self.month,1) ,myCal.MonthStL(self.year,self.month,1),myCal.YearStL(self.year,self.month,1)
        if myCal.isInLeapMonth(self.year,self.month,myCal.monthLen(self.year,self.month)):
            rDay,rMonth = myCal.DayStL(self.year,self.month,myCal.monthLen(self.year,self.month)) ,myCal.MonthStL(self.year,self.month,myCal.monthLen(self.year,self.month)) 
            rDay = myCal.DayStL(self.year,self.month,myCal.monthLen(self.year,self.month)- rDay)
        else:
            rDay,rMonth = myCal.DayStL(self.year,self.month,myCal.monthLen(self.year,self.month)) ,myCal.MonthStL(self.year,self.month,myCal.monthLen(self.year,self.month))
        
        if lMonth <= rMonth:
            lunFesList = self.lunDf[self.lunDf['month'] <= rMonth]
            lunFesList = lunFesList[lunFesList['month'] >= lMonth]    
        else:
            lunFesList = self.lunDf[self.lunDf['month'].isin([lMonth,rMonth])]

        for row in lunFesList.itertuples(index=False):
            if row.LunarorSolar == 1 or (row.month == lMonth and row.day < lDay) or (row.month == rMonth and row.day > rDay):
                continue
            fesYear = self.year
            if ly < self.year and row.month > 1:
                fesYear -= 1
            solDay = myCal.nonLeapDateLtS(fesYear,row.month,row.day)[2]
            btnID = self.findButton(solDay)
            self.children[btnID].turnYellow()
            #print(f'{row.day}/{row.month}  {solDay}')
            self.yellowBtns.append((row.Festival,solDay))

    def changeMonth(self, year, month):
        self.year = year
        self.month = month
        self.redButton = None
        del self.greenBtns
        del self.yellowBtns
        self.greenBtns = []
        self.yellowBtns = []

        starting_date = cal.weekday(year,month,1) 
        len_month = myCal.monthLen(year,month)


        for i in range(41, -1, -1):
            btn, btnId = self.children[i], 42 - i

            if starting_date < btnId <= len_month + starting_date:
                btn.turnNormal()
                curDay = btnId - starting_date
                lunarDate = myCal.dayMonthStL(self.year,self.month,curDay)
                btn.text = f"{btnId - starting_date}\n {lunarDate}"
                btn.bind(on_press = self.press)
            else:
                btn.turnGrey()
                btn.text = ""
                btn.unbind(on_press= self.press)
        self.checkLunFesInMonth()
        self.checkSolFesInMonth()

    def changeCity(self,city):
        self.city = city
        self.dF = dfMain[dfMain['city'].isin(['A', self.city])]
        self.lunDf = self.dF[self.dF['LunarorSolar'] == 0]
        self.solDf = self.dF[self.dF['LunarorSolar'] == 1]
        self.changeMonth(self.year, self.month)

    def press(self, instance:SquareButton):
        if self.redButton and int(self.redButton.text[:self.redButton.text.find('\n')]) in self.greenBtns:
            self.redButton.turnGreen()
        elif self.redButton:
            isYellow = False   
            for day in self.yellowBtns:
                if day[1] ==  int(self.redButton.text[:self.redButton.text.find('\n')]):
                    self.redButton.turnYellow()
                    isYellow = True
            if not isYellow:
                self.redButton.turnNormal()
        
        self.redButton = instance
        self.redButton.turnRed()
    


class CalFes(App):
    def build(self):
        MainApp = FloatLayout()
        return MainCalLayout()      


if __name__ == '__main__':
    CalFes().run()