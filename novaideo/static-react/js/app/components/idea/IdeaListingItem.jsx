/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { ListItem, ListItemIcon, ListItemSecondaryAction, ListItemText } from 'material-ui/List';
import Icon from 'material-ui/Icon';
import classNames from 'classnames';
import Badge from 'material-ui/Badge';
import { connect } from 'react-redux';
import CreateIcon from 'material-ui-icons/Create';

import { STATE } from '../../processes';
import { getEntityIcon } from '../../utils/processes';
// import { get } from '../../utils/routeMap';
import { Menu } from '../common/menu';
import IdeaPopover from './IdeaPopover';

const styles = (theme) => {
  return {
    listItem: {
      paddingTop: 4,
      paddingBottom: 4,
      paddingLeft: 16,
      paddingRight: 10
    },
    listItemPrivate: {
      paddingRight: '32px !important'
    },
    listItemSelected: {
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
    textSelected: {
      opacity: 1,
      fontWeight: '700',
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
    iconSelected: {
      opacity: 1,
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
    },
    root: {
      zIndex: -1
    },
    badge: {
      right: 15,
      marginTop: -11,
      fontWeight: '700'
    },
    badgeColor: {
      color: theme.palette.primary['500'],
      backgroundColor: 'white',
      marginLeft: 4,
      fontSize: 12,
      fontWeight: 700,
      top: 0,
      right: -7,
      opacity: 0.6,
      height: 20,
      width: 20
    },
    badgeColorSelected: {
      opacity: 1
    },
    unreadComment: {
      color: 'white',
      fontWeight: '700'
    },
    toStudy: {
      color: '#ef6e18',
      opacity: 0.9
    },
    favorable: {
      color: '#4eaf4e',
      opacity: 0.9
    },
    unfavorable: {
      color: '#f13b2d',
      opacity: 0.9
    }
  };
};

export class DumbIdeaListingItem extends React.Component {
  state = {
    open: false,
    hide: false
  };
  menu = null;

  renderIcon = (isActive) => {
    const { classes, node, edit, site } = this.props;
    const { open } = this.state;
    const isEdit = edit && edit.values && edit.values.text;
    if (isEdit) {
      return (
        <ListItemIcon>
          <CreateIcon
            className={classNames(classes.icon, {
              [classes.iconActive]: isActive,
              [classes.iconSelected]: open
            })}
          />
        </ListItemIcon>
      );
    }
    const EntityIcon = getEntityIcon(node.__typename);
    const state = node.state || [];
    let toStudy = false;
    let unfavorable = false;
    let favorable = false;
    if (site.examineIdeas) {
      toStudy = state.includes(STATE.idea.toStudy);
      unfavorable = state.includes(STATE.idea.unfavorable);
      favorable = state.includes(STATE.idea.favorable);
    }

    return (
      <ListItemIcon>
        <EntityIcon
          className={classNames(classes.icon, {
            [classes.iconActive]: isActive,
            [classes.iconSelected]: open,
            [classes.toStudy]: toStudy,
            [classes.unfavorable]: unfavorable,
            [classes.favorable]: favorable
          })}
        />
      </ListItemIcon>
    );
  };

  closeMenu = () => {
    if (this.menu) this.menu.close();
  };

  hideMenu = () => {
    this.setState({ hide: true });
  };

  showMenu = () => {
    this.setState({ hide: false });
  };

  onClose = () => {
    this.setState({ open: false });
  };

  onOpen = () => {
    this.setState({ open: true });
  };

  render() {
    const { classes, node } = this.props;
    const { open, hide } = this.state;
    // const ideaRoot = get('ideas', { ideaId: node.id });
    // const isOpened = open || location.pathname.startsWith(ideaRoot);
    const isPrevate = node.state.includes(STATE.idea.private);
    const textClasses = classNames(classes.text, { [classes.textSelected]: open });
    return (
      <Menu
        id={`${node.id}-menu`}
        onClose={this.onClose}
        onOpen={this.onOpen}
        anchorOrigin={{ vertical: 'center', horizontal: 'right' }}
        initRef={(menu) => {
          this.menu = menu;
        }}
        classes={{
          menuPaper: classes.menuPaper,
          menu: hide && classes.root
        }}
        activator={
          <ListItem
            dense
            button
            ContainerComponent="div"
            classes={{
              root: classNames(classes.listItem, { [classes.listItemSelected]: open, [classes.listItemPrivate]: isPrevate })
            }}
          >
            {this.renderIcon()}
            <ListItemText classes={{ primary: textClasses }} className={textClasses} primary={node.title} />
            {isPrevate &&
              <ListItemSecondaryAction className={classes.badge}>
                <Badge
                  classes={{ colorAccent: classNames(classes.badgeColor, { [classes.badgeColorSelected]: open }) }}
                  badgeContent={<Icon className="mdi-set mdi-lock" />}
                  color="accent"
                />
              </ListItemSecondaryAction>}
          </ListItem>
        }
      >
        <IdeaPopover id={node.id} onActionClick={this.closeMenu} onFormOpened={this.hideMenu} onFormClosed={this.showMenu} />
      </Menu>
    );
  }
}

export const mapStateToProps = (state, props) => {
  return {
    edit: state.form[`${props.node.id}-edit`],
    site: state.globalProps.site
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(DumbIdeaListingItem));