# -*- coding: utf8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

"""
This module represent all of behaviors used in the
Referendum election process definition.
"""

from dace.objectofcollaboration.principal.util import get_current

from novaideo.content.processes.ballot_processes import VoteBase


class Vote(VoteBase):

    def start(self, context, request, appstruct, **kw):
        vote = appstruct['vote']
        user = get_current()
        ballot = self.process.ballot
        report = ballot.report
        votefactory = report.ballottype.vote_factory
        vote_instance = votefactory(vote)
        ballot.ballot_box.addtoproperty('votes', vote_instance)
        elector = report.get_elector(user)
        report.addtoproperty('voters', elector)
        return {'vote_uid': vote_instance.uid,
                'ballot': ballot}


#TODO behaviors
