/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import Icon from 'material-ui/Icon';
import classNames from 'classnames';

import { Menu } from '../common/menu';
import IdeaPopover from '../idea/IdeaPopover';

const styles = (theme) => {
  return {
    listItem: {
      paddingTop: 4,
      paddingBottom: 4
    },
    listItemActive: {
      backgroundColor: theme.palette.tertiary.color,
      '&:hover': {
        backgroundColor: theme.palette.tertiary.color
      }
    },
    text: {
      color: 'white',
      fontSize: 15,
      opacity: 0.8,
      padding: 0,
      whiteSpace: 'nowrap',
      textOverflow: 'ellipsis',
      overflow: 'hidden'
    },
    textActive: {
      opacity: 1,
      fontWeight: '700'
    },
    textSelected: {
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    },
    icon: {
      width: 17,
      height: 15,
      color: 'white',
      opacity: 0.4,
      marginRight: 0,
      fontSize: '12px !important'
    },
    iconActive: {
      opacity: 1
    },
    iconSelected: {
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    },
    menuPaper: {
      width: 'auto',
      maxHeight: 'inherit',
      overflowX: 'auto',
      borderRadius: 6,
      '& > ul': {
        padding: 0
      }
    }
  };
};

function getIcon(type) {
  switch (type) {
  case 'Idea':
    return 'mdi-set mdi-lightbulb';
  default:
    return 'mdi-set mdi-pound';
  }
}

export class DumbContentItem extends React.Component {
  menu = null;

  renderIcon = (isActive, isSelected) => {
    const { classes, node } = this.props;
    return (
      <ListItemIcon>
        <Icon
          className={classNames(getIcon(node.__typename), classes.icon, {
            [classes.iconActive]: isActive,
            [classes.iconSelected]: isSelected
          })}
        />
      </ListItemIcon>
    );
  };

  closeMenu = () => {
    if (this.menu) this.menu.close();
  };

  render() {
    const { classes, node } = this.props;
    return (
      <Menu
        id={`${node.id}-menu`}
        anchorOrigin={{ vertical: 'center', horizontal: 'center' }}
        initRef={(menu) => {
          this.menu = menu;
        }}
        classes={{
          menuPaper: classes.menuPaper
        }}
        activator={
          <ListItem dense button classes={{ root: classes.listItem }}>
            {this.renderIcon()}
            <ListItemText classes={{ primary: classes.text }} className={classes.text} primary={node.title} />
          </ListItem>
        }
      >
        <IdeaPopover id={node.id} onActionClick={this.closeMenu} />
      </Menu>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbContentItem);