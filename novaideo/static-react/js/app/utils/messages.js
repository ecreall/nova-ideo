import { I18n } from 'react-redux-i18n';

import { get } from './routeMap';

export const getPresentProposalMessage = (proposal, user, site) => {
  return I18n.t('messages.present.proposal.message', {
    proposal: proposal.title,
    user: user,
    site: site,
    url: window.location.origin + get('ideas', { ideaId: proposal.id })
  });
};

export const getPresentProposalSubject = (proposal) => {
  return I18n.t('messages.present.proposal.subject', { proposal: proposal.title });
};