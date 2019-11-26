from bs4 import BeautifulSoup  #za web scrapping
import requests                # get i post na web str
import json                    # za json format
import re
import pprint

vremena = ['prez', 'prid t', 'aor', 'imperf', 'imp', 'prid r', 'pril s', 'pril p']

Skracenice = {'N':'Nominativ', 'D':'Dativ', 'G': 'Genitiv', 'A':'Akuzativ', 'V':'Vokativ', 'L':'Lokativ', 'I':'Instrumental',
              'odr' : 'određeni', 'imp':'imperativ', 'imperf':'imperfekt', 'prid r': 'glagolski pridjev radni',
              'prid t' : 'glagolski pridjev trpni', 'aor' : 'aorist', 'pril s' : 'glagolski prilog sadašnji',
              '3. l. mn' : 'treće lice množine', 'prez' : 'prezent', 'pril p' : 'glagolski prilog prosli', 'mn' : 'mnozina'}

NextChar = { 'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e'}

PODRUCJE = {"PREN": "preneseno značenje", "POM" : "pomorstvo", "VOJN" : "vojna znanost", 
            "RAZG" : "razgovor" ,"RUD" : "rudarstvo", "KEM" : "kemija", "FIZ" : "fizika",
            "POL" : "politika", "GOSP" : "gospodarstvo", "MED" : "medicina", "PROŠ" : "prošlost",
            "POGR" : "pogrdno", "TEHN" : "tehnologija", "PSIH" : "psihologija", "PAT" : "patologija",
            "GEOL" : "geologija", "ZOOL" : "zoologija", "UM" : "umanjenica", "UV" : "uvečanica",
            "LIK" : "likovni", "POLJ": "poljoprivreda", "GRAD": "građevina", "FIL" : "Filozofija",
            "LING" : "lingvistika", "GLAZB" : "glazba", "GLAZ" : "glazba", "KNJI" : "knjizevnost", "POV" : "povijest",
            "MET" : "meterologija", "KULIN" : "kulinarstvo", "FON" : "fonetika", "ARHIT" : "arhitektura",
            "GEOGR" : "geografija", "ŠP" : "sport", "BOT": "botanika", "BIOL":"biologija", "ETNOL":"etnologija",
            "RIB" : "ribarstvo", "REG" : "regionalno", "KINOL" : "kinologija", "INF" : "informatika", "TISK": "tiskarstvo",
            "ANAT" : "anatomija", "ZAST" : "zastarjelica", "GRAM" : "gramatika", "GEO" : "geologija", "UMJ" : "umjetnost",
            "MIN" : "mineralogija", "ŽARG" :"žargon", "KNJIŽ" : "književnost", "PRE" : "pregovori", "FARM" : "farmacija",
            "EL" : "elektortehnika", "ASTRO" : "astrologija", "PUBL" : "publikacija", "MU" : "marketing", "BANK" : "bankarstvo",
            "ETN" : "etnologija", "METON" : "metonimija"}

def mojPrintPod(rj,space='\t\t'):
    if '-' in rj:
        print(space+'-: '+rj['-'])
    if 'područja' in rj:
        print(space+"Područja: "+str(rj['područja']))
    if 'primjer' in rj:
        print(space+'Primjer: '+str(rj['primjer']))
    if 'sinonimi' in rj:
        print(space+'Sinonimi: '+str(rj['sinonimi']))
        
    print('')
        
    return

def mojPrintDef(rj,space='\t'):
    if '-' in rj:
        print(space+'-: '+rj['-'])
    else:
        print(space+'-: ')
    if 'područja' in rj:
        print(space+"Područja: "+str(rj['područja']))
    if 'podjela' in rj:
        print(space+"Podjela: ")
        for p in rj['podjela']:
            mojPrintPod(p)
    if 'primjer' in rj:
        print(space+'Primjer: '+str(rj['primjer']))
    if 'sinonimi' in rj:
        print(space+'Sinonimi: '+str(rj['sinonimi']))
    if 'special' in rj:
        print(space+'Specijal: '+rj['special'])
    print('')
        
    return

def printRoot(rj,space=''):
    print('')
    if 'Korijen' in rj:
        print('Korijen: '+rj['Korijen'])
    if 'ekvivalenta' in rj:
        print('Ekvival: '+rj['ekvivalenta'])
    if 'nastavak' in rj:
        print('nastavak: '+rj['nastavak'])
    if 'izgovor' in rj:
        print('Izgovor: '+str(rj['izgovor']))
    if 'vrstaRijeci' in rj:
        print('Vrsta rijeci: '+rj['vrstaRijeci'])
    if 'nepromjenjivo' in rj:
        print('Nepromjenjivo: '+rj['nepromjenjivo'])
    if 'gram_obilj' in rj:
        print('GramObilj: '+str(rj['gram_obilj']))
    if 'rodovi' in rj:
        print('Rodovi: '+str(rj['rodovi']))
    if 'definicije' in rj:
        print('Definicije: ')
        for p in rj['definicije']:
            mojPrintDef(p)
    if 'dodatno' in rj:
        print('Dodatne riječi: '+str(rj['dodatno']))
    if 'podrjetlo' in rj:
        print('Podrjetlo: '+str(rj['podrjetlo']))
    return

def getVariations(string, chars="//"): 
    variations = []
    variations = string.split(chars)
    
    strip_vars = [item.strip() for item in variations]
    
    return strip_vars


def findSemiCol(string, currNum=9, currChar='n'):
    index = 0
    brackO = 0
    brackI = 0
    brackG = 0
    semiColSkip = 0
    prev = ''
    charSearch = 'a'
    inDefChar = False
    
    if currChar != 'n':
        charSearch = NextChar[currChar]
        inDefChar = True
            
    for c in string:
        index += 1
        if c == '(':
            brackO += 1
                
        if c == '[':
            brackI += 1
            
        if c == '{':
            brackG += 1
            
        if brackO > 0:
            if c == ')':
                brackO -= 1
                
        if brackI > 0:
            if c == ']':
                brackI -= 1
        
        if brackG > 0:
            if c == '}':
                brackG -= 1
                          
        if currNum != 9:
            if prev+c == str(currNum+1)+'.':
                index -= 2
                break
                
        if inDefChar:
            if prev+c == charSearch+'.':
                index -= 2
                break
                
        if currChar == 'n' and currNum != 9:
            if prev+c == charSearch+'.':
                charSearch = NextChar[charSearch]
                semiColSkip += 1
                
        if brackO == 0 and brackI == 0 and brackG == 0:
            if c == ';':
                if semiColSkip == 0:
                    break
                
                semiColSkip -= 1
                  
        prev = c
        
    return index
            
                
                

def getPodrucja(string, definicija):
    podrucja = []
    string = string.strip()
    if string == '':
        return string
    if string[0].islower() or string[0].isdigit():
        return string
    
    newstr = re.search(r'([A-ZŠŽ]{2,5}(, )?)*', string)
    
    #podjeli prema zarezu i matcha sa dictom PODRUCJE
    tempPodrucja = newstr.group().split(',')
    tempPodrucja = [ x.strip() for x in tempPodrucja]
    if tempPodrucja == ['']:
        return string
    for i in range(len(tempPodrucja)):
        podrucja.append(PODRUCJE[tempPodrucja[i].strip()])

    definicija["područja"] = podrucja
    return re.sub(newstr.group(), '',string,1)


def getFirstBrackets(string,brackets='()'):
    if string[0] == brackets[0]:
        brack = 0
        num = 0
        for c in string:
            num +=1
            if c == brackets[0]:
                brack += 1
            if c == brackets[1]:
                brack -= 1
            if brack == 0:
                break
        return num
    return len(string)

def getSinonims(string, definicija):
    if re.match(r'.*=> ',string):
        string = string.split('=> ')[1]
        string = string.strip()
        if re.match(r'.*►.*',string):
            #MOZDA STAVIT KLASIFIKACIJU
            string = string.split('►',1)[0]
        if re.match(r'.*;.*',string):
            string, spec = string.split(';',1)
            definicija['special'] = spec.strip()
        string = re.sub(r'\([ 0-9a-z\.A-Z]{1,5}\)','',string)
        definicija['sinonimi'] = getVariations(string, ',')
    
    return

def getPrimjer(string, definicija):
    if re.match(r'.*\[(.*?)\]',string):
        string = re.search(r'\[(.*?)\]',string).group()
        string = string.strip('[]')
        definicija['primjer'] = getVariations(string, ';')
    
    return

def getPadez(string):
    string = string.strip()
    string = string.split(' ',1)[0]
    padez = ""
    
    if len(string) > 1:
        for c in string:
            padez += Skracenice[c] + ', '
        padez = padez[:-2]
    else:
        padez = Skracenice[string]
    
    return padez

def getVrijeme(string, rj):
    string = string.strip()
    for v in vremena:
        if re.match(r'.*{0}.*'.format(v),string):
            if v == 'prez':
                if len(string.split(',')) == 2:
                    str1, str2 = string.split(',')
                    novirj = {}
                    novirj['jednina'] = str1.split(' ',1)[1].strip()
                    novirj['mnozina'] = re.sub('3. l. mn','',str2).strip()
                    rj[Skracenice['prez']] = novirj
                else:
                    rj[Skracenice['prez']] = string.split(' ',1)
                    
                break
            else:
                string = re.sub(r'{0}'.format(v),'',string).strip()
                rj[Skracenice[v]] = string
                break
    return

def getGramObilj(string, rj):
    string = string.strip()
    if string[0].isupper():
        if len(string.split(';',1)) == 2:
            mnozina = {}
            str1, str2 = string.split(';',1)
            
            for st in str1.split(','):
                st = st.strip()
                rj[getPadez(st)] = re.sub(r'^[A-Z]{1,3} ','',st)
                
            naziv = str2.strip().split(' ')[0].strip()
            str2 = re.sub(r'{0}'.format(naziv),'',str2,1)
            str2 = str2.strip()
            novirj = {}
            if naziv == 'odr':
                if len(str2.split(',')) > 1:
                    st, str2 = str2.split(',')
                    novirj['-'] = st
                    
            naziv = Skracenice[naziv]
            if str2:
                for st in str2.split(','):
                    st = st.strip()
                    novirj[getPadez(st)] = re.sub(r'^[A-Z]{1,3} ','',st)
            rj[naziv] = novirj
            return
        
        else:
            for st in string.split(','):
                st = st.strip()
                rj[getPadez(st)] = re.sub(r'^[A-Z]{1,3} ','',st)
    else:
        nvirj = {}
        for gram in string.split(';'):
            getVrijeme(gram, nvirj)
        rj['vremena'] = nvirj
    return

def getDefChar(string, definicija={}, char='a', curnum=1):
    if char == 'a':
        definicija['podjela'] = []  
    pod = {}
        
    split = findSemiCol(string, curnum, char)
    Curr = string[:split].strip()
    Next = string[split:].strip()
    
    Curr = Curr[2:]
    Curr = getPodrucja(Curr,definicija).strip()
    
    pod["-"] = re.split('\[|=> ',Curr,1)[0].strip()
    getPrimjer(Curr, pod)
    getSinonims(Curr, pod)
    
    if Next:
        if Next[0] != NextChar[char]:
            splitter = NextChar[char]+'. '
            pod['special'] = Next.split(splitter,1)[0]
            Next = splitter+Next.split(splitter,1)[1]
            
        nextChar = NextChar[char]+'\. '
        
        if re.match(r'^{0}'.format(nextChar),Next.strip()):
            getDefChar(Next, definicija, NextChar[char], curnum)
    
    definicija["podjela"].insert(0, pod)
            
    return

def getDefNum(string, definicije, definicija = {}, num=1):
    split = findSemiCol(string,num)
    Curr = string[:split].strip()
    Next = string[split:].strip()
    
    #makni broj sa pocetka
    Curr = Curr[2:]
    Curr = getPodrucja(Curr,definicija).strip()
    
    #provjeri jel ima a.
    hasChar = re.match(r'.* a\.',Curr)
    if hasChar and not re.match(r'^a.',Curr):
        newdef, Curr = Curr.split(' a.',1)
        definicija["-"] = newdef
        getDefChar('a.'+Curr,definicija,'a',num)
        
    elif re.match(r'^a\.',Curr):
        getDefChar(Curr,definicija,'a',num)
        
    else:
        definicija["-"] = re.split('\[|=> ',Curr,1)[0].strip()
        getPrimjer(Curr, definicija)
        getSinonims(Curr, definicija)
    
    #provjeri jel nes ostalo
    if Next:
        splitter = str(num+1)+'. '
        if not re.match(r'.*{0}.*'.format(re.escape(splitter)),Next.strip()):
            if Next[0] != str(num+1):
                definicija['special'] = Next
                if len(Next.split(splitter,1)) > 1:
                    Next = splitter+Next.split(splitter,1)[1]
                else:
                    definicija['special'] = Next
                
        else:
            if Next[0] != str(num+1):
                definicija['special'] = Next.split(splitter,1)[0]
                Next = splitter+Next.split(splitter,1)[1]
                
            #procjeri jel ponovo zoves
            nextNum = str(num+1)+'\. '
            newDef = {}
    
            if re.match(r'^{0}'.format(nextNum),Next.strip()):
                getDefNum(Next, definicije, newDef, num+1)
            
    definicije.insert(0, definicija)
            
    return


def getDefinition(string, rjson):
    definicije = []
    definicija = {}
    string = getPodrucja(string, definicija).strip()
    
    if re.match(r'^1.',string):
        getDefNum(string, definicije, definicija)
    else:
        #ideja split('[|;|=')
        definicija["-"] = re.split('\[|=> ',string,1)[0].strip()
        getPrimjer(string, definicija)
        getSinonims(string, definicija)
        definicije.insert(0, definicija)
    
    #ovo provjerit
    if not definicija:
        definicije.insert(0, definicija)

    rjson["definicije"] = definicije
    return



def Prilog(string,rjson):
    rodovi = {}
    definicije = {}
    
    #mice prid na pocetku
    string = string.strip()
    string = re.sub(r'^(.*?)\(','(',string)
    
    #odvaja prvu zagradu
    split = getFirstBrackets(string,'()')
    firstBrackets = string[:split]
    firstBrackets = firstBrackets[1:-1].strip()
    restOfText = string[split:]
    restOfText = restOfText.strip()
    tempGramObilj = ""
    
    rjson['izgovor'] = getVariations(firstBrackets)
        
    rjson['vrstaRijeci'] = 'prilog'
    
    getDefinition(restOfText,rjson)
    return

def Glagol(string,rjson):
    if not re.match(r'.*\(.*',string):
        return
    vrstarj, string = re.split('\(',string,1)
    string = '('+string
    vrstarj = vrstarj.strip()
    vrstarj = re.sub('gl', 'glagol', vrstarj, 1)
    vrstarj = re.sub(' nesvr| nesvr ', ' nesvršeni ', vrstarj, 1)
    vrstarj = re.sub(' svr | svr', ' svršeni ', vrstarj, 1)
    vrstarj = re.sub(' dv | dv',' dvovidni ', vrstarj, 1)
    vrstarj = re.sub(' mn', ' množina', vrstarj)
    if re.match('.*\(neprijel\).*',string):
        vrstarj = vrstarj + 'neprijelazni'
        string = re.sub('\(neprijel\)','',string,1)
    if re.match('.*\(prijel\).*',string):
        vrstarj = vrstarj + 'prijelazni'
        string = re.sub('\(prijel\)','',string,1)
    vrstarj = re.sub(r' +', ' ', vrstarj).strip()
    
    rjson['vrstaRijeci'] = vrstarj
    split = getFirstBrackets(string,'()')
    firstBrackets = string[:split]
    firstBrackets = firstBrackets[1:-1].strip()
    restOfText = string[split:]
    restOfText = restOfText.strip()
    tempGramObilj = ""
    
    if re.match(r'.*neskl.*',firstBrackets):
        rjson['izgovor'] = (re.sub('neskl|\(|\)|\;|\.','',firstBrackets)).strip()
        if not rjson['izgovor']:
            rjson['izgovor'] = getVariations(restOfText[:getFirstBrackets(restOfText,'()')].strip('()'))
            restOfText = (restOfText[getFirstBrackets(restOfText,'()'):]).strip()
            rjson['nepromjenjivo'] = 'true'
        else:
            rjson['izgovor'] = getVariations(rj['izgovor'])
            rjson['nepromjenjivo'] = 'true'
    
    elif re.match(r'.*neskl.*',restOfText[:getFirstBrackets(restOfText,'()')]):
        rodovi['izgovor'] = firstBrackets.strip('()')
        restOfText = (restOfText[getFirstBrackets(restOfText,'()'):]).strip()
        
    else:
        izgovor, tempGramObilj = firstBrackets.split(';',1)
        rjson['izgovor'] = getVariations(izgovor)
        
        gramObilj = {}
        getGramObilj(tempGramObilj, gramObilj)
        rjson['gram_obilj'] = gramObilj
        
    getDefinition(restOfText,rjson)    
        
    return

def Imenica(string,rjson):
    if not re.match(r'.*\(.*',string):
        return
    vrstarj, string = re.split('\(',string,1)
    string = '('+string
    vrstarj = vrstarj.strip()
    vrstarj = re.sub('im', 'imenica', vrstarj)
    vrstarj = re.sub(' m| m ', ' m.r. ', vrstarj, 1)
    vrstarj = re.sub(' ž | ž', ' ž.r. ', vrstarj, 1)
    vrstarj = re.sub(' s | s', ' s.r. ', vrstarj, 1)
    vrstarj = re.sub(' mn', ' množina', vrstarj)
    vrstarj = re.sub(r' +', ' ', vrstarj).strip()
    
    rjson['vrstaRijeci'] = vrstarj
    split = getFirstBrackets(string,'()')
    firstBrackets = string[:split]
    firstBrackets = firstBrackets[1:-1].strip()
    restOfText = string[split:]
    restOfText = restOfText.strip()
    tempGramObilj = ""
    
    if re.match(r'.*neskl.*',firstBrackets):
        rjson['izgovor'] = (re.sub('neskl|\(|\)|\;|\.','',firstBrackets)).strip()
        if not rjson['izgovor']:
            rjson['izgovor'] = getVariations(restOfText[:getFirstBrackets(restOfText,'()')].strip('()'))
            restOfText = (restOfText[getFirstBrackets(restOfText,'()'):]).strip()
            rjson['nepromjenjivo'] = 'true'
        else:
            rjson['izgovor'] = getVariations(rj['izgovor'])
            rjson['nepromjenjivo'] = 'true'
    
    elif re.match(r'.*neskl.*',restOfText[:getFirstBrackets(restOfText,'()')]):
        rjson['izgovor'] = firstBrackets.strip('()')
        restOfText = (restOfText[getFirstBrackets(restOfText,'()'):]).strip()
        
    else:
        izgovor, tempGramObilj = firstBrackets.split(';',1)
        rjson['izgovor'] = getVariations(izgovor)
        
        gramObilj = {}
        getGramObilj(tempGramObilj, gramObilj)
        rjson['gram_obilj'] = gramObilj
        
    getDefinition(restOfText,rjson)    
        
    return

def Pridjev(string,rjson):
    rodovi = {}
    definicije = {}
    
    #mice prid na pocetku
    string = string.strip()
    string = re.sub(r'^(.*?)\(','(',string)
    
    #odvaja prvu zagradu
    split = getFirstBrackets(string,'()')
    firstBrackets = string[:split]
    firstBrackets = firstBrackets[1:-1].strip()
    restOfText = string[split:]
    restOfText = restOfText.strip()
    tempGramObilj = ""
    
    if re.match(r'.*neskl.*',firstBrackets):
        rodovi['nepromjenjivo'] = (re.sub('neskl|\(|\)|\;|\.','',firstBrackets)).strip()
        if not rodovi['nepromjenjivo']:
            rodovi['nepromjenjivo'] = restOfText[:getFirstBrackets(restOfText,'()')].strip('()')
            restOfText = (restOfText[getFirstBrackets(restOfText,'()'):]).strip()
    
    elif re.match(r'.*neskl.*',restOfText[:getFirstBrackets(restOfText,'()')]):
        rodovi['nepromjenjivo'] = firstBrackets.strip('()')
        restOfText = (restOfText[getFirstBrackets(restOfText,'()'):]).strip()
        
    else:
        #tempdeklin = re.search(r'\((.*?)\)',string)[0]
        tempRodovi, tempGramObilj = firstBrackets.split(';',1)
        
        tempMuski, tempZenski, tempSrednji = tempRodovi.split(',')
        
        #odvaja //
        rodovi['muski'] = getVariations(tempMuski)
        rodovi['zenski'] = getVariations(tempZenski)
        rodovi['srednji'] = getVariations(tempSrednji)
        #OVDJE UNUTRA VADIM GRAM OBILJEZJA - GORE IH NEMA
        gramObilj = {}
        getGramObilj(tempGramObilj, gramObilj)
        rjson['gram_obilj'] = gramObilj
        
    rjson['rodovi'] = rodovi
    rjson['vrstaRijeci'] = 'pridjev'
    
    getDefinition(restOfText,rjson)
    return



#POCETAK PROGRAMA
with open("lovro.html", "r", encoding="utf8" ) as html:
    contents = html.read()
    
    soup = BeautifulSoup(contents)
    
    paragraphs = soup.find_all('body')
    

matches = re.sub('<body style="background-color:#FFFFFF;">\n','',str(paragraphs[0]))
matches = re.sub('<p><span class="font3" style="font-weight:bold;color:#7995C7;">(.*?)</p>','',matches)
matches = re.sub('<p>|</p>','',matches)
matches = re.sub('-<br/>','',matches)
matches = re.sub('<br/>',' ',matches)
matches = re.sub('  ',' ',matches)
matches = re.split('<span class="font1" style="font-weight:bold;color:#386EAC;">|<span class="font2" style="font-weight:bold;color:#7C92C0;">|<span class="font3" style="font-weight:bold;color:#3973B3;">|<span class="font3" style="font-weight:bold;color:#3973B3;">|<span class="font6" style="color:#3C75B3;">|<span class="font0" style="font-weight:bold;font-variant:small-caps;color:#427FBE;">|<span class="font2" style="font-weight:bold;color:#3772B1;">|<span class="font2" style="font-weight:bold;color:#3973B2;">|<span class="font2" style="font-weight:bold;color:#427FBE;">',matches)


for entry in matches:
    #((not re.match(r'<span.*',entry)) or (not re.match(r'<body.*',entry)))
    #.strip() mice razmake sa pocetka i kraja
    #.split(',',1)[0] samo jednom splita
    
    #gledamo jel ono zaglavlje
    if re.match(r'.*► ?\d\d\d ?►',re.sub(r' |\n|\t', '', BeautifulSoup(entry).text)):
        continue
    
    if not entry in "\n\t " :
        root = {}
        saHtml = BeautifulSoup(entry)
        HtmlStr = re.sub('<br>','',str(saHtml))
        
        #odvojit c u kruzicu i *** na pocetku
        
        #pretvorimo smallCaps u CAPS pitat profesora za bolji nacin sub r'g<0>' nes
        findCaps = re.findall(r'font\-variant:small\-caps;">[\w ,]{2,15}</span>',HtmlStr)
        for item in findCaps:
            newitem = re.sub('font-variant:small-caps;">','',item)
            newitem = re.sub('</span>','',newitem)
            newitem = newitem.upper()
            newitem = 'font-variant:small-caps;">'+newitem+'</span>'
            HtmlStr = re.sub(item, newitem, HtmlStr)
        
        saHtml = BeautifulSoup(HtmlStr)
        
        #font-variant:small-caps;">pom</span>
        #font-variant:small-caps;">_\g<1>_</span>
        if len(str(saHtml).split('<span',1)) < 2:
            continue
            
        root['Korijen'], tempHtml = str(saHtml).strip().split('<span',1)
        root['Korijen'] = re.sub('<html><body><p>|<sup>|</sup>','',root['Korijen']).strip()
        saHtml = BeautifulSoup(re.sub('(.*?)>','',tempHtml,1))
        entry = saHtml.text
        entry = re.sub('¬ ','',entry)
        entry = re.sub('=►','=>',entry)
        entry = re.sub(r'\s+',' ',entry)
        entry = re.sub("',|-,",';',entry)
        entry = re.sub("3. 1. mn",'3. l. mn',entry)
        
        
        #odvajamo podrjetlo
        if re.search('©',entry):
            entry, podrjetlo = entry.split('©',1)
            root['podrjetlo'] = getVariations(podrjetlo.strip(),'©')
            
        #dodatna upotreba
        if re.search('⁂',entry):
            entry, dodatno = entry.split('⁂',1)
            root['dodatno'] = dodatno.strip()
        #<span class="font1" style="font-weight:bold;color:#386EAC;"> </span>
        
        if re.match(r'^\(= (.*?)\).*',entry.strip()):
            tempekvi = entry.partition(') ')[0]
            tempekvi = re.sub('\(= ','',tempekvi)
            root['ekvivalenta'] = tempekvi
            entry = re.split('\)',entry,1)[1].strip()
            
        if re.match('^.{4,20}\(se\)',entry):
            root['nastavak'] = '(se)'
            entry = re.sub('\(se\)','',entry)
            entry = re.sub('  ',' ',entry)
            
        if entry.strip()[:4] == '(se)':
            entry = re.sub('\(se\)','',entry,1).strip()
            root["nastavak"] = '(se)'
        
        skiping = True
        if re.match(r'^prid',entry):
            skiping = False
            Pridjev(entry,root)
            
        if re.match(r'^im',entry):
            skiping = False
            Imenica(entry,root)
            
        if re.match(r'^gl',entry):
            skiping = False
            Glagol(entry,root)
            
        if re.match(r'^pril',entry):
            skiping = False
            Prilog(entry,root)
            
        if skiping:
            continue
        
        #printRoot(root)
        
        filePathNameWExt = './' + 'JSON-fileovi' + '/' + root['Korijen'] + '.json'
        with open(filePathNameWExt, 'w') as out:
            json.dump(root, out)
        