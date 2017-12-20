/* eslint-disable import/prefer-default-export, no-underscore-dangle, no-param-reassign */

import { ICONS_MAPPING } from '../constants';

export const getActions = (actions, descriminator) => {
  const newActions = actions
    .filter((action) => {
      return action.styleDescriminator === descriminator;
    })
    .map((action) => {
      const newAction = { ...action };
      newAction.stylePicto = action.stylePicto in ICONS_MAPPING ? ICONS_MAPPING[action.stylePicto] : 'alert-circle-outline';
      return newAction;
    });
  newActions.sort((a1, a2) => {
    return a1.styleOrder - a2.styleOrder;
  });
  return newActions;
};