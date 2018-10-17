/* eslint-disable import/prefer-default-export, no-underscore-dangle, no-param-reassign */
import HelpIcon from '@material-ui/icons/Help';
import {
  PROCESSES, ICONS_MAPPING, ENTITIES_ICONS, STATE
} from '../processes';

function equal(element, filter, defaultValue = true) {
  if (!filter) return defaultValue;
  if (typeof filter === 'object' && typeof element === 'object') {
    return element.some((e) => {
      return filter.includes(e);
    });
  }
  if (typeof filter === 'object') return filter.includes(element);
  if (typeof element === 'object') return element.includes(filter);
  return filter === element;
}
// filter = { tags: undefined, processId: undefined, nodeId: undefined }
export function filterActions(actions, filter = {}) {
  if (!actions) return [];
  const validKeys = Object.keys(filter).filter((key) => {
    return typeof filter === 'object' ? filter[key].length > 0 : filter[key];
  });
  return actions.filter((action) => {
    return validKeys.every((key) => {
      return key in action && equal(action[key], filter[key]);
    });
  });
}

export function getActionData(action) {
  const processId = action.processId;
  const behaviorId = action.behaviorId;
  const processDef = PROCESSES[processId];
  const newAction = { ...action, icon: action.icon in ICONS_MAPPING ? ICONS_MAPPING[action.icon] : HelpIcon };
  if (!processDef) return newAction;
  const actionDef = processDef.nodes[
    Object.keys(processDef.nodes).filter((key) => {
      const node = processDef.nodes[key];
      const id = node.behaviorId || node.nodeId;
      return id === behaviorId;
    })[0]
  ];
  if (!actionDef) return newAction;
  return { ...newAction, ...actionDef };
}

export function getActions(actions, filter = {}) {
  if (!actions) return [];
  const newActions = filterActions(actions, filter).map((action) => {
    return getActionData(action);
  });
  newActions.sort((a1, a2) => {
    return a1.order - a2.order;
  });
  return newActions;
}

export function getAction(actions, filter = {}) {
  return getActions(actions, filter)[0];
}

export function getEntityIcon(type) {
  return ENTITIES_ICONS[type] || ENTITIES_ICONS.default;
}

export function isPrivate(type, state) {
  switch (type) {
  case 'Idea':
    return state.includes(STATE.idea.private);
  default:
    return false;
  }
}