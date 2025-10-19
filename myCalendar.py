import calendar as cal
import datetime as dt
import LunarSolar as ls

def findMonthCal(year: int, month: int):
    return cal.month(year,month)

def findDateinCal(year: int, month: int, day: int):
    day = str(day)
    monthCalendar = str(cal.month(year,month))
    suId = monthCalendar.find("Su")
    dayId = monthCalendar[suId:].find(str(day)) + suId
    resCalendar = monthCalendar[:dayId-1] + "(" + str(day) + ")" + monthCalendar[dayId+3:]
    return resCalendar

def findDatePos(year:int, month:int):
    day = str(1)
    monthCalendar = str(cal.month(year,month))    
    suId = monthCalendar.find("Su")
    dayId = monthCalendar[suId+2:].find(str(day)) 
    return (dayId-2)//3   

def findCurMonthCal():
    tday = dt.date.today()
    year = tday.year
    month = tday.month
    day = tday.day
    return findDateinCal(year,month,day)

def monthLen(year:int,month:int):
    return cal.monthrange(year,month)[1]

def curMonth():
    return dt.date.today().month

def curYear():
    return dt.date.today().year

def curDay():
    return dt.date.today().day

def monthInWord(month):
    return ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"][month-1]

def SolartoLunar(year, month, day):
    resString = ls.solar_to_lunar_string(day, month, year, 7 )
    resString = str(resString)
    return resString[resString.find("-")+2 : resString.find(" AL")]

def dayMonthStL(year,month,day):
    i = 0
    a=0
    lunarDate = SolartoLunar(year,month,day)
    while i<2:
        if lunarDate[a] == "/":
            i+=1
        a+=1
    return SolartoLunar(year,month,day)[:a-1]

def YearStL(year,month,day):
    i = 0
    a=0
    lunarDate = SolartoLunar(year,month,day)
    while i<2:
        if lunarDate[a] == "/":
            i+=1
        a+=1
    return int(SolartoLunar(year,month,day)[a:]) 

def DayStL(year,month,day):
    date = dayMonthStL(year,month,day)
    return int(date[:date.find('/')])

def MonthStL(year,month,day):
    date = dayMonthStL(year,month,day)
    return int(date[date.find('/') + 1:])

def isInLeapMonth(year,month,day):
    lunD, lunM = DayStL(year,month,day), MonthStL(year,month,day)
    if lunD > 1:
        return (lunM == MonthStL(year,month,day-30))
    else:
        return (lunM == MonthStL(year,month,day-1))

def nonLeapMonthLtS(lunyear,lunmonth,lunday):
    #sliding window to find the non-leap month in the solar calendar
    year = lunyear
    if not isInLeapMonth(year,12,31) and lunmonth > MonthStL(year,12,31) or (lunmonth == MonthStL(year,12,31) and lunday > DayStL(year,12,31)):
        year += 1
    elif isInLeapMonth(year,12,31):
        lunD = DayStL(year,12,31)
        SolD = 31 - lunD
        year += 1 if lunmonth > MonthStL(year,12,SolD) or (lunmonth == MonthStL(year,12,SolD) and lunday > DayStL(year,12,SolD)) else 0
    for month in range(2,13):
        ly, lm, ld = YearStL(year,month,1), MonthStL(year,month,1), DayStL(year,month,1)
        if ly > lunyear or (ly == lunyear and lm >lunmonth) or (ly == lunyear and lm == lunmonth and ld > lunday):
            return (year,month-1)
        
        #print(f"{month}: {ly}/{lm}/{ld}")
    #print(f"{lunyear}/{lunmonth}/{lunday}\n {year}")
    return(year,12)

def nonLeapDateLtS(lunyear,lunmonth,lunday):
    solYearMonth = nonLeapMonthLtS(lunyear,lunmonth,lunday)
    solYear, solMonth = solYearMonth[0], solYearMonth[1]
    lastDayofSolMonth = monthLen(solYear,solMonth)
    ly, lm, ld = YearStL(solYear,solMonth,1), MonthStL(solYear,solMonth,1), DayStL(solYear,solMonth,1)
    ry, rm, rd = YearStL(solYear,solMonth,lastDayofSolMonth), MonthStL(solYear,solMonth,lastDayofSolMonth), DayStL(solYear,solMonth,lastDayofSolMonth)
    if ly == lunyear and lm == lunmonth:
        solDay = 1 + (lunday - ld)
    elif ry == lunyear and rm == lunmonth:
        solDay = lastDayofSolMonth - (rd -lunday)
    else:
        solDay = lastDayofSolMonth - rd 
        rd = DayStL(solYear,solMonth,solDay)
        solDay -= rd - lunday + 1
    return (int(solYear),int(solMonth),int(solDay))

def nonLeapDateLtStoStr(lunyear,lunmonth,lunday):
    date = nonLeapDateLtS(lunyear,lunmonth,lunday)
    return f'{date[2]}/{date[1]}/{date[0]}'

def has_nonleap_lunardate_passed(lunYear,lunmonth,lunday):
    # Expecting input format: dd/mm/yyyy
    solDate = nonLeapDateLtS(lunYear,lunmonth,lunday)
    y,m,d = solDate[0],solDate[1],solDate[2]
    input_date = dt.date(y,m,d)
    today = dt.date.today()
    return input_date < today
    

if __name__ == "__main__" :
    print(f'\n{nonLeapDateLtS(2026,1,13)[1]}')