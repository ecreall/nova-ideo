/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
import CheckBoxIcon from '@material-ui/icons/CheckBox';
import classNames from 'classnames';

import { ListItem } from '../../../styledComponents/List';

const styles = {
  listItem: {
    paddingTop: '5px !important',
    marginLeft: '0 !important',
    paddingBottom: '5px !important',
    borderRadius: '0 !important'
  },
  listItemActive: {
    backgroundColor: '#a7a7a7',
    '&:hover': {
      backgroundColor: '#a7a7a7'
    }
  },
  iconSelected: {
    color: 'white'
  }
};

export class DumbSelectItem extends React.Component {
  render() {
    const {
      node, itemProps: {
        Item, selected, onSelect, onDeselect
      }, classes, theme
    } = this.props;
    const isSelected = selected.includes(node.id);
    const onClick = isSelected ? onDeselect : onSelect;
    return (
      <ListItem
        dense
        button
        onClick={() => {
          return onClick(node);
        }}
        ContainerComponent="div"
        hoverColor={theme.palette.info[500]}
        classes={{
          root: classNames(classes.listItem, { [classes.listItemActive]: isSelected })
        }}
      >
        <Item node={node} isSelected={isSelected} />
        <ListItemSecondaryAction
          onClick={() => {
            return onClick(node);
          }}
        >
          {isSelected ? (
            <CheckBoxIcon className={classNames('menu-item-text', classes.iconSelected)} />
          ) : (
            <CheckBoxOutlineBlankIcon className="menu-item-text" />
          )}
        </ListItemSecondaryAction>
      </ListItem>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbSelectItem);