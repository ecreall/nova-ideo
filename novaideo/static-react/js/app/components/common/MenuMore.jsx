/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import { CircularProgress } from 'material-ui/Progress';

import { actionsQuery } from '../../graphql/queries';
import { MenuList } from '../common/menu';
import { ACTIONS } from '../../processes';
import { getActions, filterActions } from '../../utils/processes';

const styles = {
  progress: {
    width: '100%',
    display: 'flex',
    justifyContent: 'center'
  }
};

export class DumbMenuMore extends React.Component {
  getFields = (actions) => {
    const { onActionClick, theme } = this.props;
    return actions.map((action) => {
      const isDanger = action.tags.includes(ACTIONS.danger);
      return {
        title: action.title,
        color: isDanger && theme.palette.danger.primary,
        hoverColor: isDanger && theme.palette.danger.primary,
        Icon: action.icon,
        onClick: () => {
          if (onActionClick) onActionClick(action);
        }
      };
    });
  };
  render() {
    const { data, close, classes } = this.props;
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
      fields = fields.concat(this.getFields(otherActions));
    }
    if (globalActions.length > 0) {
      if (fields.length > 0) fields.push('');
      fields = fields.concat(this.getFields(globalActions));
    }
    if (entityActions.length > 0) {
      if (fields.length > 0) fields.push('');
      fields = fields.concat(this.getFields(entityActions));
    }
    return <MenuList fields={fields} close={close} />;
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(actionsQuery, {
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