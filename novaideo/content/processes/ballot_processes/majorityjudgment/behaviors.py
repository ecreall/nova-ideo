# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# avalaible on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Majority Judgment election process definition.
"""

from substanced.util import get_oid

from dace.objectofcollaboration.principal.util import get_current
from pontus.file import OBJECT_DATA

from novaideo.content.processes.ballot_processes import VoteBase


class Vote(VoteBase):

    def start(self, context, request, appstruct, **kw):
        vote_result = {}
        for candidate in appstruct['candidates']:
            vote_result[get_oid(candidate[OBJECT_DATA])] = candidate['judgment']

        user = get_current()
        ballot = self.process.ballot
        report = ballot.report
        votefactory = report.ballottype.vote_factory
        ballot.ballot_box.addtoproperty('votes', votefactory(vote_result))
        report.addtoproperty('voters', user)
        return {}


#TODO behaviors
