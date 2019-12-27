from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
from tkinter import filedialog 
import datetime 
import time
import os
import urllib
from urllib.request import urlopen 
from bs4 import BeautifulSoup
import certifi
import lxml

refPage = None

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def check(url):
    #infer desktop
    desktopPath = os.path.expanduser("~/Desktop/")
    from datetime import date
    today = str(date.today())
    intLinks = [] #internal (in-site) links list
    extLinks = [] #external links list
    hdr = {'User-Agent': 'Mozilla/5.0'}
    log = [] #string to write to log
    
    def checkStatus(linkList, refPage=None):#if none, link is on main page, https://openscience.ubc.ca
        for link in linkList:      
            if "http" not in link:
                link = "http://"+ link
            try:
                req=urllib.request.Request(link,headers=hdr)
                resp=urllib.request.urlopen(req, cafile=certifi.where())
                if resp.status in [400,404,403,408,409,501,502,503]: #if page not available
                    log.append("PROBLEM       --> " + resp.status+"-"+resp.reason+"-->"+link)
                    if refPage:
                        log.append("                --> Referring page: " + refPage)   
                    else:
                        log.append("Problem link is on home page, " + url + ".")               
                else: log.append("no problem in --> "+ link)
               
            except Exception as e:
                log.append("PROBLEM       --> "  + link + ": " + str(e))
                if refPage:
                    log.append("                  Referring page: " + refPage)
                else:
                    log.append("                  Referring page: " + url) 
                pass
        
    def gatherLinks(currURL,refPage = None):
        try:
            req = urllib.request.Request(currURL,headers=hdr)
            resp=urlopen(req, cafile=certifi.where())
            bs = BeautifulSoup(resp, "lxml")
            links = bs.findAll('a', href=True)
            for l in links:
                if l.text == None or len(l.text) == 0: #if link text
                    continue
                else: 
                    try:
                        txt=l['href']
                        if txt == "http://www.ubc.ca": #avoid accumulating duplicate links to ubc site
                            continue
                        if len(txt)<2 or txt[0] =="#" or "../" in txt:
                            continue     
                        if txt[0]=="/": #if relative link
                            txt = url + txt
                        if txt[-1:]=="/": #if url ends in "/", clip slash
                            txt = txt[:-1]
                        if "openscience.ubc.ca/" in txt and txt not in intLinks:
                            intLinks.append(txt)                  
                            gatherLinks(txt, currURL)
                        #separate out in duplicates, internal links, and mailto links
                        elif txt not in extLinks and "openscience.ubc.ca" not in txt and "mailto" not in txt:
                            extLinks.append(txt)         
                    except Exception as e:
                        #cite exception in log
                        log.append("PROBLEM       --> " + str(e) + ": " + txt)
                        if refPage:
                            log.append("                  Referring page: " + refPage)
                        else:
                            log.append("                  Referring page: " + url) 
                        pass
        except Exception as e:
            #cite exception in log
            log.append("PROBLEM       --> " + str(e) + ": " + url)
            if refPage:
                log.append("                  Referring page: " + refPage)
            else:
                log.append("                  Referring page: " + url) 
     
    gatherLinks(url)
    checkStatus(extLinks)
    log.sort()
    fn = 'LinkCheck_' + today + "_Log.txt"
    dest = os.path.join(desktopPath, fn)
    with open(dest, 'w') as filehandle:
        filehandle.write("Link Check of " + url + ": " + today +"\n") #add date
        filehandle.write("----------------------------------------------------\n")
        for line in log:
            filehandle.write('%s\n' % line)
    msg = "All links have been checked, and the log\n" + fn + " has been\nwritten to your Desktop."
    messagebox.showinfo(title = 'Check Complete!', message = msg)       

class LinkChecker:
    def submit(self):
        link = self.url.get().strip()  
        if link == "":
            messagebox.showinfo("**Please enter the site URL.              ")        
        if link !="":
            check(link)
    
 
    def __init__(self, master):
        master.title('Link Checker')
        #master.resizable(False, False)
        master.configure(background = '#ffffff')
        master.config(height = 900, width = 600)      
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#ffffff')
        self.style.configure('TButton', background = 'white', bg = 'black', foreground='black')
        self.style.configure('TLabel', font = ('Arial', 11),background='#ffffff', foreground = '#000000')#, background = '#e1d8b9', font = ('Arial', 11))
        self.style.configure('Header.TLabel', font = ('Arial', 16, 'bold'), foreground='black')      
        
        self.folder=''
        self.frame_header = ttk.Frame(master, relief="sunken")
        self.frame_header.pack(fill=BOTH, expand=1)
        self.frame_header.config(width=600,height=900) 
     
        self.logo = PhotoImage(file = resource_path('brokenChain.gif'))
        ttk.Label(self.frame_header, image = self.logo).grid(row = 0, column = 0,pady=(5,5), padx=(40,0),sticky='ne')
        ttk.Label(self.frame_header, text = "Link Checker", style='Header.TLabel').grid(row = 0, column = 1,pady=(5,10), padx=(32,0),sticky='nw')
        ttk.Label(self.frame_header, text = "Enter the URL to check, and click the 'Check Links'\nbutton when you're ready to start! After the check is\ncomplete, a pop-up will let you know that a log has been\nsaved to your Desktop.").grid(row = 0, column = 1,pady=(40,10), padx=(33,30),sticky='ne')
        self.frame_content = ttk.Frame(master, relief="sunken")
        self.frame_content.pack(fill=BOTH, expand=1)
        ttk.Label(self.frame_content, text='Home Page URL of Website:').grid(row = 2, column = 0, padx = (50,0), pady=(10,0), sticky = 'nw')
        self.url = ttk.Entry(self.frame_content, width = 40)
        #add default url to check
        self.url.insert(END, 'https://openscience.ubc.ca')
        self.url.grid(row = 3, column = 0, padx = (50,0), pady=(20,15), sticky = 'nw')
   
        self.savePath = os.path.expanduser('~') + '\\Desktop\\'
        
        ttk.Button(self.frame_content, text = 'Check Links!',
                   command = self.submit).grid(row = 3, column = 1, padx=65, pady = (13,15), sticky = 'se')
                
def main():            
    root = Tk()
    linkchecker = LinkChecker(root)
    root.mainloop()
    
if __name__ == "__main__": main()