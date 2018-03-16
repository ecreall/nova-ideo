import { I18n } from 'react-redux-i18n';

import { iconAdapter } from '../../utils/globalFunctions';
import { PROCESSES } from '../../processes';
import { createTooltip } from '../common/Doughnut';

export function getEvaluationIcons(userToken) {
  return {
    top:
      userToken === 'support'
        ? iconAdapter('mdi-set mdi-arrow-up-drop-circle-outline')
        : iconAdapter('mdi-set mdi-arrow-up-drop-circle'),
    down:
      userToken === 'oppose'
        ? iconAdapter('mdi-set mdi-arrow-down-drop-circle-outline')
        : iconAdapter('mdi-set mdi-arrow-down-drop-circle')
  };
}

export function getExaminationValue(idea) {
  if (idea.state.includes('favorable')) return 'bottom';
  if (idea.state.includes('to_study')) return 'middle';
  if (idea.state.includes('unfavorable')) return 'top';
  return undefined;
}

export function getEvaluationActions(idea) {
  const actions = PROCESSES.ideamanagement.nodes;
  const withdrawAction = actions.withdrawToken;
  const supportAction = idea.userToken === 'support' ? withdrawAction : actions.support;
  const opposeAction = idea.userToken === 'oppose' ? withdrawAction : actions.oppose;
  const result = {
    top: supportAction,
    down: opposeAction
  };
  return result;
}

export function getIdeaSupportStats(idea, classes) {
  return [
    {
      color: '#4eaf4e',
      count: idea.tokensSupport,
      Tooltip: createTooltip(I18n.t('evaluation.support'), idea.tokensSupport, classes.tooltipSupport)
    },
    {
      color: '#ef6e18',
      count: idea.tokensOpposition,
      Tooltip: createTooltip(I18n.t('evaluation.opposition'), idea.tokensOpposition, classes.tooltipOppose)
    }
  ];
}