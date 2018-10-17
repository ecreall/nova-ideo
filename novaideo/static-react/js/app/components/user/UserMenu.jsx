/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import IconButton from '../styledComponents/IconButton';
import Button from '../styledComponents/Button';
import EmojiPicker from '../forms/widgets/EmojiPicker';
import { ACTIONS, PROCESSES } from '../../processes';
import { getActions } from '../../utils/processes';
import MenuMore from '../common/MenuMore';
import OverlaidTooltip from '../common/OverlaidTooltip';

const styles = (theme) => {
  return {
    container: {
      border: '1px solid rgba(0, 0, 0, 0.15)',
      borderRadius: 6,
      backgroundColor: 'white',
      zIndex: 10,
      boxShadow: '0 1px 1px rgba(0, 0, 0, 0.1)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      '&:hover': {
        borderColor: 'rgba(0, 0, 0, 0.3)'
      }
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
    },
    iconButton: {
      marginRight: 5,
      height: 17,
      width: 17,
      fontSize: '17px !important'
    },
    action: {
      borderRight: '1px solid rgba(0, 0, 0, 0.15)',
      '&:only-child': {
        borderRight: 'none'
      }
    }
  };
};

export class DumbUserMenu extends React.Component {
  static defaultProps = {
    overlayPosition: 'top'
  };

  constructor(props) {
    super(props);
    this.state = {
      menu: props.open
    };
  }

  componentDidMount() {
    const { initRef } = this.props;
    if (initRef) {
      initRef(this);
    }
  }

  open = () => {
    this.setState({ menu: true });
  };

  close = () => {
    this.setState({ menu: false });
  };

  getAction = (action) => {
    const { classes, onActionClick, actionsProps } = this.props;
    const abstractProcessNodes = PROCESSES.novaideoabstractprocess.nodes;
    const Icon = action.icon;
    const actionProps = (actionsProps && actionsProps[action.behaviorId]) || {};
    const actionClassName = actionProps.className || classes.button;
    switch (action.nodeId) {
    case abstractProcessNodes.addreaction.nodeId:
      return (
        <EmojiPicker
          classes={{
            button: actionClassName,
            icon: classes.icon
          }}
          onSelect={(emoji) => {
            if (onActionClick) onActionClick(action, { emoji: emoji });
          }}
          style={{ picker: { right: 1 } }}
        />
      );
    default:
      return actionProps.type === 'button' ? (
        <Button
          onClick={() => {
            if (onActionClick) onActionClick(action);
          }}
          {...actionProps.props}
          className={actionClassName}
        >
          <Icon className={classes.iconButton} />
          {I18n.t(action.title)}
        </Button>
      ) : (
        <IconButton
          onClick={() => {
            if (onActionClick) onActionClick(action);
          }}
          className={actionClassName}
        >
          <Icon className={classes.icon} />
        </IconButton>
      );
    }
  };

  render() {
    const {
      user, classes, onActionClick, overlayPosition
    } = this.props;
    if (!this.state.menu) return null;
    const actions = getActions(user.actions, { tags: ACTIONS.menu });
    return (
      <div className={classes.container}>
        {actions.map((action) => {
          return (
            <OverlaidTooltip tooltip={I18n.t(action.description || action.title)} placement={overlayPosition}>
              <div className={classes.action}>{this.getAction(action)}</div>
            </OverlaidTooltip>
          );
        })}
        <MenuMore context={user} onActionClick={onActionClick} />
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbUserMenu);