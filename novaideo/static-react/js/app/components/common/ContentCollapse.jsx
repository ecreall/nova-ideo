/* eslint-disable no-undef */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { Collapse } from 'material-ui/transitions';
import { ListItem, ListItemText, ListItemIcon } from 'material-ui/List';
import KeyboardArrowDownIcon from 'material-ui-icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from 'material-ui-icons/KeyboardArrowUp';
import classNames from 'classnames';

const styles = (theme) => {
  return {
    list: {
      height: '100%'
    },
    entered: {
      height: '60% !important'
    },
    wrapper: {
      height: '100%'
    },
    wrapperInner: {
      height: '100%'
    },
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
      opacity: 0.95,
      padding: 0,
      whiteSpace: 'nowrap',
      textOverflow: 'ellipsis',
      overflow: 'hidden'
    },
    textActive: {
      opacity: 1,
      fontWeight: '700',
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    },
    sectionIcon: {
      width: 20,
      height: 20,
      marginRight: 7,
      marginTop: -3,
      color: 'white',
      opacity: 0.95
    },
    sectionIconActive: {
      opacity: 1,
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    },
    icon: {
      color: 'white',
      opacity: 0.95
    },
    iconActive: {
      opacity: 1,
      color: theme.palette.tertiary.hover.color,
      '&:hover': {
        color: theme.palette.tertiary.hover.color
      }
    }
  };
};

export class DumbContentCollapse extends React.Component {
  toggle = () => {
    const { onOpen, id } = this.props;
    onOpen(id);
  };

  render() {
    const { classes, title, Icon, open, children } = this.props;
    const textClasses = classNames(classes.text, { [classes.textActive]: open });
    const iconClasses = classNames(classes.icon, { [classes.iconActive]: open });
    const sectionIconClasses = classNames(classes.sectionIcon, { [classes.sectionIconActive]: open });
    return [
      <ListItem
        onClick={this.toggle}
        dense
        button
        classes={{ root: classNames(classes.listItem, { [classes.listItemActive]: open }) }}
      >
        <ListItemIcon>
          <Icon classes={{ root: sectionIconClasses }} />
        </ListItemIcon>
        <ListItemText classes={{ primary: textClasses }} className={textClasses} primary={title} />
        {open
          ? <KeyboardArrowUpIcon classes={{ root: iconClasses }} />
          : <KeyboardArrowDownIcon classes={{ root: iconClasses }} />}
      </ListItem>,
      <Collapse
        in={open}
        timeout={300}
        classes={{
          container: classes.container,
          entered: classes.entered,
          wrapper: classes.wrapper,
          wrapperInner: classes.wrapperInner
        }}
      >
        {children}
      </Collapse>
    ];
  }
}

export default withStyles(styles)(DumbContentCollapse);