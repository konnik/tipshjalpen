import csv
import re
import datetime
import englandRepository
import sverigeRepository

ligor = {
    "PL_2019/20": "backend/src/data/england/1-premierleague_20192020.txt",
    "PL_2015/16": "backend/src/data/england/1-premierleague_20152016.txt",
    "CL_20192020": "backend/src/data/championsleague/cl_20192020.txt"
}

def matcherPL():    
    return englandRepository.fetch_PL_2020_21()

def matcherCh():    
    return englandRepository.fetch_Ch_2020_21()

def matcherCH():    
    return allaMatcherForSasong("Championship_2020/21")

def matcherAllsvenskan():
    return sverigeRepository.parseAllsvenskan2020()

def matcherSuperettan():
    return sverigeRepository.parseSuperettan2020()

def parseFile(file, ligatitel):
    f = open(file, encoding='utf8')
    matches = []
    datum = None
    aretRunt = False
    ar = 2020

    for line in f.readlines():
        if line.startswith("="):
            arReg = re.search("\d\d\d\d", line)
            ar = int(arReg.group(0))
            continue

        line = line.lstrip()
        datumRegex = re.search('\[.+\]', line)
        if datumRegex:
            month, day = datumRegex.group(0)[5:-1].split("/")
            if monthDict.get(month) == 1:
                if not aretRunt:
                    aretRunt = True
                    ar += 1

            datum = datetime.date(ar, monthDict.get(month), int(day))
        if len(line.split()) > 4:
            halfTime = None
            fullTime = None
            #Tar bort inledande nuffror
            substrings = re.split("  +", re.sub("\d\d.\d\d\s+", "", line))
            home = substrings[0].strip()
            away = substrings[2].strip()
            scoreString = substrings[1].split()
            if len(scoreString) > 1:
                halfTime = list(map(int, scoreString[1][1:-1].split("-")))
        
            if scoreString[0] != '-':
                fullTime = list(map(int, scoreString[0].split("-")))

            match = Match(datum, home, away, fullTime, halfTime, ligatitel)
            matches.append(match)
    return matches

def allaMatcherTillDatum(ar, manad, dag, liga):
    datum = datetime.date(ar, manad, dag)
    matcher = allaMatcherForSasong(liga)
    return list(filter(lambda x: x.date < datum ,matcher))

def allaMatcherTillDatumForLag(ar, manad, dag, liga):
    datum = datetime.date(ar, manad, dag)
    matcher = allaMatcherForSasong(liga)
    return list(filter(lambda x: x.date < datum ,matcher))

def allaMatcherForSasong(liga):
    return parseFile(ligor.get(liga), liga)

def allaMatcherForLag(lag):
    results = []
    for liga in ligor.keys():       
        for match in allaMatcherForSasong(liga):
            if lag in match.homeTeam or lag in match.awayTeam:
                results.append(match)
    return results

def resultatForLag(lag):
    return list(filter(lambda x: x.fullTime, allaMatcherForLag(lag)))
