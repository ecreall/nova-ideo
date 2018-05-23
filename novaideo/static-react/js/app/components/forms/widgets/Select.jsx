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
    menuItem: {
      paddingTop: 0,
      paddingBottom: 0,
      height: 'auto',
      '&:hover': {
        backgroundColor: 'transparent'
      }
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
    }
  };
};

export class DumbSelect extends React.Component {
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
        searchText: '',
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
    const { label, canAdd, classes } = this.props;
    const { options, searchText } = this.state;
    let exactMatch = false;
    const optionsResult = Object.keys(options).reduce((filtered, id) => {
      const title = options[id];
      const titleToSearch = searchText.toLowerCase().trim();
      const formattedTitle = title.toLowerCase().trim();
      if (!exactMatch) {
        exactMatch = titleToSearch === formattedTitle;
      }
      if (formattedTitle.search(titleToSearch) >= 0) filtered[id] = title;
      return filtered;
    }, {});
    const { menu } = this.state;
    return (
      <Manager>
        <Target>
          <div onClick={this.openMenu}>
            {label}
          </div>
        </Target>
        <Popper placement="bottom" eventsEnabled={menu} className={classNames(classes.popper, { [classes.popperClose]: !menu })}>
          <ClickAwayListener onClickAway={this.closeMenu}>
            <Grow in={menu} id="menu-list" style={{ transformOrigin: '0 0 0' }}>
              <Paper elevation={6} className={classes.paper}>
                <div className={classes.searchRoot}>
                  <Input
                    disableUnderline
                    value={this.state.searchText}
                    onChange={this.onChangeSearchText}
                    placeholder={canAdd ? I18n.t('forms.searchOrAdd') : I18n.t('forms.search')}
                    classes={{
                      root: classes.search,
                      input: classes.input
                    }}
                    endAdornment={
                      <InputAdornment position="start">
                        <IconButton>
                          <SearchIcon />
                        </IconButton>
                      </InputAdornment>
                    }
                  />
                </div>
                <MenuList role="menu">
                  {searchText &&
                    canAdd &&
                    !exactMatch &&
                    <MenuItem
                      onClick={() => {
                        this.addOption(searchText);
                      }}
                      classes={{
                        root: classes.newOptionLi
                      }}
                      value={searchText}
                    >
                      <Checkbox
                        classes={{
                          default: classes.newOption,
                          checked: classes.newOption
                        }}
                      />
                      <ListItemText
                        classes={{
                          primary: classes.newOption
                        }}
                        primary={searchText}
                      />
                    </MenuItem>}
                  {Object.keys(optionsResult).map((id) => {
                    const title = optionsResult[id];
                    return (
                      <MenuItem
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
              </Paper>
            </Grow>
          </ClickAwayListener>
        </Popper>
      </Manager>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbSelect);