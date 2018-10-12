import urllib.request
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def street_find(words):
    #find only the street name
    for word in words:
        if word.lower().find("street") != -1:
            return word
        else:
            pass

def road_find(words):
    #find only the road name
    for word in words:
        if word.lower().find("road") != -1:
            return word
        else:
            pass

def address_split(address):
    words = address.split(sep = ',')
    street = street_find(words)
    road = road_find(words)
    if street == None:
        street = road

    if street == None:
        street = ""

    full_address = ''
    for word in words[:-2]:
        full_address += word
                

    location = [street.strip(), words[-2].strip(), words[-1].strip(), full_address]
    return location


def title(soup):
    people =  []
    ranking = []
    nrc = []
    for names in soup.find_all('td', attrs={'class':'views-field views-field-title'}):
        people.append(names.get_text(strip=True))
    for names in soup.find_all('td', attrs={'class':'views-field views-field-field-person-type'}):
        ranking.append(names.get_text(strip=True))
    for names in soup.find_all('td', attrs={'class':'views-field views-field-field-nrc-complete'}):
        nrc.append(names.get_text(strip=True))
    return [people, ranking, nrc]


def type_business(soup):
    business = soup.find('li', attrs={'class':'field-item even'})
    if business == None:
        return None
    else:
        return soup.find('li', attrs={'class':'field-item even'}).get_text(strip=True)


def webpage(start, stop):
    #enter the number of webpages to be scraped from start to stop
    for page in range(start, stop):
        quote_page = 'https://dica.gov.mm/en/company-search?company=I&page={}'.format(page)
        print('\nPage: {}'.format(page+1))
        # query the website and return the html to the variable ‘page’
        page = urllib.request.urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        # parse the html using beautiful soup and store in variable `soup`
        get_company_names(soup)

def get_company_names(soup):
    
        for company in soup.find_all('td', {'class': 'views-field views-field-field-company-name-myanmar'}):
            url = []
            url.append(company.a['href'])
            get_info(url)

def get_info(url):
    for company in url:
        page = urllib.request.urlopen(company)
        soup = BeautifulSoup(page, 'html.parser')
        data = []
        for i in soup.find_all('div', attrs={'class' : 'field-item even'}):
            data.append(i.get_text(strip=True))
        titles = title(soup)
        people = titles[0]
        ranking = titles[1]
        nrc = titles[2]
        name = data[0]
        mm = data[1]
        num = data[2]
        registry_date = data[3]
        expiry_date = data[4]
        address = address_split(data[5])
        business = type_business(soup)
        print(name)
        
        error = "Can't encode MM font."
        if len(people)==0:
            people = ranking = nrc = ['']


        with open('yes.csv', 'a', newline = '') as csv_file:
        #input data into csv file
         writer = csv.writer(csv_file)
         try :
             writer.writerow([name, num, registry_date, expiry_date, business, address[0],address[1], address[2],people[0],ranking[0],nrc[0], datetime.now(), address[3], company])         
         except:
             writer.writerow([name, num, registry_date, expiry_date, business, address[0],address[1], address[2],people[0],ranking[0],nrc[0], datetime.now(), error, company])  
         else:
             
             if len(people)>1:
                 for i in range(len(people)-1):
                     writer.writerow([None, None, None, None, None, None,None,None,people[i+1],ranking[i+1],nrc[i+1]])
             else:
                 pass


print("Webpages to scrape. Counts from 0 \n")
start = int(input("Start: "))
stop = int(input("\nStop: "))

webpage(start, stop)
