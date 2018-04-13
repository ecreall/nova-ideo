/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';
import { I18n } from 'react-redux-i18n';

import Actions from '../../graphql/queries/Actions.graphql';
import { MenuList } from '../common/menu';
import { ACTIONS } from '../../processes';
import { getActions, filterActions } from '../../utils/processes';

const styles = {
  progress: {
    width: '100%',
    minWidth: 320,
    minHeight: 200,
    display: 'flex',
    justifyContent: 'center'
  }
};

const getFields = (actions, onActionClick, theme) => {
  return actions.map((action) => {
    const isDanger = action.tags.includes(ACTIONS.danger);
    return {
      title: I18n.t(action.title),
      color: isDanger && theme.palette.danger.primary,
      hoverColor: isDanger && theme.palette.danger.primary,
      Icon: action.icon,
      onClick: () => {
        if (onActionClick) onActionClick(action);
      }
    };
  });
};

export const DumbMenuMore = ({ data, close, onActionClick, theme, classes }) => {
  if (!data.actions) {
    return (
      <div className={classes.progress}>
        <CircularProgress size={30} />
      </div>
    );
  }
  const actions = getActions(
    data.actions.edges.map((action) => {
      return action.node;
    }),
    { tags: ACTIONS.secondary }
  );
  const otherActions = filterActions(actions, { tags: ACTIONS.other });
  const globalActions = filterActions(actions, { tags: ACTIONS.global });
  const entityActions = filterActions(actions, { tags: ACTIONS.entity });
  let fields = [];
  if (otherActions.length > 0) {
    fields = fields.concat(getFields(otherActions, onActionClick, theme));
  }
  if (globalActions.length > 0) {
    if (fields.length > 0) fields.push('');
    fields = fields.concat(getFields(globalActions, onActionClick, theme));
  }
  if (entityActions.length > 0) {
    if (fields.length > 0) fields.push('');
    fields = fields.concat(getFields(entityActions, onActionClick, theme));
  }
  return <MenuList fields={fields} close={close} />;
};

export default withStyles(styles, { withTheme: true })(
  graphql(Actions, {
    options: (props) => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: {
          context: props.context.oid,
          processIds: [],
          nodeIds: [],
          processTags: [],
          actionTags: [ACTIONS.secondary]
        }
      };
    }
  })(DumbMenuMore)
);