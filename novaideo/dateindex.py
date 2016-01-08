
import calendar
import pytz
import datetime

from persistent import Persistent
from BTrees.Length import Length
from ZODB.broken import Broken
from hypatia.keyword import KeywordIndex
from hypatia.field import FieldIndex
from hypatia.query import InRange
from hypatia._compat import string_types
from plone.event.recurrence import recurrence_sequence_ical

from substanced.catalog.factories import IndexFactory
from substanced.catalog.indexes import SDIndex
from substanced.catalog.discriminators import dummy_discriminator
from substanced.content import content
from . import log

_marker = None


class InRangeWithNotIndexed(InRange):
    """ Index value falls within a range.

    CQE eqivalent: lower < index < upper
                   lower <= index <= upper
    """

    def _apply(self, names):
        result = super(InRangeWithNotIndexed, self)._apply(names)
        # result is a BTrees.LFBTree.LFSet
        # and self.index.not_indexed() is a BTrees.LFBTree.LFTreeSet
        result = self.index.family.IF.union(result, self.index.not_indexed())
        # result.update(self.index.not_indexed()) is slower
        # return a BTrees.LFBTree.LFSet
        return result


def int2dt(dtint, hours=None, minutes=None):
    """ Returns a datetime object from an integer representation with
    resolution of one minute. The datetime returned is in the UTC zone.

    >>> from plone.event.utils import int2dt
    >>> int2dt(1077760031)
    datetime.datetime(2011, 11, 11, 11, 11, tzinfo=<UTC>)

    Dateconversion with int2dt from anything else than integers does not work
    >>> int2dt(.0)
    Traceback (most recent call last):
    ...
    ValueError: int2dt expects integer values as arguments.

    """
    if not isinstance(dtint, int):
        raise ValueError('int2dt expects integer values as arguments.')

    try:
        date = datetime.datetime.utcfromtimestamp(dtint).replace(
            tzinfo=pytz.UTC)
        if hours is not None and minutes is not None:
            date = datetime.datetime.combine(
                date, datetime.time(hours, minutes, 0, tzinfo=pytz.UTC))

        return date
    except ValueError:
        log.error(str(dtint))
        raise


def dt2int(date):
    return calendar.timegm(date.timetuple())


class HypatiaDateRecurringIndex(KeywordIndex, FieldIndex):

    def discriminate(self, obj, default):
        """ See interface IIndexInjection """
        if callable(self.discriminator):
            value = self.discriminator(obj, _marker)
        else:
            value = getattr(obj, self.discriminator, _marker)

        if value is _marker:
            return default

        if isinstance(value, Persistent):
            raise ValueError('Catalog cannot index persistent object %s' %
                             value)

        if isinstance(value, Broken):
            raise ValueError('Catalog cannot index broken object %s' %
                             value)

        if not isinstance(value, dict):
            raise ValueError('Catalog can only index dict with '
                'attr and date keys, or date and recurdef keys, given %s' %
                             value)
        # examples:
        # {'attr': 'dates',
        #  'date': datetime.datetime.now()}
        # will get dates_recurrence attribute on the obj to get iCal string
        # for recurrence definition
        # or
        # {'date': datetime.datetime.now(),
        #  'recurdef': ICALSTRING}
        # no access to obj attributes at all

        date = value.get('date')
        default_recurdef = value.get('recurdef', _marker)
        if default_recurdef is not _marker:
            recurdef = default_recurdef
        else:
            attr_recurdef = value.get('attr') + '_recurrence'
            recurdef = getattr(obj, attr_recurdef, None)

        if callable(recurdef):
            recurdef = recurdef()

        if not recurdef:
            dates = [date]
        else:
            dates = recurrence_sequence_ical(date, recrule=recurdef)

        # dates is a generator
        return tuple(dates)

    def normalize(self, dates):
        return [dt2int(date) for date in dates]

# below is the same implementation as Keyword Index, but replacing
# self._fwd_index = self.family.OO.BTree() by self._fwd_index = self.family.IO.BTree()
# family.OO.Set by family.II.Set
# family.OO.difference by family.II.difference

    def reset(self):
        """Initialize forward and reverse mappings."""
        # The forward index maps index keywords to a sequence of docids
        self._fwd_index = self.family.IO.BTree()

        # The reverse index maps a docid to its keywords
        self._rev_index = self.family.IO.BTree()
        self._num_docs = Length(0)
        self._not_indexed = self.family.IF.TreeSet()

    def index_doc(self, docid, obj):
        seq = self.discriminate(obj, _marker)

        if seq is _marker:
            if not (docid in self._not_indexed):
                # unindex the previous value
                self.unindex_doc(docid)
                # Store docid in set of unindexed docids
                self._not_indexed.add(docid)
            return None

        if docid in self._not_indexed:
            # Remove from set of unindexed docs if it was in there.
            self._not_indexed.remove(docid)

        if isinstance(seq, string_types):
            raise TypeError('seq argument must be a list/tuple of strings')

        old_kw = self._rev_index.get(docid, None)
        if not seq:
            if old_kw:
                self.unindex_doc(docid)
            return

        seq = self.normalize(seq)

        new_kw = self.family.II.Set(seq)

        if old_kw is None:
            self._insert_forward(docid, new_kw)
            self._insert_reverse(docid, new_kw)
            self._num_docs.change(1)
        else:
            # determine added and removed keywords
            kw_added = self.family.II.difference(new_kw, old_kw)
            kw_removed = self.family.II.difference(old_kw, new_kw)

            if not (kw_added or kw_removed):
                return

            # removed keywords are removed from the forward index
            for word in kw_removed:
                fwd = self._fwd_index[word]
                fwd.remove(docid)
                if not fwd:
                    del self._fwd_index[word]

            # now update reverse and forward indexes
            self._insert_forward(docid, kw_added)
            self._insert_reverse(docid, new_kw)

    def applyInRange(self, start, end, excludemin=False, excludemax=False):
        if start is not None:
            start = dt2int(start)

        if end is not None:
            end = dt2int(end)

        return self.family.IF.multiunion(
            self._fwd_index.values(
                start, end, excludemin=excludemin, excludemax=excludemax)
        )

    def document_repr(self, docid, default=None):
        result = self._rev_index.get(docid, default)
        if result is not default:
            return ', '.join([int2dt(r).isoformat() for r in result])
#            return repr(result)
        return default

    def inrange_with_not_indexed(self, start, end, excludemin=False,
            excludemax=False):
        return InRangeWithNotIndexed(self, start, end, excludemin, excludemax)



@content(
    'Date Recurring Index',
    icon='glyphicon glyphicon-search',
    is_index=True,
    )
class DateRecurringIndex(SDIndex, HypatiaDateRecurringIndex):
    def __init__(self, discriminator=None, family=None,
                 action_mode=None):
        if discriminator is None:
            discriminator = dummy_discriminator
        HypatiaDateRecurringIndex.__init__(
            self, discriminator, family=family
            )
        if action_mode is not None:
            self.action_mode = action_mode


class DateRecurring(IndexFactory):
    index_type = DateRecurringIndex
