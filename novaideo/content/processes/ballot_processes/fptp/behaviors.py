# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
FPTP election process definition.
"""

from substanced.util import get_oid

from dace.objectofcollaboration.principal.util import get_current
from pontus.file import OBJECT_DATA

from novaideo.content.processes.ballot_processes import VoteBase


class Vote(VoteBase):

    def start(self, context, request, appstruct, **kw):
        elected_id = appstruct['elected']
        try:
            subject_id = get_oid(elected_id[OBJECT_DATA])
        except Exception:
            subject_id = elected_id

        user = get_current()
        ballot = self.process.ballot
        report = ballot.report
        votefactory = report.ballottype.vote_factory
        ballot.ballot_box.addtoproperty('votes', votefactory(subject_id))
        report.addtoproperty('voters', user)
        return {}


#TODO behaviors
