/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import IconButton from 'material-ui/IconButton';
import MoreHorizIcon from 'material-ui-icons/MoreHoriz';

import { Menu, Popper } from '../common/menu';
import EmojiPicker from '../forms/widgets/EmojiPicker';

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
  render() {
    const { classes } = this.props;
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
          <Popper
            id="comment-menu"
            activator={
              <IconButton className={classes.button} aria-label="More" aria-haspopup="true" onClick={this.handleClick}>
                <MoreHorizIcon className={classes.icon} />
              </IconButton>
            }
          >
            <Menu
              fields={[
                {
                  title: 'Une action importante'
                },
                '',
                {
                  title: 'Supprimer le message',
                  color: '#d7385d',
                  hoverColor: '#d7385d'
                }
              ]}
            />
          </Popper>
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbCommentMenu);