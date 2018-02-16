/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';

import { Menu } from '../common/menu';
import UserPopover from './UserPopover';

const styles = {
  menuPaper: {
    width: 'auto',
    maxHeight: 'inherit',
    overflowX: 'auto',
    borderRadius: 6,
    '& > ul': {
      padding: 0
    }
  },
  title: {
    display: 'flex',
    fontSize: 15,
    color: '#2c2d30',
    fontWeight: '900',
    justifyContent: 'space-around',
    cursor: 'pointer',
    '&:hover': {
      textDecoration: 'underline'
    }
  }
};

export class DumbUserTitle extends React.Component {
  menu = null;

  closeMenu = () => {
    if (this.menu) this.menu.close();
  };

  render() {
    const { classes, node, onOpen } = this.props;
    return (
      <Menu
        onOpen={onOpen}
        id={`${node.id}-menu`}
        anchorOrigin={{ vertical: 'center', horizontal: 'center' }}
        initRef={(menu) => {
          this.menu = menu;
        }}
        classes={{
          menuPaper: classes.menuPaper
        }}
        activator={
          <span className={classes.title}>
            {node.title}
          </span>
        }
      >
        <UserPopover id={node.id} onActionClick={this.closeMenu} />
      </Menu>
    );
  }
}

export default withStyles(styles)(DumbUserTitle);