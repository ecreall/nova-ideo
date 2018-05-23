import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import CardActions from '@material-ui/core/CardActions';
import { I18n } from 'react-redux-i18n';

import OverlaidTooltip from './OverlaidTooltip';
import Button, { IconButton } from '../styledComponents/Button';

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
    },
    btnAction: {
      marginRight: '4px !important',
      minWidth: 'auto',
      minHeight: 'auto',
      padding: '5px 10px'
    }
  };
};

const IconActions = ({ actions, onActionClick, overlayPosition, actionDecoration, classes }) => {
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
            >
              <Icon className={classes.actionsIcon} />
              {action.counter}
            </IconButton>
          </OverlaidTooltip>
        );
      })}
    </CardActions>
  );
};

const BtnActions = ({ actions, onActionClick, theme, classes }) => {
  return (
    <CardActions classes={{ root: classes.actionsContainer }} disableActionSpacing>
      {actions.map((action, key) => {
        return (
          <Button
            key={key}
            onClick={() => {
              if (onActionClick) onActionClick(action);
            }}
            className={classes.btnAction}
            background={theme.palette.primary[500]}
          >
            {I18n.t(action.title)}
          </Button>
        );
      })}
    </CardActions>
  );
};

export const DumbAllignedActions = ({ type = 'icon', ...props }) => {
  switch (type) {
  case 'icon':
    return <IconActions {...props} />;
  case 'button':
    return <BtnActions {...props} />;
  default:
    return null;
  }
};

export default withStyles(styles, { withTheme: true })(DumbAllignedActions);