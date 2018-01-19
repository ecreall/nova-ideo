/* eslint-disable react/no-array-index-key, no-confusing-arrow */
/* eslint-disable no-param-reassign */
import React from 'react';
import classNames from 'classnames';
import IconButton from 'material-ui/IconButton';
import { MenuItem, MenuList } from 'material-ui/Menu';
import Grow from 'material-ui/transitions/Grow';
import Paper from 'material-ui/Paper';
import { Manager, Target, Popper } from 'react-popper';
import ClickAwayListener from 'material-ui/utils/ClickAwayListener';
import { ListItemText } from 'material-ui/List';
import Checkbox from 'material-ui/Checkbox';
import { withStyles } from 'material-ui/styles';
import TextField from 'material-ui/TextField';

const styles = {
  popperClose: {
    pointerEvents: 'none'
  },
  popper: {
    zIndex: 3
  },
  paper: {
    borderRadius: 6,
    border: '1px solid rgba(0,0,0,.15)'
  },
  menuItem: {
    paddingTop: 0,
    paddingBottom: 0,
    height: 'auto',
    '&:hover': {
      backgroundColor: 'transparent'
    }
  },
  button: {
    width: 40,
    height: 40,
    color: ' #a3a3a3'
  },
  searchRoot: {
    padding: '5px 15px',
    backgroundColor: 'whitesmoke',
    borderBottom: 'solid 1px rgba(191, 191, 191, 0.42)'
  },
  search: {
    backgroundColor: 'white',
    border: 'solid 1px #bfbfbf',
    borderRadius: 12,
    padding: '5px 10px'
  }
};

class Select extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      menu: false,
      options: this.props.options,
      selected: this.props.value ? Object.keys(this.props.value) : [],
      searchText: ''
    };
  }

  componentDidMount() {
    if (this.props.initRef) {
      this.props.initRef(this);
    }
  }

  onChangeSearchText = (event) => {
    this.setState({
      searchText: event.target.value
    });
  };

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

  addOption(text) {
    this.setState(
      {
        options: { ...{ [text]: text }, ...this.state.options },
        selected: [text, ...this.state.selected]
      },
      () => {
        return this.props.onChange(this.getSelected());
      }
    );
  }

  getSelected = () => {
    const { options, selected } = this.state;
    return Object.keys(options).reduce((filtered, id) => {
      if (selected.includes(id)) filtered[id] = options[id];
      return filtered;
    }, {});
  };

  openMenu = () => {
    this.setState({ menu: true });
  };

  closeMenu = () => {
    this.setState({ menu: false });
  };

  render() {
    const { label, classes } = this.props;
    const { options, searchText } = this.state;
    const optionsResult = Object.keys(options).reduce((filtered, id) => {
      const title = options[id];
      if (title.toLowerCase().search(searchText) >= 0) filtered[id] = title;
      return filtered;
    }, {});
    const { menu } = this.state;
    return (
      <Manager>
        <Target>
          <IconButton className={classes.button} aria-owns={'menu-list'} aria-haspopup="true" onClick={this.openMenu}>
            {label}
          </IconButton>
        </Target>
        <Popper
          placement="top-start"
          eventsEnabled={menu}
          className={classNames(classes.popper, { [classes.popperClose]: !menu })}
        >
          <ClickAwayListener onClickAway={this.closeMenu}>
            <Grow in={menu} id="menu-list" style={{ transformOrigin: '0 0 0' }}>
              <Paper elevation={6} className={classes.paper}>
                <TextField
                  value={this.state.searchText}
                  onChange={this.onChangeSearchText}
                  placeholder="Search"
                  InputProps={{
                    disableUnderline: true,
                    classes: {
                      root: classes.searchRoot,
                      input: classes.search
                    }
                  }}
                  InputLabelProps={{
                    shrink: true
                  }}
                />
                <MenuList role="menu">
                  {Object.keys(optionsResult).map((id) => {
                    const title = optionsResult[id];
                    return (
                      <MenuItem
                        onClick={() => {
                          this.toggleOption(!this.state.selected.includes(id), id);
                        }}
                        ey={id}
                        value={id}
                      >
                        <Checkbox checked={this.state.selected.includes(id)} />
                        <ListItemText primary={title} />
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

export default withStyles(styles, { withTheme: true })(Select);