/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';

import { MenuList as StyledMenuList, MenuItem } from '../../styledComponents/Menu';
import { ListItemIcon, ListItemText } from '../../styledComponents/List';
import Divider from './Divider';

const styles = {
  section: {
    position: 'relative',
    paddingTop: 16,
    paddingBottom: 15,
    margin: 0,
    width: '100%',
    clear: 'both',
    borderBottom: '1px solid rgba(0,0,0,.15)'
  },
  sectionHeader: {
    height: 40,
    margin: '6px 22px'
  },
  menuSection: {
    paddingTop: '0 !important',
    paddingBottom: '0 !important'
  }
};

export function renderMenuItem({
  Icon, title, onClick, color, hoverColor
}) {
  return (
    <MenuItem onClick={onClick} hoverColor={hoverColor}>
      {Icon && (
        <ListItemIcon iconColor={color}>
          <Icon className="menu-item-icon" />
        </ListItemIcon>
      )}
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

export class DumbMenuList extends React.Component {
  renderItem = (field) => {
    const { theme, close } = this.props;
    if (typeof field === 'string') {
      return <Divider title={field} />;
    }

    if (typeof field === 'function') {
      return <div onClick={close}>{field()}</div>;
    }
    const Icon = field.Icon;
    return renderMenuItem({
      Icon: Icon,
      title: field.title,
      color: field.color,
      hoverColor: field.hoverColor || theme.palette.info[500],
      onClick: (event) => {
        close(event, field.onClick);
      }
    });
  };

  render() {
    const { header, fields, classes } = this.props;
    return (
      <div className={classNames({ [classes.section]: header, 'menu-section': header })}>
        {header && <div className={classes.sectionHeader}>{header}</div>}
        <StyledMenuList className={header && classes.menuSection} role="menu">
          {fields.map((field) => {
            return this.renderItem(field);
          })}
        </StyledMenuList>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbMenuList);