/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import classNames from 'classnames';
import Grow from 'material-ui/transitions/Grow';
import Paper from 'material-ui/Paper';
import { Manager, Target, Popper } from 'react-popper';
import ClickAwayListener from 'material-ui/utils/ClickAwayListener';
import { withStyles } from 'material-ui/styles';
import ReactDOM from 'react-dom';

import { MenuList, MenuItem } from '../styledComponents/MenuList';
import { ListItemIcon, ListItemText } from '../styledComponents/List';

const menuRoot = document.getElementById('menu-root');

export function renderMenuItem({ Icon, title, onClick, color, hoverColor }) {
  return (
    <MenuItem onClick={onClick} hoverColor={hoverColor}>
      {Icon &&
        <ListItemIcon>
          <Icon className="menu-item-icon" />
        </ListItemIcon>}
      <ListItemText
        color={color}
        classes={{
          primary: 'menu-item-text'
        }}
        primary={title}
      />
    </MenuItem>
  );
}

const styles = {
  popper: {
    zIndex: 3000
  },
  popperClose: {
    pointerEvents: 'none'
  },
  paper: {
    borderRadius: 6,
    width: 300,
    border: '1px solid rgba(0,0,0,.15)'
  }
};

class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      menu: false
    };
    this.popper = document.createElement('div');
  }

  componentDidMount() {
    menuRoot.appendChild(this.popper);
  }

  componentWillUnmount() {
    menuRoot.removeChild(this.popper);
  }

  openMenu = () => {
    const { onOpen } = this.props;
    this.setState({ menu: true }, () => {
      if (onOpen) {
        onOpen();
      }
    });
  };

  closeMenu = (event, fieldCallback) => {
    const { onClose } = this.props;
    this.setState({ menu: false }, () => {
      if (fieldCallback) fieldCallback();
      if (onClose) onClose();
    });
  };

  renderItem = (field) => {
    const { theme } = this.props;
    if (typeof field === 'function') {
      return (
        <div onClick={this.closeMenu}>
          {field()}
        </div>
      );
    }
    const Icon = field.Icon;
    return renderMenuItem({
      Icon: Icon,
      title: field.title,
      color: field.color,
      hoverColor: field.hoverColor || theme.palette.info[500],
      onClick: (event) => {
        this.closeMenu(event, field.onClick);
      }
    });
  };

  render() {
    const { id, fields, classes, children } = this.props;
    const { menu } = this.state;
    return (
      <Manager
        className={classNames(classes.menu, {
          [classes.menuOpen]: menu
        })}
      >
        <Target onClick={this.openMenu}>
          {children}
        </Target>
        {ReactDOM.createPortal(
          <Popper
            placement="top-start"
            eventsEnabled={menu}
            className={classNames(classes.popper, { [classes.popperClose]: !menu })}
          >
            <ClickAwayListener onClickAway={this.closeMenu}>
              <Grow in={menu} id={id} style={{ transformOrigin: '0 0 0' }}>
                <Paper elevation={6} className={classes.paper}>
                  <MenuList role="menu">
                    {fields.map((field) => {
                      return this.renderItem(field);
                    })}
                  </MenuList>
                </Paper>
              </Grow>
            </ClickAwayListener>
          </Popper>,
          this.popper
        )}
      </Manager>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Menu);