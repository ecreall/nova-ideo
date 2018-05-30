/* eslint-disable react/no-array-index-key, no-confusing-arrow */
/* eslint-disable no-param-reassign */
import React from 'react';
import { I18n } from 'react-redux-i18n';
import classNames from 'classnames';
import IconButton from '@material-ui/core/IconButton';
import MenuList from '@material-ui/core/MenuList';
import MenuItem from '@material-ui/core/MenuItem';
import Grow from '@material-ui/core/Grow';
import Paper from '@material-ui/core/Paper';
import { Manager, Target, Popper } from 'react-popper';
import ClickAwayListener from '@material-ui/core/ClickAwayListener';
import ListItemText from '@material-ui/core/ListItemText';
import Checkbox from '@material-ui/core/Checkbox';
import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputAdornment from '@material-ui/core/InputAdornment';
import SearchIcon from '@material-ui/icons/Search';

const styles = (theme) => {
  return {
    popperClose: {
      pointerEvents: 'none'
    },
    popper: {
      zIndex: 1100
    },
    paper: {
      borderRadius: 10,
      border: '1px solid rgba(0,0,0,.15)'
    },
    searchRoot: {
      padding: 10,
      backgroundColor: 'whitesmoke',
      borderBottom: 'solid 1px rgba(191, 191, 191, 0.42)',
      borderTopRightRadius: 10,
      borderTopLeftRadius: 10
    },
    search: {
      backgroundColor: 'white',
      border: '1px solid #a0a0a2',
      borderRadius: 4,
      boxShadow: 'inset 0 1px 1px rgba(0,0,0,.075)',
      alignItems: 'center',
      height: 35
    },
    input: {
      padding: '10px 10px 10px',
      fontSize: 15,
      '&::placeholder': {
        color: '#000',
        fontSize: 15,
        fontWeight: 400,
        opacity: '.375'
      }
    },
    newOptionLi: {
      backgroundColor: theme.palette.tertiary.color
    },
    newOption: {
      color: theme.palette.tertiary.hover.color
    },
    menuItem: {
      paddingLeft: 0,
      borderRadius: 3
    }
  };
};

export class DumbSelectList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      options: props.options,
      selected: props.value ? Object.keys(props.value) : []
    };
  }

  componentDidMount() {
    if (this.props.initRef) {
      this.props.initRef(this);
    }
  }

  toggleOption = (checked, id) => {
    const selected = [...this.state.selected];
    if (checked && !selected.includes(id)) {
      selected.push(id);
    } else if (!checked && selected.includes(id)) {
      selected.splice(selected.indexOf(id), 1);
    }
    this.setState(
      {
        selected: selected
      },
      () => {
        return this.props.onChange(this.getSelected());
      }
    );
  };

  getSelected = () => {
    const { options, selected } = this.state;
    return Object.keys(options).reduce((filtered, id) => {
      if (selected.includes(id)) filtered[id] = options[id];
      return filtered;
    }, {});
  };

  render() {
    const { label, classes } = this.props;
    const { options } = this.state;
    return (
      <MenuList role="menu">
        {Object.keys(options).map((id) => {
          const title = options[id];
          return (
            <MenuItem
              className={classes.menuItem}
              onClick={() => {
                this.toggleOption(!this.state.selected.includes(id), id);
              }}
              key={id}
              value={id}
            >
              <Checkbox checked={this.state.selected.includes(id)} />
              <ListItemText primary={title} />
            </MenuItem>
          );
        })}
      </MenuList>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbSelectList);