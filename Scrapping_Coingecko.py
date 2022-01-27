##import required Modules
import requests
from bs4 import BeautifulSoup
import openpyxl
import datetime

## first page of Coingecko
url = f'https://www.coingecko.com/?locale=en&page=1'

##open a excelfile to save the results 
excel = openpyxl.Workbook()
sheet = excel.active 
sheet.title='Crypto_coins' 
print(excel.sheetnames)
##Adding headers to the sheet
sheet.append(['Coin_rank','Coin_name','Coin_symbol','Price in US dollars','Market_Capital in US dollars','24_hrs_trading_volume','24_hrs_change_in%'])

##function to get next page of the website     
def getnextpage(s):
  
    pages = s.find('ul', class_ ="pagination")
    if not pages.find('li', class_ ="page-item next disabled"):
        url = 'https://www.coingecko.com/' + str(pages.find('li', class_ = "page-item next").find('a')['href'])
        return url
    else:
        ## return null , if its the lastpage
        return

##function to get coin data from a webpage 
def getdata(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    
    table_content = soup.find('div', class_ ="coingecko-table").find('tbody').find_all('tr')
   
    for table in table_content:
        try:
            coin_rank = int(table.find('td', class_= "table-number").get_text(strip=True).replace(",",""))
        except:
            coin_rank = "Rank_Unknown"
        coin_name = table.find('a', class_ ="tw-hidden").get_text(strip=True)
       
        coin_symbol = table.find('a', class_= "d-lg-none").get_text(strip=True)
      
       
        try:       
            change24hrs = float(table.find('td', class_='td-change24h').get_text(strip=True).replace("%",""))
        except:
            change24hrs = "unknown"
        
        a = table.find_all('span', class_ ="no-wrap")
        try:
                price = float(a[0].get_text(strip=True).replace("$","").replace(",",""))
        except: 
                price = "price unknown"
        try:
                trading_volume=a[1].get_text(strip=True)
        except:
                trading_volume = "unknown"
        try:

                market_cap=float(a[2].get_text(strip=True).replace("$","").replace(",",""))

        except:

            market_cap="unknown"
        
        sheet.append([coin_rank,coin_name,coin_symbol,price,market_cap,trading_volume,change24hrs])

    return(soup)

### While Loops exectes till it reached the last page of the website
while True:
  a=getdata(url)
  url = getnextpage(a)
  if not url:
      break; 
      
##Saving the excel file   
excel.save('cryto.xlsx')
      
 
    
    
    
