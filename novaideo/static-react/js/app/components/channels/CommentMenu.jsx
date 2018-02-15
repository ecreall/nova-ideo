/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import IconButton from 'material-ui/IconButton';
import MoreHorizIcon from 'material-ui-icons/MoreHoriz';

import { MenuList, Menu } from '../common/menu';
import EmojiPicker from '../forms/widgets/EmojiPicker';
import { ACTIONS } from '../../constants';
import { getActions } from '../../utils/entities';

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

  render() {
    const { classes, comment, onActionClick } = this.props;
    if (!this.state.menu) return null;
    const actions = getActions(comment.actions, { descriminator: [ACTIONS.global, ACTIONS.text, ACTIONS.plus] });
    const fields = actions.map((action) => {
      return {
        title: action.title,
        Icon: action.icon,
        onClick: () => {
          if (onActionClick) onActionClick(action);
        }
      };
    });
    return (
      <div className={classes.container}>
        <div className={classes.action}>
          <EmojiPicker
            classes={{
              button: classes.button,
              icon: classes.icon
            }}
            onSelect={this.onSelectEmoji}
            style={{ picker: { right: 1 } }}
          />
        </div>
        <div>
          <Menu
            id="comment-more-menu"
            activator={
              <IconButton aria-haspopup="true" className={classes.button} aria-label="More">
                <MoreHorizIcon className={classes.icon} />
              </IconButton>
            }
          >
            <MenuList fields={fields} />
          </Menu>
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbCommentMenu);