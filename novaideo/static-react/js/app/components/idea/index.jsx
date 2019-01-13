import React from 'react';
import { Translate, I18n } from 'react-redux-i18n';

import { iconAdapter } from '../../utils/globalFunctions';
import { PROCESSES, STATE } from '../../processes';
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
  if (idea.state.includes(STATE.idea.favorable)) return 'bottom';
  if (idea.state.includes(STATE.idea.toStudy)) return 'middle';
  if (idea.state.includes(STATE.idea.unfavorable)) return 'top';
  return undefined;
}

export function getExaminationTtile(idea) {
  if (idea.state.includes(STATE.idea.favorable)) return I18n.t('states.idea.favorable');
  if (idea.state.includes(STATE.idea.toStudy)) return I18n.t('states.idea.toStudy');
  if (idea.state.includes(STATE.idea.unfavorable)) return I18n.t('states.idea.unfavorable');
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
      Tooltip: createTooltip(
        <Translate value="evaluation.support" count={idea.tokensSupport} />,
        idea.tokensSupport,
        classes.tooltipSupport
      )
    },
    {
      color: '#ef6e18',
      count: idea.tokensOpposition,
      Tooltip: createTooltip(
        <Translate value="evaluation.opposition" count={idea.tokensOpposition} />,
        idea.tokensOpposition,
        classes.tooltipOppose
      )
    }
  ];
}