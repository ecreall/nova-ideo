/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import IconButton from 'material-ui/IconButton';
import MoreHorizIcon from 'material-ui-icons/MoreHoriz';

import { Menu } from '../common/menu';
import EmojiPicker from '../forms/widgets/EmojiPicker';
import { ACTIONS, PROCESSES } from '../../processes';
import { getActions } from '../../utils/processes';
import MenuMore from '../common/MenuMore';

const styles = (theme) => {
  return {
    container: {
      position: 'absolute',
      right: 20,
      border: '1px solid rgba(0, 0, 0, 0.15)',
      borderRadius: 6,
      top: -13,
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
      width: 20
    },
    action: {
      borderRight: '1px solid rgba(0, 0, 0, 0.15)'
    }
  };
};

export class DumbCommentMenu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      menu: false
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
    const { classes, onActionClick } = this.props;
    const abstractProcessNodes = PROCESSES.novaideoabstractprocess.nodes;
    const Icon = action.icon;
    switch (action.nodeId) {
    case abstractProcessNodes.addreaction.nodeId:
      return (
        <EmojiPicker
          classes={{
            button: classes.button,
            icon: classes.icon
          }}
          onSelect={(emoji) => {
            if (onActionClick) onActionClick(action, { emoji: emoji });
          }}
          style={{ picker: { right: 1 } }}
        />
      );
    default:
      return (
        <IconButton
          onClick={() => {
            if (onActionClick) onActionClick(action);
          }}
          className={classes.button}
        >
          <Icon className={classes.icon} />
        </IconButton>
      );
    }
  };

  render() {
    const { classes, comment, onActionClick } = this.props;
    if (!this.state.menu) return null;
    const actions = getActions(comment.actions, { tags: ACTIONS.menu });
    return (
      <div className={classes.container}>
        {actions.map((action) => {
          return (
            <div className={classes.action}>
              {this.getAction(action)}
            </div>
          );
        })}
        <div>
          <Menu
            id="comment-more-menu"
            activator={
              <IconButton aria-haspopup="true" className={classes.button} aria-label="More">
                <MoreHorizIcon className={classes.icon} />
              </IconButton>
            }
          >
            <MenuMore context={comment} onActionClick={onActionClick} />
          </Menu>
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbCommentMenu);