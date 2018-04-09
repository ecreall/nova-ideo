import React from 'react';
import { withStyles } from 'material-ui/styles';
import { CardActions } from 'material-ui/Card';
// import IconButton from 'material-ui/IconButton';
import { I18n } from 'react-redux-i18n';

import OverlaidTooltip from './OverlaidTooltip';
import { IconButton } from '../styledComponents/Button';

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
      width: 16,
      overflow: 'inherit'
    }
  };
};

class AllignedActions extends React.Component {
  render() {
    const { actions, onActionClick, overlayPosition, actionDecoration, classes } = this.props;
    return (
      <CardActions classes={{ root: classes.actionsContainer }} disableActionSpacing>
        {actions.map((action, key) => {
          const Icon = action.icon;
          return (
            <OverlaidTooltip tooltip={I18n.t(action.description || action.title)} placement={overlayPosition}>
              <IconButton
                className={classes.actionsText}
                textColor={actionDecoration && action.active && action.color}
                key={key}
                onClick={() => {
                  if (onActionClick) onActionClick(action);
                }}
                aria-label="todo"
              >
                <Icon className={classes.actionsIcon} />
                {action.counter}
              </IconButton>
            </OverlaidTooltip>
          );
        })}
      </CardActions>
    );
  }
}

export default withStyles(styles)(AllignedActions);