
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import mechanize
import re
import time
from tkinter import *
import tkinter.messagebox as msg
import datetime

print('SIX Automated Presence - Gondok')

# Set date data
date = datetime.datetime.now()

if (date.month<=5): # => Sem. Genap 
    academicYear = str(date.year-1)
    academicSemester = '2' 
else : # => Sem. Ganjil
    academicYear = str(date.year) 
    academicSemester = '1'

# Open "Jadwal Mahasiswa", but go through login first

user_data_arr = []

with open ('user-data.txt') as user_data_txt:
    next(user_data_txt)
    for line in user_data_txt:
        user_data_arr.append(line.replace('\n','').split(' = ')[1])

NIM = user_data_arr[2]

user_URL = 'app/mahasiswa:'+NIM+'%2B'+academicYear+'-'+academicSemester+'/kelas/pertemuan/jadwal/mahasiswa'

alamat = r'https://akademik.itb.ac.id/app/mahasiswa:'+NIM+'+'+academicYear+'-'+academicSemester+'/kelas/pertemuan/jadwal/mahasiswa'
req = Request(alamat, headers={'User-Agent': 'Mozilla/5.0'})

br = mechanize.Browser()
br.set_handle_robots(False)
br.open(alamat)

# Web will redirect to login page. Finding link to sign in with INA:
target_login_INA = r'/login/INA?returnTo=https://akademik.itb.ac.id/'+user_URL

for link in br.links():
    if link.url == target_login_INA:
        break

br.follow_link(link)

# We are now at the Login page. Selecting form and submitting w/ credentials :

print('Entering login info...')

credentials = {
    'username' : user_data_arr[0],
    'password' : user_data_arr[1]
}

br.select_form(id='fm1')



br.form['username'] = credentials['username']
br.form['password'] = credentials['password']

res = br.submit()

# Redirecting to original (Jadwal) link

# Storing username
html = BeautifulSoup(br.response().read(),'html.parser')

cols = html.findAll('a',{'class':'dropdown-toggle'})
username = cols[-1].text.replace('\n','').replace(' ','')
username = re.sub(r"(?<=\w)([A-Z])", r" \1", username)

print('Successfully logged in. \nReturning to Schedule Menu...')

target_redirect_matkul = '/locale/id?returnTo=/'+user_URL

br.follow_link(link)

# Now at Jadwal Mhs page

# Store all possible presence links in linkAbsensi
linkAbsensi = []
for link in br.links():
    if link.url == '#' and link.attrs[2][0]=='data-kuliah':
        linkAbsensi.append(link)

print('Now crawling links to find available attendances',end='')

# Each link will be opened and checked for forms. When one with forms appears, check its value and submit it
for i in linkAbsensi:
    print('.',end='')
    # print('\n')
    br.open(r'https://akademik.itb.ac.id'+i.attrs[3][1])
    test = i.attrs[2][1]
    # if (len(br.forms)!=0):
    #     Todo: Find button, check value, submit, retrieve subject and return to user
print('\nSuccessfully marked '+username+' as present in '+test+"!")

