import React from 'react';
import { withStyles } from 'material-ui/styles';
import { CardActions } from 'material-ui/Card';
import IconButton from 'material-ui/IconButton';
import { I18n } from 'react-redux-i18n';

import OverlaidTooltip from './OverlaidTooltip';

const styles = (theme) => {
  return {
    actionsContainer: {
      height: 0,
      width: '100%'
    },
    actionsText: {
      fontSize: 13,
      color: '#585858',
      fontWeight: '700',
      marginRight: 35,
      '&:hover': {
        color: theme.palette.info['700']
      }
    },
    actionsIcon: {
      fontWeight: 100,
      fontSize: '16px !important',
      marginRight: 5,
      marginTop: 1,
      height: 16,
      width: 16
    }
  };
};

class AllignedActions extends React.Component {
  render() {
    const { actions, onActionClick, overlayPosition, classes } = this.props;
    return (
      <CardActions classes={{ root: classes.actionsContainer }} disableActionSpacing>
        {actions.map((action, key) => {
          const Icon = action.icon;
          return (
            <IconButton
              className={classes.actionsText}
              key={key}
              onClick={() => {
                if (onActionClick) onActionClick(action);
              }}
              aria-label="todo"
            >
              <OverlaidTooltip tooltip={I18n.t(action.title)} placement={overlayPosition}>
                <Icon className={classes.actionsIcon} />
              </OverlaidTooltip>
              {action.counter}
            </IconButton>
          );
        })}
      </CardActions>
    );
  }
}

export default withStyles(styles)(AllignedActions);