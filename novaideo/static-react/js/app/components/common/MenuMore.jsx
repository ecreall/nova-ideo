/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';
import { Translate } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import IconButton from '@material-ui/core/IconButton';
import MoreHorizIcon from '@material-ui/icons/MoreHoriz';

import Actions from '../../graphql/queries/Actions.graphql';
import { Menu, MenuList } from '../common/menu';
import { ACTIONS } from '../../processes';
import { getActions, filterActions } from '../../utils/processes';

const styles = (theme) => {
  return {
    progress: {
      width: '100%',
      minWidth: 320,
      minHeight: 200,
      display: 'flex',
      justifyContent: 'center'
    },
    button: {
      height: 30,
      width: 30,
      '&:hover': {
        color: theme.palette.info[500]
      }
    },
    icon: {
      height: 20,
      width: 20,
      fontSize: '20px !important'
    }
  };
};

export const getFields = (actions, onActionClick, theme, titlesProps = {}) => {
  return actions.map((action) => {
    const isDanger = action.tags.includes(ACTIONS.danger);
    return {
      title: <Translate value={action.title} {...titlesProps} />,
      color: isDanger && theme.palette.danger.primary,
      hoverColor: isDanger && theme.palette.danger.primary,
      Icon: action.icon,
      onClick: () => {
        if (onActionClick) onActionClick(action);
      }
    };
  });
};

export const DumbMenuMore = ({ context, data, close, onActionClick, theme, classes }) => {
  if (!data.actions) return null;
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
  return (
    fields.length > 0 && (
      <Menu
        id={`${context.id}-menu-more`}
        activator={
          <IconButton aria-haspopup="true" className={classes.button} aria-label="More">
            <MoreHorizIcon className={classes.icon} />
          </IconButton>
        }
      >
        <MenuList fields={fields} close={close} />
      </Menu>
    )
  );
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