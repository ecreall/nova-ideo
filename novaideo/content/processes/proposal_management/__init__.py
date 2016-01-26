# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import venusian

from dace.objectofcollaboration.entity import Entity

from novaideo.core import _


AMENDMENTS_CYCLE_DEFAULT_DURATION = [
              _("Three minutes"),
              _("Five minutes"),
              _("Ten minutes"),
              _("Twenty minutes"),
              _("One hour"),
              _("Four hours"),
              _("One day"),
              _("Three days"),
              _("One week"),
              _("Two weeks")]


WORK_MODES = {}


class work_mode(object):
    """ Decorator for novaideo access actions. 
    An access action allows to view an object"""

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            WORK_MODES[ob.work_id] = ob()

        venusian.attach(wrapped, callback)
        return wrapped


class WorkMode(Entity):

    work_mode_process_id = NotImplemented
    participants_mini = NotImplemented
    participants_maxi = 12
    title = _('Work mode')
    description = _('Work mode for the improvement of the proposal')
    work_id = 'work_mode'
    order = 0


@work_mode()
class WikiWorkMode(WorkMode):

    work_mode_process_id = 'wikiworkmodeprocess'
    participants_mini = 1
    title = _('Change without validation (At least one member)')
    work_id = 'wiki'
    order = 0


@work_mode()
class CorrectionWorkMode(WorkMode):

    work_mode_process_id = 'correctionworkmodeprocess'
    participants_mini = 3
    title = _('Change with validation (At least three members)')
    work_id = 'correction'
    order = 1


@work_mode()
class AmendmentWorkMode(WorkMode):

    work_mode_process_id = 'amendmentworkmodeprocess'
    participants_mini = 3
    title = _('Change with amendments (At least three members)')
    work_id = 'amendment'
    order = 2
