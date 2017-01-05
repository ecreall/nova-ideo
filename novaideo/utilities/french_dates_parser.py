# -*- coding: UTF-8 -*-
##                                                                              ##
## Copyright 2006 Ecreall under license CECILL terms,                           ##
## available on "http://www.cecill.info/licences/Licence_CeCILL_V1-fr.html"     ##
## author : Michael launay                                                      ##
## @TODO Modifier getFermeture ##
## Bogue sur getDatesFromPeriode("Du 14 juin au 21 juillet du lundi au dimanche de 14h à 18h, sauf le mardi et les jours fériés")=[[2016, 6, 14, 1, 2], [2016, 6, 15, 2, 3], [2016, 6, 16, 3, 3], [2016, 6, 17, 4, 3], [2016, 6, 18, 5, 3], [2016, 6, 19, 6, 3], [2016, 6, 20, 0, 3], [2016, 6, 22, 2, 4], [2016, 6, 23, 3, 4], [2016, 6, 24, 4, 4], [2016, 6, 25, 5, 4], [2016, 6, 26, 6, 4], [2016, 6, 27, 0, 4], [2016, 6, 29, 2, 5], [2016, 6, 30, 3, 5], [2016, 7, 1, 4, 1], [2016, 7, 2, 5, 1], [2016, 7, 3, 6, 1], [2016, 7, 4, 0, 1], [2016, 7, 6, 2, 1], [2016, 7, 7, 3, 1], [2016, 7, 8, 4, 2], [2016, 7, 9, 5, 2], [2016, 7, 10, 6, 2], [2016, 7, 11, 0, 2], [2016, 7, 13, 2, 2], [2016, 7, 14, 3, 2], [2016, 7, 15, 4, 3], [2016, 7, 16, 5, 3], [2016, 7, 17, 6, 3], [2016, 7, 18, 0, 3], [2016, 7, 20, 2, 3], [2016, 7, 21, 3, 3]]
## Il ne devrait pas y avoir le 1er mardi [2016, 6, 14, 1, 2] !
##

import re
import time
import warnings


def getLocalTime():
   return time.localtime()

def mockLocalTime() :
   #(tm_year=2006, tm_mon=5, tm_mday=15, tm_hour=16, tm_min=38, tm_sec=23, tm_wday=4, tm_yday=135, tm_isdst=1)
   return time.struct_time((2006, 5, 15, 16, 38, 23, 4, 135, 1))

if __name__ == '__main__':
   getLocalTime = mockLocalTime

def getDateAMJNR(pDate) :
   """Donne la date sous forme de tuple [Année, Mois, Jour, IndexNomJour, Rang]"""
   lLocalTime = getLocalTime()
   lTime = time.mktime((pDate and pDate[0] or lLocalTime[0],
                        pDate and pDate[1] or lLocalTime[1],
                        pDate and pDate[2] or lLocalTime[2],
                        0, 0, 0, 0, 0,
                        -1))
   lNewTime = time.localtime(lTime)
   return [lNewTime[0], lNewTime[1], lNewTime[2], lNewTime[6], (lNewTime[2]-1)//7 + 1]

def incDate(pDate, pIncrement = 60 * 60 * 24 + 1) :
   """ Incremente une date exprimée sous forme [Année, Mois, Jour, IndexNomJour, Rang] avec pIncrement exprimmé en secondes"""
   lLocalTime = getLocalTime()
   lTime = time.mktime((pDate and pDate[0] or lLocalTime[0],
                        pDate and pDate[1] or lLocalTime[1],
                        pDate and pDate[2] or lLocalTime[2],
                        0, 0, 0, 0, 0,
                        -1))
   lNewTime = []
   lNewTime.extend(time.localtime(lTime + pIncrement))
   lResult = [lNewTime[0], lNewTime[1], lNewTime[2], lNewTime[6], (lNewTime[2]-1)//7 + 1]
   return lResult

def incJour(pDate) :
    """Incremente la date d'une journée"""
    lDate = incDate(pDate)
    if lDate[2] == pDate[2] :
      lDate = incDate(lDate, 25*60*60+1)
    return lDate
#Les heures
ENM_Heures = "(1[0-9]|2[0-3]|[0-9])h"
ENM_Minutes = "[0-5][0-9]"

ENM_GroupHeuresMinutes = ENM_Heures + "(" + ENM_Minutes + ")?"
ENM_HeuresMinutes = "1[0-9]h[0-5][0-9]|2[0-3]h[0-5][0-9]|[0-9]h[0-5][0-9]|1[0-9]h|2[0-3]h|[0-9]h"
ENM_BlockHeuresMinutes = "(" + ENM_HeuresMinutes + ")"

gExpHeuresMinutes = re.compile(ENM_GroupHeuresMinutes)

def getTimeDeExpHeuresMinutes(pPhrase) :
  """Donne toutes les heures d'une phrase sous forme d'une liste de tuple (H, M)"""
  lMHeuresMinutes = gExpHeuresMinutes.findall(pPhrase)
  if not lMHeuresMinutes :
    return []
  lHeures = []
  for lStrHeure, lStrMinutes in lMHeuresMinutes :
    lHeure = None
    if lStrHeure :
      lHeure = int(lStrHeure)
    lMinutes = None
    if lStrMinutes :
      lMinutes = int(lStrMinutes)
    lHeures.append([lHeure, lMinutes])
  return lHeures

if __name__ == '__main__' :
    #Test unitaire
    #Verification de HeuresMinutes
    print('Verification HeuresMinutes')
    def assertHM(pExp, pPrint = False):
      for h in  range(0, 23) :
        lTest = '%dh'%h
        if pPrint : print('Verification HeuresMinutes test de "%s"' % lTest)
        assert(pExp.match(lTest))
        pass
      for h in  range(0, 23) :
        for m in range(0, 59) :
          lTest = '%dh%0.2d'%(h,m)
          if pPrint : print('Verification HeuresMinutes test de "%s"' % lTest)
          assert(pExp.match(lTest))
          pass
      assert(pExp.match('24h') == None)
      assert(pExp.match('24h60') == None)
      pass

    assertHM(re.compile(ENM_HeuresMinutes))
    lS = "Le 19 avril à 10h30, 11h, 7h, 6h20, 8h59, 14h30 et 16h30 et le 20 avril à 15h13 et 19h40 et de 9h à 12h"
    assert(getTimeDeExpHeuresMinutes(lS) == \
          [[10, 30], [11, None], [7, None], [6, 20], [8, 59], [14, 30], [16, 30], [15, 13], [19, 40], [9, None], [12, None]])

#Le rang
ENM_ValeursRang = ["1er", "2ème", "3ème", "4ème", "5ème"]
ENM_Rang = "|".join(ENM_ValeursRang)
ENM_BlockRang = "(" + ENM_Rang + ")"
#Les jours
ENM_ValeursNomJour = ["lundi",
                     "mardi",
                     "mercredi",
                     "jeudi",
                     "vendredi",
                     "samedi",
                     "dimanche"]
ENM_NomJour = "|".join(ENM_ValeursNomJour)
ENM_BlockNomJour = "(" + ENM_NomJour + ")"

ENM_ValeursNomJours = ["lundis",
                      "mardis",
                      "mercredis",
                      "jeudis",
                      "vendredis",
                      "samedis",
                      "dimanches"]
ENM_NomJours = "|".join(ENM_ValeursNomJours)
ENM_BlockNomJours = "(" + ENM_NomJours + ")"

ENM_ExpGroupRangJour = "(" + ENM_BlockRang + " )?" + ENM_BlockNomJour
gExpGroupRangJour = re.compile(ENM_ExpGroupRangJour)

def getRangJour(pPhrase) :
  """Donne tous les jours d'une phrase sous forme d'une liste de tuple (Jour, Rang)
     Ne fais pas de distinction entre pluriel et singulier.
     S'il n'y a pas de rang alors Rang est None"""
  lJours = []
  for lJ in gExpGroupRangJour.findall(pPhrase) :
    lRang = None
    if lJ[1] :
      lRang = ENM_ValeursRang.index(lJ[1]) + 1
    lJours.append([ENM_ValeursNomJour.index(lJ[2]), lRang])
  return lJours



ENM_ExpNomsJoursJusquAu = "jusqu'au " + ENM_BlockRang + " " + ENM_BlockNomJour \
                        + "|jusqu'au " + ENM_BlockNomJour
ENM_ExpNomsJoursAPartir = "à partir (du " + ENM_BlockRang + " |de )" + ENM_BlockNomJour \
                        + "à partir (du |de )" + ENM_BlockNomJour
ENM_ExpNomsJoursLe = "le (" + ENM_BlockRang + " )?" + ENM_BlockNomJour + "(, (le )?(" + ENM_BlockRang + " )?" + ENM_BlockNomJour + "){,21}( et (le )?(" + ENM_BlockRang + " )?" + ENM_BlockNomJour + ")?"
ENM_ExpNomsJoursDuAu = "du (" + ENM_BlockRang + " )?" + ENM_BlockNomJour + " au (" + ENM_BlockRang + " )?" + ENM_BlockNomJour
ENM_ExpNomsJoursLes = "les (" + ENM_BlockRang + " )?" + ENM_BlockNomJours + "(, (" + ENM_BlockRang + " )?" + ENM_BlockNomJours + "){,21}( et (les )?(" + ENM_BlockRang + " )?" + ENM_BlockNomJours + ")?"
ENM_ExpNomsJours = ENM_ExpNomsJoursJusquAu + "|" + ENM_ExpNomsJoursLe + "|" + ENM_ExpNomsJoursDuAu + "|" + ENM_ExpNomsJoursLes
ENM_BlockExpNomsJours = "(" + ENM_ExpNomsJours + ")"

gExpNomJour = re.compile(ENM_NomJour)
gExpNomsJours = re.compile(ENM_ExpNomsJours)
gExpNomsJoursJusquAu = re.compile(ENM_ExpNomsJoursJusquAu)
gExpNomsJoursAPartir = re.compile(ENM_ExpNomsJoursAPartir)
gExpNomsJoursLe = re.compile(ENM_ExpNomsJoursLe)
gExpNomsJoursDuAu = re.compile(ENM_ExpNomsJoursDuAu)
gExpNomsJoursLes = re.compile(ENM_ExpNomsJoursLes)

def getJoursDeExpNomJour(pPhrase) :
  """Donne tous les numéro des jours utilisé dans pPhrase sous forme du tuple (Numero_jour_de_debut, Numero_jour_de_fin, Rang)
     Ne fais pas de distinction entre pluriel et singulier.
     Si Numero_de_jour_de_debut est None il n'y a pas de jour de debut.
     Si Numero_de_jour_de_fin est None il n'y a pas de jour de fin.
     Si Rang et None il n'y a pas de jour de fin.
     Retourne également la liste des tuples (PosDebut, PosFin, RegularExpression) des concordances."""

  lMatchs = []

  def getListeJour(pPhrase) :
    lJours = []
    for lJ in gExpNomJour.findall(pPhrase) :
      lJours.append(ENM_ValeursNomJour.index(lJ))
    return lJours

  def isAlreadyMatched(pPos) :
    for (lDeb, lFin, lReg) in lMatchs :
      if lDeb <= pPos < lFin :
        return True
    return False

  lNomJours = []

  # traite les séances du type "jusqu'au NomJour"
  lIndexSearch = 0
  while 1 :
    lMNomsJoursJusquAu = gExpNomsJoursJusquAu.search(pPhrase, lIndexSearch)
    if not lMNomsJoursJusquAu :
      break
    lPosDebut, lPosFin = (lMNomsJoursJusquAu.start(), lMNomsJoursJusquAu.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeNomsJours = getListeJour(pPhrase[lPosDebut:lPosFin])
    lNomJours.append([None, lListeNomsJours[0]])
    lMatchs.append([lPosDebut, lPosFin, gExpNomsJoursJusquAu])

  # traite les séances du type "à partir du NomJour"
  lIndexSearch = 0
  while 1 :
    lMNomsJoursAPartir = gExpNomsJoursAPartir.search(pPhrase, lIndexSearch)
    if not lMNomsJoursAPartir :
      break
    lPosDebut, lPosFin = (lMNomsJoursAPartir.start(), lMNomsJoursAPartir.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeNomsJours = getListeJour(pPhrase[lPosDebut:lPosFin])
    lNomJours.append([lListeNomsJours[0], None])
    lMatchs.append([lPosDebut, lPosFin, gExpNomsJoursAPartir])

  # traite les séances du type "le NomJour"
  lIndexSearch = 0
  while 1 :
    lMNomsJoursLe = gExpNomsJoursLe.search(pPhrase, lIndexSearch)
    if not lMNomsJoursAPartir :
      break
    lPosDebut, lPosFin = (lMNomsJoursLe.start(), lMNomsJoursLe.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeNomsJours = getListeJour(pPhrase[lPosDebut:lPosFin])
    lNomJours.append([lListeNomsJours[0], None])
    lMatchs.append([lPosDebut, lPosFin, gExpNomsJoursLe])

  # traite les séances du type "du NomJour au NomJour"
  lIndexSearch = 0
  while 1 :
    lMNomsJoursDuAu = gExpNomsJoursDuAu.search(pPhrase, lIndexSearch)
    if not lMNomsJoursDuAu :
      break
    lPosDebut, lPosFin = (lMNomsJoursDuAu.start(), lMNomsJoursDuAu.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeNomsJours = getListeJour(pPhrase[lPosDebut:lPosFin])
    lNomJours.append([lListeNomsJours[0], lListeNomsJours[1]])
    lMatchs.append([lPosDebut, lPosFin, gExpNomsJoursDuAu])

  # traite les séances du type "les NomJours(, NomJours)* et NomJour"
  lIndexSearch = 0
  while 1 :
    lMNomsJoursLes = gExpNomsJoursLes.search(pPhrase, lIndexSearch)
    if not lMNomsJoursLes :
      break
    lPosDebut, lPosFin = (lMNomsJoursLes.start(), lMNomsJoursLes.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeNomsJours = getListeJour(pPhrase[lPosDebut:lPosFin])
    lNomJours.extend([[lJ, None] for lJ in lListeNomsJours])
    lMatchs.append([lPosDebut, lPosFin, gExpNomsJoursLes])
  return [lNomJours, lMatchs]

if __name__ == '__main__' :
    #Test unitaire
    print("Verification de getJoursDeExpNomJour")
    lS = "Tous les lundis, mardis, mercredis sauf les 1er lundis du mois"
    print( "(\"%s\", %s)"%(lS, getJoursDeExpNomJour(lS)))
    assert(getJoursDeExpNomJour(lS)[0] == [[0, None], [1, None], [2, None], [0, None]])

#Les périodes
ENM_ValeursMatinMidiSoir = ["soir", "matin", "midi", "après-midi", "week-end"]
ENM_MatinMidiSoir = "|".join(ENM_ValeursMatinMidiSoir)
ENM_BlockMatinMidiSoir = "(" + ENM_MatinMidiSoir + ")"

ENM_ValeursMatinsMidisSoirs = ["soirs", "matins", "midis", "après-midis", "week-ends"]
ENM_MatinsMidisSoirs = "|".join(ENM_ValeursMatinsMidisSoirs)
ENM_BlockMatinsMidisSoirs = "(" + ENM_MatinsMidisSoirs + ")"

#Les numéros des jours
ENM_JourCalendaire = "1er|[1-2][0-9]|3[0-1]|[2-9]"

#Les mois
ENM_ValeursMois = ["janvier",
                   "février",
                   "mars",
                   "avril",
                   "mai",
                   "juin",
                   "juillet",
                   "août",
                   "septembre",
                   "octobre",
                   "novembre",
                   "décembre",]

ENM_Mois = "|".join(ENM_ValeursMois)

#Le premier du mois
ENM_PremierDuMois = "1er (" + ENM_Mois + ")"

#L'année
ENM_Annee = "20[0-9][0-9]"


#Les séances
ENM_ExpListeSeances = "à " + ENM_BlockHeuresMinutes + "((, (à )?" + ENM_BlockHeuresMinutes + "){,99}" + " et (à )?" + ENM_BlockHeuresMinutes + ")?"
ENM_ExpHeureDebut = "(dès |à partir de |départ à )" + ENM_BlockHeuresMinutes
ENM_ExpPeriodes = "de " + ENM_BlockHeuresMinutes + " à " + ENM_BlockHeuresMinutes + "(, de " + ENM_BlockHeuresMinutes + " à " + ENM_BlockHeuresMinutes + "){,99}" + "( et de " + ENM_BlockHeuresMinutes + " à " + ENM_BlockHeuresMinutes +")?"
ENM_ExpJusquA = "jusqu'à " + ENM_BlockHeuresMinutes
ENM_ExpPseudoPeriode = "de " + ENM_BlockHeuresMinutes + " (jusqu'à l'aube|jusqu'à plus soif)"


ENM_HeureSeances = ENM_ExpListeSeances + "|" + ENM_ExpHeureDebut + "|" + ENM_ExpPeriodes + "|" + ENM_ExpJusquA + "|" + ENM_ExpPseudoPeriode
ENM_BlockHeureSeances =  "(" + ENM_HeureSeances + ")"

gExpListeSeances = re.compile(ENM_ExpListeSeances)
gExpHeureDebut = re.compile(ENM_ExpHeureDebut)
gExpPeriodes = re.compile(ENM_ExpPeriodes)
gExpJusquA = re.compile(ENM_ExpJusquA)
gExpPseudoPeriode = re.compile(ENM_ExpPseudoPeriode)

gTokenDuAu = re.compile("^Du ")
gTokenDuAuAu = re.compile(" au ")
gTokenDuAuRDV = re.compile(" et sur RDV")


def getHeuresDeExpHeureSeances(pPhrase) :
  """Donne tous les tuples (Heure_de_debut, Heure_de_fin) d'une phrase
     Si Heure_de_debut est None il n'y a pas d'heure de debut.
     Si Heure_de_fin est None il n'y a pas d'heure de fin.
     Retourne également la liste des tuples (PosDebut, PosFin, RegularExpression) des concordances."""

  lMatchs = []

  def isAlreadyMatched(pPos) :
    for (lDeb, lFin, lReg) in lMatchs :
      if lDeb <= pPos < lFin :
        return True
    return False

  lHeures = []
  lIndexSearch = 0

  # traite les séances du type "de HHhMM jusqu'à l'aube"
  lIndexSearch = 0
  while 1 :
    lMPseudoPeriode = gExpPseudoPeriode.search(pPhrase, lIndexSearch)
    if not lMPseudoPeriode :
      break
    lPosDebut, lPosFin = (lMPseudoPeriode.start(), lMPseudoPeriode.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeHeures = getTimeDeExpHeuresMinutes(pPhrase[lPosDebut:lPosFin])
    lHeures.append([lListeHeures[0], None])
    lMatchs.append([lPosDebut, lPosFin, gExpPseudoPeriode])

  # traite les seances du type 'de HHhMM à HHhMM'
  while 1 :
    lMPeriodes = gExpPeriodes.search(pPhrase, lIndexSearch)
    if not lMPeriodes :
      break
    lPosDebut, lPosFin = (lMPeriodes.start(), lMPeriodes.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeHeures = getTimeDeExpHeuresMinutes(pPhrase[lPosDebut:lPosFin])
    assert(not len(lListeHeures) % 2)
    for lIndex in range(0, len(lListeHeures), 2) :
      lHeures.append([lListeHeures[lIndex], lListeHeures[lIndex + 1]])
    lMatchs.append([lPosDebut, lPosFin, gExpPeriodes])

  # traite les séances du type 'Jusqu'à HHhMM'
  lIndexSearch = 0
  while 1 :
    lMJusquA = gExpJusquA.search(pPhrase, lIndexSearch)
    if not lMJusquA :
      break
    lPosDebut, lPosFin = (lMJusquA.start(), lMJusquA.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeHeures = getTimeDeExpHeuresMinutes(pPhrase[lPosDebut:lPosFin])
    lHeures.extend([[None, lHeureFin] for lHeureFin in lListeHeures])
    lMatchs.append([lPosDebut, lPosFin, gExpJusquA])

  # traite les séances du type "à partir de, dès"
  lIndexSearch = 0
  while 1 :
    lMHeuresDebut = gExpHeureDebut.search(pPhrase, lIndexSearch)
    if not lMHeuresDebut :
      break
    lPosDebut, lPosFin = (lMHeuresDebut.start(), lMHeuresDebut.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeHeures = getTimeDeExpHeuresMinutes(pPhrase[lPosDebut:lPosFin])
    lHeures.extend([[lHeureDebut, None] for lHeureDebut in lListeHeures])
    lMatchs.append([lPosDebut, lPosFin, gExpJusquA])

  # traite les séances du type "à HHhMM, HHhMM, et HHhMM"
  lIndexSearch = 0
  while 1 :
    lMListesSeances = gExpListeSeances.search(pPhrase, lIndexSearch)
    if not lMListesSeances :
      break
    lPosDebut, lPosFin = (lMListesSeances.start(), lMListesSeances.end())
    lIndexSearch = lPosFin
    if isAlreadyMatched(lPosDebut) :
      continue
    lListeHeures = getTimeDeExpHeuresMinutes(pPhrase[lPosDebut:lPosFin])
    lHeures.extend([[lHeureDebut, None] for lHeureDebut in lListeHeures])
    lMatchs.append([lPosDebut, lPosFin, gExpListeSeances])

  return (lHeures, lMatchs)

if __name__ == '__main__' :
    #Test unitaire
    print( "Verification de getHeuresDeGroupHeureSeances")
    lS = "Le 19 avril à 10h30, 11h, 7h, 6h20, 8h59, 14h30 et 16h30 et le 20 avril à 15h13 et 19h40 et de 9h à 12h"
    assert(getHeuresDeExpHeureSeances(lS)[0] == [[[9, None], [12, None]],[[10, 30], None], [[11, None], None], [[7, None], None], [[6, 20], None], [[8, 59], None], [[14, 30], None], [[16, 30], None], [[15, 13], None], [[19, 40], None]])


#Date
ENM_DateJour= "(" + ENM_JourCalendaire + ")( (" + ENM_Mois + ")( " + ENM_Annee + ")?)?"
ENM_BlockDateJour = "(" + ENM_DateJour + ")"

ENM_TousLesMatinsMidisSoirs = " tous les " + ENM_BlockMatinsMidisSoirs
ENM_DateJourSeances = ENM_DateJour + "((," + ENM_TousLesMatinsMidisSoirs + "|, le " + ENM_BlockMatinMidiSoir + "|(,)? " + ENM_BlockExpNomsJours + ")?" + "( " + ENM_BlockHeureSeances + ")?){,99}"
ENM_BlockDateJourSeances = "(" + ENM_DateJourSeances + ")"

ENM_BreakSeances = "fermeture|fermé|sauf"

gExpTousLesMatinsMidisSoirs = re.compile(ENM_TousLesMatinsMidisSoirs)
gExpDateJourSeances = re.compile(ENM_DateJourSeances)
gExpJourCalendaire = re.compile(ENM_JourCalendaire)
gExpMois = re.compile(ENM_Mois)
gExpAnnee = re.compile(ENM_Annee)
gExpBreakSeances = re.compile(ENM_BreakSeances)

ANNEE = 0
MOIS = 1
JOUR = 2
#NOM_JOUR = 3
#RANG = 4
SEANCES = 3
HEURE_DEBUT = 0
HEURE_FIN = 1
def getExpDateJourSeances(pPhrase) :
  """Donne la liste des jours avec leur séances
     sous forme d'une liste de tuples (Annee, Mois, DateJour, IndexJour, Rang, (Heure_de_debut,Heure_de_fin)*)
     Si Annee est None il n'y a pas d'année.
     Si Mois est None il n'y a pas de Mois.
     Si Mois est not None alors IndexJour est la position donnée par getJoursDeExpNomJour
     Si Heure_de_debut et None il n'y a pas d'heure de debut.
     Si Heure_de_fin et None il n'y a pas d'heure de fin.
     Retourne également la liste des tuples (PosDebut, PosFin, RegularExpression) des concordances."""
  lDates = []
  lMatches = []
  lIndexPhrase = 0
  lMBreak = gExpBreakSeances.search(pPhrase)
  while 1 :
    lMDateJour = gExpDateJourSeances.search(pPhrase, lIndexPhrase)
    if not lMDateJour :
      break
    lPosDebut = lMDateJour.start()
    lPosFin = lIndexPhrase = lMDateJour.end()

    if lMBreak and lMBreak.start() < lPosDebut :
      break

    lStrDate = pPhrase[lPosDebut:lPosFin]
    lJour = lMois = lAnnee = lSeances = None

    lMJour = gExpJourCalendaire.search(lStrDate)
    assert(lMJour)
    lJour = lMJour.group()
    if ENM_ValeursRang.count(lJour) :
      lJour = str(ENM_ValeursRang.index(lJour) + 1)
    lJour = int(lJour)

    lStrDate = lStrDate[lMJour.end():]
    lMMois = gExpMois.search(lStrDate)
    if lMMois :
      lStrDate = lStrDate[lMMois.end():]
      lMois = lMMois.group()
      assert(ENM_ValeursMois.count(lMois))
      lMois = int(ENM_ValeursMois.index(lMois) + 1)

    lMAnnee = gExpAnnee.search(lStrDate)
    if lMAnnee :
      lStrDate = lStrDate[lMAnnee.end():]
      lAnnee = int(lMAnnee.group())

    lMNomsJours = gExpNomsJours.search(lStrDate)
    if lMNomsJours :
#      lNomsJours = getJoursDeExpNomJour(lStrDate)
      lStrDate = lStrDate[lMNomsJours.end():]

    lSeances = getHeuresDeExpHeureSeances(lStrDate)
    if lSeances :
      lHeuresSeances = lSeances[0] # ne prend pas la liste des expressions regulieres de séances ayant été trouvées
    #calcul la position du break dans la sous chaîne
    lMLocalBreak = gExpBreakSeances.search(lStrDate)
    if lMLocalBreak :
      #Ne prend en compte que les séances situées avant le break
      lPosBreak = lMLocalBreak.start()
      lHeuresSeances = []
      for lSeance, lReg in lSeances :
        if lPosBreak < lReg[0] :
          lHeuresSeances.append(lSeance)

    lDates.append([lAnnee, lMois, lJour, lHeuresSeances,])


    lMatches.append([lPosDebut, lPosFin, gExpDateJourSeances,])
  if not lDates :
    return None
  return (lDates, lMatches)
  pass

ENM_FermetureNom = "(, | et | [(])?((fermeture le|fermé le|relâche le) (" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + "(,( le)? (" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + "){,99}" + "((,)? et (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + ")?" \
                          + "|(fermeture les|fermé les|relâche les) (jours fériés|(" +  ENM_BlockRang + " )?" + ENM_BlockNomJours + "(, (" +  ENM_BlockRang + " )?" + ENM_BlockNomJours + "){,99}" + "((,)? et (" +  ENM_BlockRang + " )?" + ENM_BlockNomJours + ")?( du mois)?))[)]?"

ENM_FermetureNomDuAu = "(, | et | [(])?(fermeture|fermé|relâche) (?P<DateFermeture>du (" +  ENM_BlockRang + " )?"+ ENM_BlockNomJour + " au (" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + ")( du mois)?[)]?"
ENM_OvertureNomDuAu = "(, | et )? (?P<DateOuvertur>du "+ ENM_BlockNomJour + " au " + ENM_BlockNomJour + ")( " + ENM_BlockHeureSeances + ")?(, le " + ENM_BlockNomJour + "( " + ENM_BlockHeureSeances + ")?){,4}( et le " + ENM_BlockNomJour + "( " + ENM_BlockHeureSeances + ")?)?"

ENM_FermetureNomSeancesLe = "(, | et | [(])?((fermeture le|fermé le|relâche le) (" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + " " + ENM_BlockHeureSeances + "(,( le)? (" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + " " + ENM_BlockHeureSeances + "){,99}" + "((,)? et (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + " " + ENM_BlockHeureSeances + ")?)[)]?"

ENM_FermetureNomSeancesLes = "(, | et | [(])?((fermeture les|fermé les|relâche les) (jours fériés|(" +  ENM_BlockRang + " )?" + ENM_BlockNomJours + " " + ENM_BlockHeureSeances + "(, (" +  ENM_BlockRang + " )?" + ENM_BlockNomJours + " " + ENM_BlockHeureSeances + "){,99}" + "((,)? et (" +  ENM_BlockRang + " )?" + ENM_BlockNomJours + " " + ENM_BlockHeureSeances + ")?( du mois)?))[)]?"

ENM_FermetureDate =  "(, | et | \()?(fermeture|fermé|relâche) (?P<DateFermeture>(du " + ENM_DateJour + " au |le )?" + ENM_DateJour + ")\)?"
ENM_FermetureDateSeances =  "(, | et | \()?(fermeture|fermé|relâche) (?P<DateFermeture>(du " + ENM_DateJour + " " + ENM_BlockHeureSeances + " au |le )?" + ENM_DateJour + " " + ENM_BlockHeureSeances + ")\)?"

ENM_Fermeture = "^" + ENM_FermetureNom + "|^" + ENM_FermetureDate

ENM_TousSauf = "(,)? (tous les jours )?sauf ((le )?"  + ENM_DateJour + "|les jours fériés)"
ENM_TousSaufSeances = "(,)? (tous les jours )?sauf ((le )?"  + ENM_DateJour + " " + ENM_BlockHeureSeances + "|les jours fériés)"

ENM_TousSaufNomJour = "(,)? (tous les jours )?sauf (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + "(, (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + "){,99}" + "((,)? et (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + ")?((,)? et les jours fériés)?"
ENM_TousSaufNomJourSeances = "(,)? (tous les jours )?sauf (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + " " + ENM_BlockHeureSeances + "(, (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + " " + ENM_BlockHeureSeances + "){,99}" + "((,)? et (le )?(" +  ENM_BlockRang + " )?" + ENM_BlockNomJour + " " + ENM_BlockHeureSeances + ")?((,)? et les jours fériés)?"

gExpFermetureNom = re.compile(ENM_FermetureNom)
gExpFermetureNomDuAu = re.compile(ENM_FermetureNomDuAu)
gExpOuvertureNomDuAu = re.compile(ENM_OvertureNomDuAu)
gExpFermetureNomSeancesLe = re.compile(ENM_FermetureNomSeancesLe)
gExpFermetureNomSeancesLes = re.compile(ENM_FermetureNomSeancesLes)
gExpFermetureDate = re.compile(ENM_FermetureDate)
gExpFermetureDateSeances = re.compile(ENM_FermetureDateSeances)
gExpFermeture = re.compile(ENM_Fermeture)
gExpTousSauf = re.compile(ENM_TousSauf)
gExpTousSaufSeances = re.compile(ENM_TousSaufSeances)
gExpTousSaufDeb = re.compile("^" + ENM_TousSauf)
gExpTousSaufNomJour = re.compile(ENM_TousSaufNomJour)
gExpTousSaufNomJourDeb = re.compile("^" + ENM_TousSaufNomJour)
gExpTousSaufNomJourSeances = re.compile(ENM_TousSaufNomJourSeances)
gTokenJusquAu = re.compile("^Jusqu'au ")
gTokenJusquAuTousLes = re.compile("^ tous les " + ENM_BlockMatinMidiSoir)
gTokenJusquAuVirgule = re.compile("^, le ")
gTokenLe = re.compile("^Le ")
gTokenLes = re.compile("^Les ")
gTokenLeOuLesEt = re.compile("^(, et le |, le |, | et le | et les |, les | et )")


def getJusquAu(pPhrase):
    """Retourne la date de fin ou la chaîne d'erreur"""
    # vérifie la syntaxe
    lMTokenJusquAu = gTokenJusquAu.match(pPhrase)
    if not lMTokenJusquAu :
        return None
    lIndex = lMTokenJusquAu.end()
    lResult = getExpDateJourSeances(pPhrase[lIndex:])
    if not lResult :
        raise AttributeError("Seule la partie \"Jusqu'au \" est correcte", pPhrase)
    lDeb, lFin, lReg = lResult[1][0]
    if lDeb != 0 :
        raise AttributeError("Seule la partie \"Jusqu'au \" est correcte", pPhrase)
    if lFin + lIndex != len(pPhrase) :
        lToken = pPhrase[lIndex + lFin :]
        if not gTokenJusquAuTousLes.match(lToken) and not gTokenJusquAuVirgule.match(lToken)\
          and not gExpFermeture.match(lToken) and not gExpTousSaufDeb.match(lToken)\
          and not gExpTousSaufNomJourDeb.match(lToken) and not gExpTousLesMatinsMidisSoirs.match(lToken)\
          and not gTokenLeOuLesEt.match(lToken) and not gExpFermeture.match(lToken) :
          raise AttributeError("Seule la partie \"%s\" a été reconnue" % pPhrase[:lIndex + lFin], pPhrase)
    else :
      lOldFin = lFin
      for lDeb, lFin, lReg in lResult[1][1:] :
        lToken = pPhrase[lIndex + lOldFin : lIndex + lDeb]
        if not gTokenJusquAuTousLes.match(lToken) and not gTokenJusquAuVirgule.match(lToken)\
          and not gExpFermeture.match(lToken) and not gExpTousSaufDeb.match(lToken)\
          and not gExpTousSaufNomJourDeb.match(lToken) and not gExpTousLesMatinsMidisSoirs.match(lToken)\
          and not gTokenLeOuLesEt.match(lToken) and not gExpFermeture.match(lToken) :
          raise AttributeError("Seule la partie \"%s\" a été reconnue" % pPhrase[:lIndex + lOldFin], pPhrase)
        lOldFin = lFin
    # transforme et vérifie les dates
    lJusquAuDate = lResult[0][0]
    if not lJusquAuDate[JOUR] :
        raise AttributeError("Veuillez saisir le jour (1 à 31) de la date butoire", pPhrase)
    if not lJusquAuDate[MOIS] :
        raise AttributeError("Le mois de la date butoire doit être saisie", pPhrase)
    if not lJusquAuDate[ANNEE] :
        lJusquAuDate[ANNEE] = getLocalTime()[0]
    lIndex = 1
    try :
#      lEndTime = time.strptime("%d-%d-%d"%(lJusquAuDate[ANNEE], lJusquAuDate[MOIS], lJusquAuDate[JOUR]), "%Y-%m-%d")
      for lDate in lResult[0][1:] :
        lAutreDate = []
        lAutreDate.extend(lDate)
        lIndex += 1
        if not lAutreDate[MOIS] :
          lAutreDate[MOIS] = lJusquAuDate[MOIS]
        if not lAutreDate[ANNEE] :
          lAutreDate[ANNEE] = lJusquAuDate[ANNEE]
#        lAutreTime = time.strptime("%d-%d-%d"%(lAutreDate[ANNEE], lAutreDate[MOIS], lAutreDate[JOUR]), "%Y-%m-%d")
        if (lAutreDate[ANNEE], lAutreDate[MOIS], lAutreDate[JOUR]) > (lJusquAuDate[ANNEE], lJusquAuDate[MOIS], lJusquAuDate[JOUR]) :
          raise AttributeError("La %dème date donnée ne doit pas être postérieure à la date butoire"%lIndex, pPhrase)
      return [None, lJusquAuDate]
    except ValueError :
      if lIndex == 1 :
        raise AttributeError("La première date donnée n'est pas cohérente", pPhrase)
      else :
        raise AttributeError("La %dème date donnée n'est pas cohérente" % lIndex, pPhrase)

def getJoursFermes(pPhrase) :
    """Donne les jours de fermeture sous forme d'une liste de liste [Annee, Mois, Jour, IndiceNomJour, RangJour]"""
    lMatchs = []

    def isAlreadyMatched(pPos) :
      for (lDeb, lFin) in lMatchs :
        if lDeb <= pPos < lFin :
          return True
      return False

    def getPeriodeJour(pJourDebut, pJourFin):
      lJourDebut, lRangDebut = pJourDebut
      lJourFin, lRangFin = pJourFin
      lJours = []
      lJours.append(pJourDebut)
      if not lRangFin and not lRangDebut :
        if lJourFin < lJourDebut :
          for lDate in range(lJourDebut + 1, lJourFin + 7) :
            lJours.append([lDate%7, None])
        else :
          for lDate in range(lJourDebut + 1, lJourFin) :
            lJours.append([lDate%7, None])
      else :
        lDateDebut = 7 * (lRangDebut or 1) + lJourDebut + 1
        lDateButee = 7 * (lRangFin or 1) + lJourFin
        if lDateButee < lDateDebut :
           raise AttributeError("Les Nième jours doivent être dans l'ordre croissant, ex: \"du 1er mardi au 3ème lundi\"", pPhrase)
        for lDate in range(lDateDebut, lDateButee) :
           lJours.append([lDate%7,lDate//7])
      lJours.append(pJourFin)
      return lJours

    lDatesFermees = []
    lJoursFermes = []
    lStart = lEnd = None
    lMFermetureNomSeancesLe = gExpFermetureNomSeancesLe.search(pPhrase)
    lMFermetureNomSeancesLes = gExpFermetureNomSeancesLes.search(pPhrase)
    lMTousSaufSeances = gExpTousSaufSeances.search(pPhrase)
    lMTousSaufNomJourSeances = gExpTousSaufNomJourSeances.search(pPhrase)
    lMFermetureDateSeances = gExpFermetureDateSeances.search(pPhrase)
    if lMFermetureNomSeancesLe or lMFermetureNomSeancesLes or lMTousSaufSeances \
                               or lMTousSaufNomJourSeances or lMFermetureDateSeances:
      lStart = (lMFermetureNomSeancesLe or lMFermetureNomSeancesLes or lMTousSaufSeances\
                                        or lMTousSaufNomJourSeances or lMFermetureDateSeances).start()
      lEnd = (lMFermetureNomSeancesLe or lMFermetureNomSeancesLes or lMTousSaufSeances\
                                      or lMTousSaufNomJourSeances or lMFermetureDateSeances).end()
      if not isAlreadyMatched(lStart) :
        lMatchs.append((lStart, lEnd))

    lMFermetureNom = gExpFermetureNom.search(pPhrase)
    if lMFermetureNom :
        lStart = lMFermetureNom.start()
        lEnd = lMFermetureNom.end()
        if not isAlreadyMatched(lStart) :
          lListeJour = getRangJour(pPhrase[lStart : lEnd])
          if lListeJour :
            lJoursFermes.extend(lListeJour)
            lMatchs.append((lStart, lEnd))

    lMFermetureNomDuAu = gExpFermetureNomDuAu.search(pPhrase)
    if lMFermetureNomDuAu :
        lStart = lMFermetureNomDuAu.start()
        lEnd = lMFermetureNomDuAu.end()
        if not isAlreadyMatched(lStart) :
          lSubPhrase = lMFermetureNomDuAu.group('DateFermeture')
          lListeJour = getRangJour(lSubPhrase)
          lMatchs.append((lStart, lEnd))
          if lListeJour :
            lJourDebut = lListeJour[0]
            if len(lListeJour) == 2 :
              lJourFin = lListeJour[-1]
              lJoursFermes.extend(getPeriodeJour(lJourDebut, lJourFin))
            else :
              lJoursFermes.append(lJourDebut)


    lMFermetureDate = gExpFermetureDate.search(pPhrase)
    if lMFermetureDate :
        lStart = lMFermetureDate.start()
        lEnd = lMFermetureDate.end()
        if not isAlreadyMatched(lStart) :
          lSubPhrase = lMFermetureDate.group('DateFermeture')
          lExpDateJourSeances = getExpDateJourSeances(lSubPhrase)
          if lExpDateJourSeances :
            lDateDebut = getDateAMJNR(lExpDateJourSeances[0][0][0:3])
            lDatesFermees.append(lDateDebut)
            if len(lExpDateJourSeances[0]) == 2 :
              lDateFin = getDateAMJNR(lExpDateJourSeances[0][1][0:3])
              if lDateFin < lDateDebut :
                raise AttributeError("Les dates doivent être dans l'ordre croissant, si vos dates sont sur des années différentes veuillez donner la date complète", pPhrase)
              lDate = incJour(lDateDebut)
              while lDate < lDateFin :
                lDatesFermees.append(lDate)
                lDate = incJour(lDate)
              lDatesFermees.append(lDateFin)
            lMatchs.append((lStart, lEnd))

    lMTousSauf = gExpTousSaufNomJour.search(pPhrase)
    if lMTousSauf :
        lStart = lMTousSauf.start()
        lEnd = lMTousSauf.end()
        if not isAlreadyMatched(lStart) :
          lListeJour = getRangJour(pPhrase[lStart : lEnd])
          if lListeJour :
            lJoursFermes.extend(lListeJour)
            lMatchs.append((lStart, lEnd))

    lMSauf = gExpTousSauf.search(pPhrase)
    if lMSauf :
        lStart = lMSauf.start()
        lEnd = lMSauf.end()
        if not isAlreadyMatched(lStart) :
          lExpDateJourSeances = getExpDateJourSeances(pPhrase[lStart : lEnd])
          if lExpDateJourSeances :
            lDateDebut = getDateAMJNR(lExpDateJourSeances[0][0][0:3])
            lDatesFermees.append(lDateDebut)
            lMatchs.append((lStart, lEnd))

    lMOuverture = gExpOuvertureNomDuAu.search(pPhrase)
    if lMOuverture :
        lStart = lMOuverture.start()
        lEnd = lMOuverture.end()
        if not isAlreadyMatched(lStart) :
          lListeJour = getRangJour(pPhrase[lStart : lEnd])
          if lListeJour :
            lJourDebut = lListeJour[0]
            lJourFin = lListeJour[1]
            lJoursOuverts = getPeriodeJour(lJourDebut, lJourFin)
            if len(lListeJour) > 2 :
              lJoursOuverts.extend(lListeJour[2:])
          lListeJoursSemaine = [ [lNom, None] for lNom in range(0,7)]
          for lJ in lJoursOuverts :
            if lListeJoursSemaine.count(lJ) :
              lListeJoursSemaine.remove(lJ)
          if lListeJoursSemaine :
            lJoursFermes.extend(lListeJoursSemaine)

    lDates = []
    lDates.extend([[None, None, None, lNom, lRang] for (lNom, lRang) in lJoursFermes])
    lDates.extend(lDatesFermees)
    return lDates

if __name__ == '__main__' :
    #Test unitaire
    print( "Verification de getJoursFermes")
    lAnnee = getLocalTime()[0]
    lTestFermeture = [
      ["Jusqu'au 1er juillet, tous les soirs à 20h30, le 25 juin à 15h30, relâche les lundis et dimanches",
       [[None, None, None, 0, None], [None, None, None, 6, None]]],
      ["Du 14 juin au 21 juillet du lundi au dimanche de 14h à 18h, sauf le mardi et les jours fériés",
       [[None, None, None, 1, None]]],
      ["Du 25 mai au 9 juillet tous les jours sauf le lundi",
       [[None, None, None, 0, None]]],
      ["Du 25 mai au 9 juillet tous les jours sauf le lundi de 11h à 18h",
       []],
      ["Du 3 janvier au 14 janvier 2007 tous les jours sauf le mardi, le samedi, et le dimanche",
       [[None, None, None, 1, None], [None, None, None, 5, None], [None, None, None, 6, None]]],
      ["Du 3 janvier au 14 janvier 2007 tous les jours sauf mardi de 10h à 12h et de 14h à 17h30, le samedi jusqu'à 18h30, le dimanche de 14h à 18h30",
       []],
      ["Du 20 juin au 26 juillet du mardi au samedi de 14h à 18h (fermé les jours fériés)",
       [[None, None, None, 0, None], [None, None, None, 6, None]]],
      ["Du 7 au 30 juin (fermé le lundi)",
       [[None, None, None, 0, None]]],
      ["Du 17 au 23 juin (fermé du lundi au mercredi)",
       [[None, None, None, 0, None], [None, None, None, 1, None], [None, None, None, 2, None]]],
      ["Du 7 au 13 juin (fermé du jeudi au mardi]",
       [[None, None, None, 3, None], [None, None, None, 4, None], [None, None, None, 5, None],
        [None, None, None, 6, None], [None, None, None, 0, None], [None, None, None, 1, None]]],
      ["Du 15 au 23 juin (fermé du vendredi au mercredi)",
       [[None, None, None, 4, None], [None, None, None, 5, None], [None, None, None, 6, None],
        [None, None, None, 0, None], [None, None, None, 1, None], [None, None, None, 2, None]]],
      ["Du 1er juin au 3 août (fermé du 1er lundi au 3ème mercredi)",
       [[None, None, None, 0, 1], [None, None, None, 1, 1], [None, None, None, 2, 1], [None, None, None, 3, 1],
        [None, None, None, 4, 1], [None, None, None, 5, 1], [None, None, None, 6, 1],
        [None, None, None, 0, 2], [None, None, None, 1, 2], [None, None, None, 2, 2], [None, None, None, 3, 2],
        [None, None, None, 4, 2], [None, None, None, 5, 2], [None, None, None, 6, 2],
        [None, None, None, 0, 3], [None, None, None, 1, 3], [None, None, None, 2, 3],
       ]],
      ["Du 5 juillet au 1er septembre du mardi au vendredi de 9h à 12h et de 14h à 18h, le lundi de 15h à 18h, les 10, 17 et 24 juin de 9h à 12h et de 15h à 15h30 (fermeture du 24 juillet au 20 août)",
       [[None, None, None, 5, None], [None, None, None, 6, None],
        getDateAMJNR((lAnnee, 7, 24, None, None)), getDateAMJNR((lAnnee, 7, 25, None, None)), getDateAMJNR((lAnnee, 7, 26, None, None)), getDateAMJNR((lAnnee, 7, 27, None, None)),
        getDateAMJNR((lAnnee, 7, 28, None, None)), getDateAMJNR((lAnnee, 7, 29, None, None)), getDateAMJNR((lAnnee, 7, 30, None, None)), getDateAMJNR((lAnnee, 7, 31, None, None)),
        getDateAMJNR((lAnnee, 8, 1, None, None)), getDateAMJNR((lAnnee, 8, 2, None, None)), getDateAMJNR((lAnnee, 8, 3, None, None)), getDateAMJNR((lAnnee, 8, 4, None, None)),
        getDateAMJNR((lAnnee, 8, 5, None, None)), getDateAMJNR((lAnnee, 8, 6, None, None)), getDateAMJNR((lAnnee, 8, 7, None, None)), getDateAMJNR((lAnnee, 8, 8, None, None)),
        getDateAMJNR((lAnnee, 8, 9, None, None)), getDateAMJNR((lAnnee, 8, 10, None, None)), getDateAMJNR((lAnnee, 8, 11, None, None)), getDateAMJNR((lAnnee, 8, 12, None, None)),
        getDateAMJNR((lAnnee, 8, 13, None, None)), getDateAMJNR((lAnnee, 8, 14, None, None)), getDateAMJNR((lAnnee, 8, 15, None, None)), getDateAMJNR((lAnnee, 8, 16, None, None)),
        getDateAMJNR((lAnnee, 8, 17, None, None)), getDateAMJNR((lAnnee, 8, 18, None, None)), getDateAMJNR((lAnnee, 8, 19, None, None)), getDateAMJNR((lAnnee, 8, 20, None, None))]
       ],
      ["Du 9 au 23 juin (fermé le 14 juin 2006 à 14h)",
       []],
      ["Du 4 juin au 12 juillet du lundi au dimanche de 14h à 18h, sauf le 1er mardi du mois et les jours fériés",
       [[None, None, None, 1, 1]]],
    ]
    for lTest, lResult in lTestFermeture :
      lGetResult = getJoursFermes(lTest)
      print( "Vérification de getJoursFermes(\"%s\")=%s"%(lTest, lGetResult))
      print( "Résultat attendu %s" %lResult)
      assert(lGetResult == lResult)

def checkDates(pDates) :
    """ check date integrity"""
    lIndex = 0
    #Contrôle la cohérences des dates et l'ordre chronologique de celle-ci
    try :
      lOldTime = None
      for lDate in pDates :
        lIndex = lIndex + 1
#        lTime = time.strptime("%d-%d-%d"%(lDate[ANNEE], lDate[MOIS], lDate[JOUR]), "%Y-%m-%d")
        if lOldTime and lDate < lOldTime :
          raise AttributeError("Les dates doivent être dans l'ordre chronologique", pDates)
        lOldTime = lDate
    except ValueError :
      if lIndex == 1 :
        raise AttributeError("La première date donnée n'est pas cohérente", pDates)
      else :
        raise AttributeError("La %dème date donnée n'est pas cohérente" % lIndex, pDates)
    return pDates


def getLeOuLes(pPhrase):
    """Retourne la date de fin ou la chaîne d'erreur"""
    # vérifie la syntaxe
    lMTokenLe = gTokenLe.match(pPhrase)
    lMTokenLes = gTokenLes.match(pPhrase)
    if not lMTokenLe and not lMTokenLes :
        return None
    lIndex = lMTokenLe and lMTokenLe.end() or lMTokenLes.end()
    lResult = getExpDateJourSeances(pPhrase[lIndex:])
    if not lResult :
      if lMTokenLe :
        raise AttributeError("Seule la partie \"Le \" est correcte", pPhrase)
      else :
        raise AttributeError("Seule la partie \"Les \" est correcte", pPhrase)
    lDeb, lFin, lReg = lResult[1][0]
    if lDeb != 0 :
      if lMTokenLe :
        raise AttributeError("Seule la partie \"Le \" est correcte", pPhrase)
      else :
        raise AttributeError("Seule la partie \"Les \" est correcte", pPhrase)
    lOldFin = lFin
    for lDeb, lFin, lReg in lResult[1][1:] :
      lToken = pPhrase[lIndex + lOldFin : lIndex + lDeb]
      if not gTokenLeOuLesEt.match(lToken) :
         raise AttributeError("Seule la partie \"%s\" a été reconnue" % pPhrase[:lIndex + lOldFin], pPhrase)
      lOldFin = lFin
    # transforme et vérifie les dates
    lDates = lResult[0]
    # si Les on vérifie qu'on a bien plusieurs dates
    if lMTokenLes and len(lDates) <= 1:
      raise AttributeError("Si vous utilisez \"Les\" veuillez alors indiquer plusieurs dates", pPhrase)
    lAnnee = getLocalTime()[0]
    lMois = None
    lSeances = None
    #Fixe les annees
    for lIndex in range(0, len(lDates)) :
      if lDates[lIndex][ANNEE] :
        lAnnee = lDates[lIndex][ANNEE]
        if lIndex > 0 :
          # remonte la liste des dates pour fixer l'année
          for lPos in [lIndex - 1 - x for x in range(0, lIndex)] :
            if lDates[lPos][ANNEE] :
              break;
            else :
              lDates[lPos][ANNEE] = lAnnee
    #Fixe l'année des dernières dates de la liste n'ayant pas d'année
    if not lDates[len(lDates) - 1][ANNEE] :
      for lPos in [len(lDates) - 1 - x for x in range(0, len(lDates))] :
        if lDates[lPos][ANNEE] :
          break;
        else :
          lDates[lPos][ANNEE] = lAnnee
    #Fixe les mois
    for lIndex in range(0, len(lDates)) :
      if lDates[lIndex][MOIS] :
        # remonte la liste des dates pour fixer le mois
        lMois = lDates[lIndex][MOIS]
        if lIndex > 0 :
          for lPos in [lIndex - 1 - x for x in range(0, lIndex)] :
            if lDates[lPos][MOIS] :
              break;
            else :
              lDates[lPos][MOIS] = lMois
    #Fixe le mois des dernières dates de la liste n'ayant pas de mois
    if not lMois :
        raise AttributeError("Vous devez donner le mois de votre événement", pPhrase)
    if not lDates[len(lDates) - 1][MOIS] :
      for lPos in [len(lDates) - 1 - x for x in range(0, len(lDates))] :
        if lDates[lPos][MOIS] :
          break;
        else :
          lDates[lPos][MOIS] = lMois
    #fixe les séances
    for lIndex in range(0, len(lDates)) :
      if lDates[lIndex][SEANCES] :
        # remonte la liste des dates pour fixer le mois
        lSeances = lDates[lIndex][SEANCES]
        if lIndex > 0 :
          for lPos in [lIndex - 1 - x for x in range(0, lIndex)] :
            if lDates[lPos][SEANCES] :
              break;
            else :
              lDates[lPos][SEANCES] = lSeances
    #Fixe les seances des dernières dates de la liste n'ayant pas de séances
    if not lDates[len(lDates) - 1][SEANCES] :
      for lPos in [len(lDates) - 1 - x for x in range(0, len(lDates))] :
        if lDates[lPos][SEANCES] :
          break;
        else :
          lDates[lPos][SEANCES] = lSeances
    #Contrôle la cohérences des dates et l'ordre chronologique de celle-ci
    return checkDates(lDates)

def getDuAu(pPhrase):
    """Retourne la date de fin ou la chaîne d'erreur"""
    # vérifie la syntaxe
    lMTokenDuAu = gTokenDuAu.match(pPhrase)
    if not lMTokenDuAu :
        return None
    lIndex = lMTokenDuAu.end()
    lSubPhrase = pPhrase[lIndex:]
    lResult = getExpDateJourSeances(lSubPhrase)
    if not lResult :
      raise AttributeError("Seule la partie \"Du \" est correcte", pPhrase)
    lDeb, lFin, lReg = lResult[1][0]
    if lDeb != 0 :
      raise AttributeError("Seule la partie \"Du \" est correcte", pPhrase)
    lOldFin = lFin
    #vérifie que l'on a bien au moins 2 dates et que les deux premières sont séparées par "au"
    if not (len(lResult[0]) >= 2 and gTokenDuAuAu.match(pPhrase[lIndex + lOldFin: lIndex + lResult[1][1][0]])) :
      raise AttributeError("La saisie doit contenir une date de début et une date de fin séparées par \" au \"", pPhrase)
    lOldFin = lResult[1][1][1]
    lSeparateurs = lResult[1][2:]

    for lDeb, lFin, lReg in lSeparateurs :
      lToken = lSubPhrase[lOldFin : lDeb]
      if not gTokenDuAuRDV.match(lToken) \
          and not gTokenJusquAuTousLes.match(lToken) and not gTokenJusquAuVirgule.match(lToken)\
          and not gExpFermeture.match(lToken) and not gExpTousSaufDeb.match(lToken)\
          and not gExpTousSaufNomJourDeb.match(lToken) and not gExpTousLesMatinsMidisSoirs.match(lToken)\
          and not gTokenLeOuLesEt.match(lToken) and not gExpFermeture.match(lToken)\
          and not gExpFermetureNomDuAu.match(lToken) :
          raise AttributeError("Seule la partie \"%s\" a été reconnue" % pPhrase[:lIndex + lOldFin], pPhrase)
      lOldFin = lFin

    if lOldFin != len(lSubPhrase) :
      lToken =lSubPhrase[lOldFin:]
      if not gTokenDuAuRDV.match(lToken) \
          and not gTokenJusquAuTousLes.match(lToken) and not gTokenJusquAuVirgule.match(lToken)\
          and not gExpFermeture.match(lToken) and not gExpTousSaufDeb.match(lToken)\
          and not gExpTousSaufNomJourDeb.match(lToken) and not gExpTousLesMatinsMidisSoirs.match(lToken)\
          and not gTokenLeOuLesEt.match(lToken) and not gExpFermeture.match(lToken)\
          and not gExpFermetureNomDuAu.match(lToken) :
          raise AttributeError("Seule la partie \"%s\" a été reconnue" % pPhrase[:lIndex + lOldFin], pPhrase)
    # transforme et vérifie les dates
    lDates = lResult[0]
    lAnnee = lDates[0][ANNEE] or lDates[1][ANNEE] or getLocalTime()[0]
    lMois = lDates[0][MOIS] or lDates[1][MOIS]
    lSeances = lDates[0][SEANCES] or lDates[1][SEANCES]
    if not lMois :
        raise AttributeError("Vous devez donner le mois de votre événement", pPhrase)
    if not lDates[0][ANNEE] :
      lDates[0][ANNEE] = lAnnee
    if not lDates[0][MOIS] :
      lDates[0][MOIS] = lMois
    if not lDates[0][SEANCES] :
      lDates[0][SEANCES] = lSeances
    if not lDates[1][ANNEE] :
      lDates[1][ANNEE] = lAnnee
    if not lDates[1][MOIS] :
      lDates[1][MOIS] = lMois
    if not lDates[1][SEANCES] :
      lDates[1][SEANCES] = lSeances
    #Contrôle la cohérences des dates et l'ordre chronologique de celle-ci
    return checkDates(lDates[0:2])

def getDatesFromSeances(pPhrase) :
  lDates = getJusquAu(pPhrase) or \
           getLeOuLes(pPhrase) or  \
           getDuAu(pPhrase)
  return lDates


def getDatesFromPeriode(pDateDebut, pDateFin, pDatesASupprimer = None) :
    """Retourne la liste des dates d'une periode en excluant les dates de pDatesASupprimer.
       Si pDateDebut est None nous calculont les dates à partire de maintenant.
       Les dates à supprimer sont sous la forme liste de liste [Annee, Mois, Jour, IndiceNomJour, RangJour]"""
    def notInASupprimer(pDate) :
      lJour = [None, None, None, pDate[3], None]
      lJourRang = [None, None, None, pDate[3], pDate[4]]
      if pDatesASupprimer.count(pDate) or pDatesASupprimer.count(lJour) or pDatesASupprimer.count(lJourRang):
        return False
      return True
    lDateDebut = None
    lDateFin = None
    if not pDateFin :
       raise AttributeError("Vous devez donner la date de fin de période")
    lDateDebut = getDateAMJNR(pDateDebut and pDateDebut[:3] or None)
    lDateFin = getDateAMJNR(pDateFin[:3])

    if lDateFin < lDateDebut :
       raise AttributeError("Les dates doivent être dans l'ordre croissant, si vos dates sont sur des années différentes veuillez donner la date complète")
    lDates = []
    lDates.append(lDateDebut)
    lDate = incJour(lDateDebut)
    while lDate < lDateFin :
      if pDatesASupprimer and notInASupprimer(lDate) or not pDatesASupprimer :
        lDates.append(lDate)
      lDate = incJour(lDate)
    lDates.append(lDateFin)
    return lDates

if __name__ == '__main__' :
    #Test unitaire
    def getDate(pDebut, pFin) :
        lDebut = getDateAMJNR(pDebut)
        lFin = getDateAMJNR(pFin)
        lDates = []
        lDates.append(lDebut)
        lDate = incJour(pDebut)
        while lDate < lFin :
          lDates.append(lDate)
          lDate = incJour(lDate)
        lDates.append(lFin)
    lAnnee = getLocalTime()[0]
    lTestDatesFromPeriode = [
      ["Jusqu'au 1er décembre, tous les soirs à 20h30, le 25 juin à 15h30, relâche les lundis et dimanches",
       None
       ],
      ["Du 14 juin au 21 juillet du lundi au dimanche de 14h à 18h, sauf le mardi et les jours fériés", #@TODO tester bug du mardi
       [[2006, 6, 14, 2, 2], [2006, 6, 15, 3, 3], [2006, 6, 16, 4, 3], [2006, 6, 17, 5, 3], [2006, 6, 18, 6, 3],
        [2006, 6, 19, 0, 3], [2006, 6, 21, 2, 3], [2006, 6, 22, 3, 4], [2006, 6, 23, 4, 4], [2006, 6, 24, 5, 4],
        [2006, 6, 25, 6, 4], [2006, 6, 26, 0, 4], [2006, 6, 28, 2, 4], [2006, 6, 29, 3, 5], [2006, 6, 30, 4, 5],
        [2006, 7, 1, 5, 1], [2006, 7, 2, 6, 1], [2006, 7, 3, 0, 1], [2006, 7, 5, 2, 1], [2006, 7, 6, 3, 1],
        [2006, 7, 7, 4, 1], [2006, 7, 8, 5, 2], [2006, 7, 9, 6, 2], [2006, 7, 10, 0, 2], [2006, 7, 12, 2, 2],
        [2006, 7, 13, 3, 2], [2006, 7, 14, 4, 2], [2006, 7, 15, 5, 3], [2006, 7, 16, 6, 3], [2006, 7, 17, 0, 3],
        [2006, 7, 19, 2, 3], [2006, 7, 20, 3, 3], [2006, 7, 21, 4, 3]]],
      ["Du 25 mai au 9 juillet tous les jours sauf le lundi, mercredi, jeudi et samedi",
        [[2006, 5, 25, 3, 4], [2006, 5, 26, 4, 4], [2006, 5, 28, 6, 4], [2006, 5, 30, 1, 5], [2006, 6, 2, 4, 1],
         [2006, 6, 4, 6, 1], [2006, 6, 6, 1, 1], [2006, 6, 9, 4, 2], [2006, 6, 11, 6, 2], [2006, 6, 13, 1, 2],
         [2006, 6, 16, 4, 3], [2006, 6, 18, 6, 3], [2006, 6, 20, 1, 3], [2006, 6, 23, 4, 4], [2006, 6, 25, 6, 4],
         [2006, 6, 27, 1, 4], [2006, 6, 30, 4, 5], [2006, 7, 2, 6, 1], [2006, 7, 4, 1, 1], [2006, 7, 7, 4, 1],
         [2006, 7, 9, 6, 2]]],
      ["Du 3 janvier au 14 janvier 2007 tous les jours sauf le mardi, le samedi, et le dimanche",
       [[2007, 1, 3, 2, 1], [2007, 1, 4, 3, 1], [2007, 1, 5, 4, 1], [2007, 1, 8, 0, 2], [2007, 1, 10, 2, 2],
        [2007, 1, 11, 3, 2], [2007, 1, 12, 4, 2], [2007, 1, 14, 6, 2]]],
      ["Du 20 juin au 26 juillet du mardi au samedi de 14h à 18h (fermé les jours fériés)",
       [[2006, 6, 20, 1, 3], [2006, 6, 21, 2, 3], [2006, 6, 22, 3, 4], [2006, 6, 23, 4, 4],
        [2006, 6, 24, 5, 4], [2006, 6, 27, 1, 4], [2006, 6, 28, 2, 4], [2006, 6, 29, 3, 5],
        [2006, 6, 30, 4, 5], [2006, 7, 1, 5, 1], [2006, 7, 4, 1, 1], [2006, 7, 5, 2, 1], [2006, 7, 6, 3, 1],
        [2006, 7, 7, 4, 1], [2006, 7, 8, 5, 2], [2006, 7, 11, 1, 2], [2006, 7, 12, 2, 2], [2006, 7, 13, 3, 2],
        [2006, 7, 14, 4, 2], [2006, 7, 15, 5, 3], [2006, 7, 18, 1, 3], [2006, 7, 19, 2, 3], [2006, 7, 20, 3, 3],
        [2006, 7, 21, 4, 3], [2006, 7, 22, 5, 4], [2006, 7, 25, 1, 4], [2006, 7, 26, 2, 4]]],
      ["Du 7 au 30 juin (fermé le lundi)",
       [[2006, 6, 7, 2, 1], [2006, 6, 8, 3, 2], [2006, 6, 9, 4, 2], [2006, 6, 10, 5, 2], [2006, 6, 11, 6, 2],
        [2006, 6, 13, 1, 2], [2006, 6, 14, 2, 2], [2006, 6, 15, 3, 3], [2006, 6, 16, 4, 3], [2006, 6, 17, 5, 3],
        [2006, 6, 18, 6, 3], [2006, 6, 20, 1, 3], [2006, 6, 21, 2, 3], [2006, 6, 22, 3, 4], [2006, 6, 23, 4, 4],
        [2006, 6, 24, 5, 4], [2006, 6, 25, 6, 4], [2006, 6, 27, 1, 4], [2006, 6, 28, 2, 4], [2006, 6, 29, 3, 5],
        [2006, 6, 30, 4, 5]]],
      ["Du 17 au 23 juin (fermé du lundi au mercredi)",
       [[2006, 6, 17, 5, 3], [2006, 6, 18, 6, 3], [2006, 6, 22, 3, 4], [2006, 6, 23, 4, 4]]],
      ["Du 7 au 13 juin (fermé du jeudi au mardi)",
       [[2006, 6, 7, 2, 1], [2006, 6, 13, 1, 2]]], #ici nous avons un conflit entre la dernière date et le jour de fermeture
      ["Du 15 au 23 juin (fermé du vendredi au mercredi)",
       [[2006, 6, 15, 3, 3], [2006, 6, 22, 3, 4], [2006, 6, 23, 4, 4]]],
      ["Du 1er juin au 3 août (fermé du 1er lundi au 3ème mercredi)",
       [[2006, 6, 1, 3, 1], [2006, 6, 15, 3, 3], [2006, 6, 16, 4, 3], [2006, 6, 17, 5, 3], [2006, 6, 18, 6, 3],
        [2006, 6, 22, 3, 4], [2006, 6, 23, 4, 4], [2006, 6, 24, 5, 4], [2006, 6, 25, 6, 4], [2006, 6, 26, 0, 4],
        [2006, 6, 27, 1, 4], [2006, 6, 28, 2, 4], [2006, 6, 29, 3, 5], [2006, 6, 30, 4, 5], [2006, 7, 15, 5, 3],
        [2006, 7, 16, 6, 3], [2006, 7, 20, 3, 3], [2006, 7, 21, 4, 3], [2006, 7, 22, 5, 4], [2006, 7, 23, 6, 4],
        [2006, 7, 24, 0, 4], [2006, 7, 25, 1, 4], [2006, 7, 26, 2, 4], [2006, 7, 27, 3, 4], [2006, 7, 28, 4, 4],
        [2006, 7, 29, 5, 5], [2006, 7, 30, 6, 5], [2006, 7, 31, 0, 5], [2006, 8, 3, 3, 1]]],
      ["Du 5 juillet au 1er septembre du mardi au vendredi de 9h à 12h et de 14h à 18h, le lundi de 15h à 18h, les 10, 17 et 24 juin de 9h à 12h et de 15h à 15h30 (fermeture du 24 juillet au 20 août)",
        [[2006, 7, 5, 2, 1], [2006, 7, 6, 3, 1], [2006, 7, 7, 4, 1], [2006, 7, 10, 0, 2], [2006, 7, 11, 1, 2],
         [2006, 7, 12, 2, 2], [2006, 7, 13, 3, 2], [2006, 7, 14, 4, 2], [2006, 7, 17, 0, 3], [2006, 7, 18, 1, 3],
         [2006, 7, 19, 2, 3], [2006, 7, 20, 3, 3], [2006, 7, 21, 4, 3], [2006, 8, 21, 0, 3], [2006, 8, 22, 1, 4],
         [2006, 8, 23, 2, 4], [2006, 8, 24, 3, 4], [2006, 8, 25, 4, 4], [2006, 8, 28, 0, 4], [2006, 8, 29, 1, 5],
         [2006, 8, 30, 2, 5], [2006, 8, 31, 3, 5], [2006, 9, 1, 4, 1]]],
      ["Du 4 juin au 12 juillet du lundi au dimanche de 14h à 18h, sauf le 1er mardi du mois et les jours fériés",
       [[2006, 6, 4, 6, 1], [2006, 6, 5, 0, 1], [2006, 6, 7, 2, 1], [2006, 6, 8, 3, 2], [2006, 6, 9, 4, 2],
        [2006, 6, 10, 5, 2], [2006, 6, 11, 6, 2], [2006, 6, 12, 0, 2], [2006, 6, 13, 1, 2], [2006, 6, 14, 2, 2],
        [2006, 6, 15, 3, 3], [2006, 6, 16, 4, 3], [2006, 6, 17, 5, 3], [2006, 6, 18, 6, 3], [2006, 6, 19, 0, 3],
        [2006, 6, 20, 1, 3], [2006, 6, 21, 2, 3], [2006, 6, 22, 3, 4], [2006, 6, 23, 4, 4], [2006, 6, 24, 5, 4],
        [2006, 6, 25, 6, 4], [2006, 6, 26, 0, 4], [2006, 6, 27, 1, 4], [2006, 6, 28, 2, 4], [2006, 6, 29, 3, 5],
        [2006, 6, 30, 4, 5], [2006, 7, 1, 5, 1], [2006, 7, 2, 6, 1], [2006, 7, 3, 0, 1], [2006, 7, 5, 2, 1],
        [2006, 7, 6, 3, 1], [2006, 7, 7, 4, 1], [2006, 7, 8, 5, 2], [2006, 7, 9, 6, 2], [2006, 7, 10, 0, 2],
        [2006, 7, 11, 1, 2], [2006, 7, 12, 2, 2]]],
     ["Du 1er septembre au 1er décembre",getDate([getLocalTime()[0], 9, 1, 0, 0], [getLocalTime()[0], 12, 1, 0, 0])],
#     ["Du 1er octobre au 30 novembre de 9h à 12h, le weekend de 9h à 12h et de 14h à 18h, fermé le lundi",
#        [[None, 10, 1, []], [None, 11, 30, [[[9, None], [12, None]], [[14, None], [18, None]]]]]],
    ]
    for lTest, lResult in lTestDatesFromPeriode :
     try:
      lDates = getDatesFromSeances(lTest)
      lJoursFermes = getJoursFermes(lTest)
      lGetResult = getDatesFromPeriode(lDates[0], lDates[1], lJoursFermes)
      print( "Vérification de getDatesFromPeriode(\"%s\")=%s"%(lTest, lGetResult))
      print( "Résultat attendu %s" %lResult)
      if lResult != None :
        assert(lGetResult == lResult)
     except :
      print( lTest)
      raise

def getSeancesFromDate(pDate, pPhrase, pChamps = [JOUR, MOIS, ANNEE, SEANCES]) :
  """ Donne la séances d'une date"""
  def getSeance(pDates) :
    lStr = ""
    if pDates :
      lIndex = 0
      lLast = len(pDates) - 1
      for lDate in pDates :
        if lIndex == lLast and lIndex >= 1 :
          lStr = lStr + " et "
        elif lIndex != lLast and lIndex > 0:
          lStr = lStr + ", "
        if lDate[0] and not lDate[1] :
          lStr = "à %dh%s" % (lDate[0][0], lDate[0][1] or '')
        elif lDate[0] and lDate[1] :
          lStr = "de %dh%s à %dh%s" % (lDate[0][0], lDate[0][1] or '', lDate[1][0], lDate[1][1] or '')
        elif not lDate[0] and lDate[1] :
          lStr = "jusqu'à %dh%s" % (lDate[1][0], lDate[1][1] or '')
        lIndex = lIndex + 1
    return lStr

  lLeOuLes = gTokenLe.match(pPhrase) or gTokenLes.match(pPhrase)
  lJusquAu = gTokenJusquAu.match(pPhrase)
  lDuAu = gTokenDuAu.match(pPhrase)
  if lJusquAu or lDuAu :
    return pPhrase
  elif lLeOuLes :
    lSeances = "Le "
    if pChamps.count(JOUR) :
      lSeances = lSeances + " %d"%pDate[JOUR]
    if pChamps.count(MOIS) :
      lSeances = lSeances + " %s"%ENM_ValeursMois[pDate[MOIS] - 1]
    if pChamps.count(ANNEE) :
      lSeances = lSeances + " %s"%pDate[ANNEE]
    if pChamps.count(SEANCES) :
      lSeances = lSeances + " %s"%getSeance(pDate[SEANCES])
    return lSeances


if __name__ == '__main__' :
    #Test unitaire
    print( "Verification de getExpDateJourSeances")
    lTestJusquAu =[
      ["Jusqu'au 1er juillet, tous les soirs à 20h30, le 25 juin à 15h30, relâche les lundis et dimanches", [[None, 7, 1, [[[20, 30], None]]], [None, 6, 25, [[[15, 30], None]]]]],
      ["Jusqu'au 31 août", [[None, 8, 31, []]]],
      ["Jusqu'au 2 janvier 2007 à 20h", [[2007, 1, 2, [[[20, None], None]]]]],
      ["Jusqu'au 11 décembre", [[None, 12, 11, []]]],
      ["Jusqu'au 28 février tous les midis", [[None, 2, 28, []]]],
      ["Jusqu'au 19 août à 20h", [[None, 8, 19, [[[20, None], None]]]]],
     ]
    lTestLe = [
      ["Le 1er janvier à 18h", [[None, 1, 1, [[[18, None], None]]]]],
      ["Le 28 février à partir de 18h", [[None, 2, 28, [[[18, None], None]]]]],
      ["Le 3 mars à partir de 20h", [[None, 3, 3, [[[20, None], None]]]]],
      ["Le 22 juin à 15h30 et le 23 juin à 20h30", [[None, 6, 22, [[[15, 30], None]]], [None, 6, 23, [[[20, 30], None]]]]],
      ["Le 25 juin à 15h30 et le 26 juin à 10h30, à 16h11 et à 22h", [[None, 6, 25, [[[15, 30], None]]], [None, 6, 26, [[[10, 30], None],[[16, 11], None],[[22, None], None]]]]],
      ["Le 22 juillet de 21h30 jusqu'à plus soif", [[None, 7, 22, [[[21, 30], None]]]]],
      ["Le 23 août de 11h30 jusqu'à l'aube", [[None, 8, 23, [[[11, 30], None]]]]],
      ["Le 24 septembre de 21h30 à 23h", [[None, 9, 24, [[[21, 30], [23, None]]]]]],
      ["Le 25 octobre départ à 14h53", [[None, 10, 25, [[[14, 53], None]]]]],
      ["Le 26 novembre dès 12h", [[None, 11, 26, [[[12, None], None]]]]],
      ["Le 9 décembre à 12h, 14 décembre à 19h et le 15 décembre à 18h",
       [[None, 12, 9, [[[12, None], None]]], [None, 12, 14, [[[19, None], None]]], [None, 12, 15, [[[18, None], None]]]]],
      ["Le 12 janvier à 12h, le 13 juin à 15h et le 14 juin à 18h",
       [[None, 1, 12, [[[12, None], None]]], [None, 6, 13, [[[15, None], None]]], [None, 6, 14, [[[18, None], None]]]]],
      ["Le 4 mai à 12h, le 13 juin à 15h et le 14 juin à 18h",
       [[None, 5, 4, [[[12, None], None]]], [None, 6, 13, [[[15, None], None]]], [None, 6, 14, [[[18, None], None]]]]],
      ["Le 31 décembre 2006 à 12h, le 13 janvier 2007 à 15h et le 14 juin 2007 à 18h",
       [[2006, 12, 31, [[[12, None], None]]], [2007, 1, 13, [[[15, None], None]]], [2007, 6, 14, [[[18, None], None]]]]],
      ["Le 19 avril à 10h30, 14h30 et 16h30 et le 20 avril à 14h30 et 16h30",
       [[None, 4, 19, [[[10, 30], None], [[14, 30], None], [[16, 30], None]]], [None, 4, 20, [[[14, 30], None], [[16, 30], None]]]]],
      ["Le 18 à 13h, le 19 de 16h à 17h, le 20 de 10h à 12h et de 14h à 17h, et le 21 juin 2006 à 11h, 12h, 13h et 14h et le 1er janvier 2007 à 1h",
       [[None, None, 18, [[[13, None], None]]], [None, None, 19, [[[16, None], [17, None]]]], [None, None, 20, [[[10, None], [12, None]],[[14, None], [17, None]]]], [2006, 6, 21, [[[11, None], None], [[12, None], None], [[13, None], None], [[14, None], None]]], [2007, 1, 1, [[[1, None], None]]]]],
    ]
    lTestLes = [
      ["Les 23, 24 à 20h30 et 25 juin à 17h",
       [[None, None, 23, []], [None, None, 24, [[[20, 30], None]]], [None, 6, 25, [[[17, None], None]]]]],
      ["Les 23, 24 juin à 20h30 et 25 juin à 17h",
       [[None, None, 23, []], [None, 6, 24, [[[20, 30], None]]], [None, 6, 25, [[[17, None], None]]]]],
      ["Les 30 juin et 1er juillet à 20h30",
       [[None, 6, 30, []], [None, 7, 1, [[[20, 30], None]]]]],
      ["Les 21, 22, 23, 28 et 29 juin de 20h à 22h",
       [[None, None, 21, []], [None, None, 22, []], [None, None, 23, []], [None, None, 28, []], [None, 6, 29, [[[20, None], [22, None]]]]]],
      ["Les 28, 29, 30 juin et 1er juillet à 20h30",
       [[None, None, 28, []], [None, None, 29, []], [None, 6, 30, []], [None, 7, 1, [[[20, 30], None]]]]],
      ["Les 28, 29, 30 juin et le 1er juillet à 20h30",
       [[None, None, 28, []], [None, None, 29, []], [None, 6, 30, []], [None, 7, 1, [[[20, 30], None]]]]],
      ["Les 12 à 15h, 13 à 20h30, 16 et 17 février à 15h",
       [[None, None, 12, [[[15, None], None]]], [None, None, 13, [[[20, 30], None]]], [None, None, 16, []], [None, 2, 17, [[[15, None], None]]]]],
      ["Les 12 à 15h, 13 à 20h30, 16 et 17 juillet à 15h",
       [[None, None, 12, [[[15, None], None]]], [None, None, 13, [[[20, 30], None]]], [None, None, 16, []], [None, 7, 17, [[[15, None], None]]]]],
      ["Les 19, 26 juillet et le 2 août à 20h",
       [[None, None, 19, []], [None, 7, 26, []], [None, 8, 2, [[[20, None], None]]]]],
      ["Les 28, 29, 30 juin et les 1er, 2, 3, 4 juillet à 20h30",
       [[None, None, 28, []], [None, None, 29, []], [None, 6, 30, []], [None, None, 1, []], [None, None, 2, []], [None, None, 3, []], [None, 7, 4, [[[20, 30], None]]]]],
    ]
    lTestDuAu = [
      ["Du 23 au 29 juin", [[None, None, 23, []], [None, 6, 29, []]]],
#      ["Du mardi au samedi soir à 22h", False],
      ["Du 28 janvier 2006 au 14 septembre 2007", [[2006, 1, 28, []], [2007, 9, 14, []]]],
      ["Du 3 mars au 3 septembre", [[None, 3, 3, []], [None, 9, 3, []]]],
      ["Du 5 au 11 août à 14h30", [[None, None, 5, []], [None, 8, 11, [[[14, 30], None]]]]],
      ["Du 5 mai au 25 juin du mardi au vendredi de 9h à 17h, les samedis et dimanches de 14h à 18h",
        [[None, 5, 5, []], [None, 6, 25, [[[9, None], [17, None]], [[14, None], [18, None]]]]]],
      ["Du 14 juin au 21 juillet du lundi au dimanche de 14h à 18h, sauf le mardi et les jours fériés",
        [[None, 6, 14, []], [None, 7, 21, [[[14, None], [18, None]]]]]],
      ["Du 25 mai au 9 juillet tous les jours sauf le lundi de 11h à 18h", [[None, 5, 25, []], [None, 7, 9, []]]],
      ["Du 1er au 30 juin du lundi au vendredi de 8h à 12h et de 14h à 18h, le samedi de 14h à 18h",
        [[None, None, 1, []], [None, 6, 30, [[[8, None], [12, None]], [[14, None], [18, None]], [[14, None], [18, None]]]]]],
      ["Du 3 janvier au 14 janvier 2007 tous les jours sauf mardi de 10h à 12h et de 14h à 17h30, le samedi jusqu'à 18h30, le dimanche de 14h à 18h30",
        [[None, 1, 3, []], [2007, 1, 14, []]]],
      ["Du 2 juin 2006 au 14 janvier 2007 les lundis, mercredis, jeudis et vendredis de 10h à 12h et de 14h à 17h30, le samedi jusqu'à 18h30, le dimanche de 14h à 18h30",
        [[2006, 6, 2, []], [2007, 1, 14, [[[10, None], [12, None]], [[14, None], [17, 30]], [[14, None], [18, 30]], [None, [18, 30]]]]]],
      ["Du 1er au 30 juin les jeudis, vendredis et samedis de 15h à 19h et sur RDV",
        [[None, None, 1, []], [None, 6, 30, [[[15, None], [19, None]]]]]],
      ["Du 20 juin au 26 juillet du mardi au samedi de 14h à 18h (fermé les jours fériés)",
        [[None, 6, 20, []], [None, 7, 26, [[[14, None], [18, None]]]]]],
      ["Du 7 au 30 juin (fermé le lundi)", [[None, None, 7, []], [None, 6, 30, []]]],
      ["Du 5 juin au 1er septembre du mardi au vendredi de 9h à 12h et de 14h à 18h, le lundi de 15h à 18h, les 10, 17 et 24 juin de 9h à 12h et de 15h à 15h30 (fermeture du 24 juillet au 20 août)",
        [[None, 6, 5, []], [None, 9, 1, [[[9, None], [12, None]], [[14, None], [18, None]], [[15, None], [18, None]]]], [None, None, 10, []], [None, None, 17, []], [None, 6, 24, [[[9, None], [12, None]], [[15, None], [15, 30]]]]]],
#      ["Du 1er septembre au 30 octobre de 9h à 12h et de 14h à 18h le week-end, fermé le lundi",
#        [[None, 9, 1, []], [None, 10, 30, [[[9, None], [12, None]], [[14, None], [18, None]]]]]],
      ["Du 1er septembre au 30 octobre de 9h à 12h, le week-end de 9h à 12h et de 14h à 18h, fermé le lundi",
        [[None, 9, 1, []], [None, 10, 30, [[[9, None], [12, None]], [[9, None], [12, None]], [[14, None], [18, None]]]]]],
    ]
    lTestErreursJusquAu = [
      ["Jusqu'au 1 septembre les lundis et mardi", None],
      ["Jusqu'au 1er septembre les lu ndis et mardi", None],
    ]
    lTestErreursLe = [
      ["Le 11er janvier à 18h", None],
      ["Le 29 février à partir de 18h", None],
    ]
    lTestErreursLes = [
      ["Les 25, 24 à 20h30 et 25 juin à 17h",None],
      ["Les 32, 24 juin à 20h30 et 25 juin à 17h",None],
      ["Les 3, 12 juillet à 20h30 et 25 juin à 17h",None],
      ["Les 30 juin 2006 et 1er juillet 2005 à 20h30", None],
    ]
    lTestErreursDuAu = [
       ["Du 7 au 32 juin (fermé le lundi)", None],
      ["Du 35 juin au 11er septembre du mardi au vendredi de 9h à 12h et de 14h à 18h, le lundi de 15h à 18h, les 10, 17 et 24 juin de 9h à 12h et de 15h à 15h30 (fermeture du 24 juillet au 20 août)",
        None],
    ]
    lTests = lTestJusquAu + lTestLe + lTestLes + lTestDuAu
    TEST = True
    if TEST :
      for lTest, lExpectedResult in lTests :
        lResult = getExpDateJourSeances(lTest)
        print( "(\"%s\", %s), " % (lTest, lResult[0]))
        if lExpectedResult :
          assert(lExpectedResult == lResult[0])
        else :
          warnings.warn("@TODO implementer le test")
    for lTest in lTestJusquAu :
        print( "(\"%s\", %s), " % (lTest[0], getJusquAu(lTest[0])))

    for lTest in lTestLe :
        print( "(\"%s\", %s), " % (lTest[0], getLeOuLes(lTest[0])))
    for lTest in lTestErreursJusquAu :
      try :
        print( "(\"%s\", %s), " % (lTest[0], getJusquAu(lTest[0])))
        raise "%s aurait du déclencher une erreur"%lTest[0]
      except AttributeError as pErr :
        pass
    for lTest in lTestErreursLe :
      try :
        print( "(\"%s\", %s), " % (lTest[0], getLeOuLes(lTest[0])))
        raise "%s aurait du déclencher une erreur"%lTest[0]
      except AttributeError as pErr :
        pass

    for lTest in lTestLes :
        print( "(\"%s\", %s), " % (lTest[0], getLeOuLes(lTest[0])))
    for lTest in lTestErreursLes :
      try :
        print( "(\"%s\", %s), " % (lTest[0], getLeOuLes(lTest[0])))
        raise "%s aurait du déclencher une erreur"%lTest[0]
      except AttributeError as pErr :
        pass

    for lTest in lTestDuAu :
        print( "(\"%s\", %s), " % (lTest[0], getDuAu(lTest[0])))
    for lTest in lTestErreursDuAu :
      try :
        print( "(\"%s\", %s), " % (lTest[0], getDuAu(lTest[0])))
        raise "%s aurait du déclencher une erreur"%lTest[0]
      except AttributeError as pErr :
        pass

#warnings.warn("@TODO vérifier la cohérence des heures avec matin midi soir après-midi avant exploitation")
