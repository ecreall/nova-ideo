/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import classNames from 'classnames';
import AddIcon from 'material-ui-icons/Add';
import IconButton from 'material-ui/IconButton';
import { MenuItem, MenuList } from 'material-ui/Menu';
import Grow from 'material-ui/transitions/Grow';
import Paper from 'material-ui/Paper';
import { Manager, Target, Popper } from 'react-popper';
import ClickAwayListener from 'material-ui/utils/ClickAwayListener';
import { withStyles } from 'material-ui/styles';

const styles = (theme) => {
  return {
    popperClose: {
      pointerEvents: 'none'
    },
    menu: {
      flex: 1,
      display: 'flex',
      position: 'absolute',
      alignItems: 'center',
      height: '100%',
      zIndex: 1,
      borderBottomLeftRadius: 3,
      borderTopLeftRadius: 3,
      marginLeft: -1,
      '&:hover': {
        backgroundColor: theme.palette.tertiary.color,
        border: 'solid 1px',
        borderColor: theme.palette.tertiary.color,
        '& .comment-menu-button': {
          color: theme.palette.tertiary.hover.color
        }
      }
    },
    menuOpen: {
      backgroundColor: theme.palette.tertiary.color,
      border: 'solid 1px',
      borderColor: theme.palette.tertiary.color
    },
    buttonOpen: {
      color: theme.palette.tertiary.hover.color
    }
  };
};

class CommentMenu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      menu: false
    };
  }

  openMenu = () => {
    this.setState({ menu: true });
  };

  closeMenu = () => {
    this.setState({ menu: false });
  };

  render() {
    const { fields, classes } = this.props;
    const { menu } = this.state;
    return (
      <Manager
        className={classNames(classes.menu, {
          [classes.menuOpen]: menu
        })}
      >
        <Target>
          <IconButton
            className={classNames('comment-menu-button', {
              [classes.buttonOpen]: menu
            })}
            aria-owns={menu ? 'comment-menu-list' : null}
            aria-haspopup="true"
            onClick={this.openMenu}
          >
            <AddIcon />
          </IconButton>
        </Target>
        <Popper placement="top-start" eventsEnabled={menu} className={classNames({ [classes.popperClose]: !menu })}>
          <ClickAwayListener onClickAway={this.closeMenu}>
            <Grow in={menu} id="comment-menu-list" style={{ transformOrigin: '0 0 0' }}>
              <Paper elevation={6}>
                <MenuList role="menu">
                  {fields.map((field) => {
                    return (
                      <MenuItem onClick={this.closeMenu}>
                        {field}
                      </MenuItem>
                    );
                  })}
                </MenuList>
              </Paper>
            </Grow>
          </ClickAwayListener>
        </Popper>
      </Manager>
    );
  }
}

export default withStyles(styles, { withTheme: true })(CommentMenu);