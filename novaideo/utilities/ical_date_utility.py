# -*- coding: utf8 -*-
# Copyright (c) 2015 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi, Sophie jazwiecki

import datetime
import pytz
from itertools import dropwhile, takewhile
import time
from plone.event.recurrence import recurrence_sequence_ical
from ..dateindex import int2dt, dt2int
from dace.util import find_catalog
from substanced.util import get_oid
#from creationculturelle.cache import region

from novaideo.utilities import french_dates_parser as Parser
from .memoize import memoize


def get_publication_periodic_date(site, event):
    ocur = occurences_start(
        event, 'dates', from_=datetime.datetime.now(tz=pytz.UTC))

    if ocur:
        site_publication_date = site.next_publication_date().replace(tzinfo=pytz.UTC)
        closing_frequence_delta = datetime.timedelta(
            days=getattr(site, 'closing_frequence', 0))
        site_end_publication = site_publication_date + closing_frequence_delta
        site_end_publication = site_end_publication.replace(tzinfo=pytz.UTC)
        while True:
            dates = occurences_from(site_publication_date, ocur)
            dates = list(occurences_until(site_end_publication, dates))
            if dates:
                return True, site_publication_date

            next_dates = list(occurences_from(site_end_publication, ocur))
            if not next_dates:
                dates = list(occurences_until(site_publication_date, ocur))
                end_date = None
                if dates:
                    end_date = dates[-1].replace(tzinfo=pytz.UTC)

                return False, end_date

            site_publication_date = site_end_publication
            site_end_publication = site_publication_date + closing_frequence_delta
            site_end_publication = site_end_publication.replace(tzinfo=pytz.UTC)

    return False, None


def get_end_date(ical_date):
    #TODO retourne la derniere date de la date ical et
    #none si la date est infinie.
    return None


def get_dates_in_period(ical_date, start_date, end_date):
    #TODO retourne la liste des dates entre start_date et end_date
    #qui sont dans la date ical.
    pass


@memoize
def getDatesFromString(context, dates_str):  # was getDatesFromSeances in old project
    """Return a list of datetime from parsed dates_str.
    """
    return Parser.getDatesFromSeances(dates_str)


def list_date_to_dates(l_date):
    dates = []
    date_key = ''.join([str(l_date[0]), str(l_date[1]), str(l_date[2])])
    if l_date[3]:
        l_time = [t for t in l_date[3]]
        for time_ in l_time:
            start_time = time_[0]
            end_time = time_[1]
            start_date_time = None
            if start_time:
                start_date_time = datetime.datetime(
                    *(l_date[0], l_date[1], l_date[2],
                      start_time[0] or 0, start_time[1] or 0, 0)).replace(tzinfo=pytz.UTC)
            else:
                start_date_time = datetime.datetime(
                    *(l_date[0], l_date[1], l_date[2],
                      0, 0, 0)).replace(tzinfo=pytz.UTC)

            end_date_time = None
            if end_time:
                end_date_time = datetime.datetime(
                    *(l_date[0], l_date[1], l_date[2],
                      end_time[0] or 0, end_time[1] or 0, 0)).replace(tzinfo=pytz.UTC)
            else:
                end_date_time = datetime.datetime(
                    *(l_date[0], l_date[1], l_date[2],
                      23, 59, 59)).replace(tzinfo=pytz.UTC)

            dates.append(dict(start=start_date_time, end=end_date_time))

    return (date_key, dates)


@memoize
def get_dates_intervals(context, dates_str):
    dates = getDatesFromString(context, dates_str)
    return dict([list_date_to_dates(d) for d in dates if d])


def set_recurrence(dates, dates_str):
    """Return iCal string from dates (list of list representing datetime)
    """
    if len(dates) >= 1 and (Parser.gTokenLe.match(dates_str) or\
       Parser.gTokenLes.match(dates_str)):
        rfcdates = []
        for l_date in dates:
            rfcdate = time.strftime("%Y%m%dT000000",
                (l_date[0], l_date[1], l_date[2], 0, 0, 0, 0, 0, 0))
            rfcdates.append(rfcdate)
        return "RDATE;VALUE=DATE-TIME:" + ",".join(rfcdates)
    elif len(dates) >= 1 and (Parser.gTokenJusquAu.match(dates_str) or\
         Parser.gTokenDuAu.match(dates_str)):
        l_jours_fermes = Parser.getJoursFermes(dates_str)
        date_debut = dates[0]
        date_fin = dates[1]
        # handle the case where we recatalog in june a date "Jusqu'au 20 mai"
        # getDatesFromPeriode raises an AttributeError if date_fin < date_debut
        # be careful, [2012, 1, 2] < (2011, 9, 25) is True!
        if date_debut is None and\
           tuple(date_fin[:3]) < tuple(time.localtime()[:3]):
            date_debut = date_fin
        # TODO instead of the following line, we should generate
        # the equivalent in ical rule
        l_dates_ouvertures = Parser.getDatesFromPeriode(
                              date_debut, date_fin, l_jours_fermes)
        rfcdates = []
        for l_date in l_dates_ouvertures:
            rfcdate = time.strftime("%Y%m%dT000000",
                (l_date[0], l_date[1], l_date[2], 0, 0, 0, 0, 0, 0))
            rfcdates.append(rfcdate)
        return "RDATE;VALUE=DATE-TIME:" + ",".join(rfcdates)


dates_mapping = {
    'dates_start_date': 'start_date'
}


def occurences_until(until, dates, is_ints=False):
    _until = until
    if is_ints:
        _until = until and dt2int(until) or None

    if _until is not None:
        results = takewhile(lambda x: x <= _until, dates)
        return results

    return dates


def occurences_from(from_, dates, is_ints=False):
    _from = from_
    if is_ints:
        _from = from_ and dt2int(from_) or None

    if _from is not None:
        results = dropwhile(lambda x: x < _from, dates)
        return results

    return dates

#@region.cache_on_arguments()
def occurences_start(obj, propertyname, from_=None, until=None,
                     hours=None, minutes=None):
    oid = get_oid(obj, None)
    if oid is not None:
        index = find_catalog('novaideo')[
            dates_mapping.get(
                propertyname + '_start_date',
                propertyname + '_start_date')]
        results = index._rev_index.get(oid, ())
        results = occurences_until(until, results, True)
        results = occurences_from(from_, results, True)
        results = [int2dt(d, hours, minutes) for d in results]
    else:
        start = getattr(obj, propertyname + '_start_date', None)
        recurrence = getattr(obj, propertyname + '_recurrence', '')
        if not recurrence:
            results = [start]
        else:
            results = list(recurrence_sequence_ical(start, recrule=recurrence,
                                                    from_=from_, until=until))
    return results


def getMiseAJourSeance(dates_str, start_date, end_date=None, context=None):
    """Donne l'expression de la séance mise à jour par rapport à pTimeDateDebut.
       Retourne le tuple NouvelleSeance, NBJourRestant (None si inconnu)"""
    if context:
        dates = getDatesFromString(context, dates_str)
    else:
        dates = Parser.getDatesFromSeances(dates_str)

    dates_len = len(dates)
    local_time_start_date = (start_date.year, start_date.month, start_date.day)
    if dates_str.startswith('Jusqu'):
        return dates_str, None

    if dates_str.startswith('Du') and \
       tuple(dates[0][:3]) < local_time_start_date:
        new_date_str = "Jusqu'" + dates_str[dates_str.find("au"):]
        return new_date_str, None

    if dates_len == 1:
        return dates_str, 1

    index = 0
    for date in dates:
        if date and tuple(date[:3]) >= local_time_start_date:
            break

        index += 1

    expressions = Parser.getExpDateJourSeances(dates_str)
    if index == 0 or index == dates_len:
        return dates_str, dates_len

    pos_start, pos_end, exp = expressions[1][index]
    return "Le " + dates_str[pos_start:], dates_len - index
