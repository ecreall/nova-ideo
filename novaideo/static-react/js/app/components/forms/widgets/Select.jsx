/* eslint-disable no-param-reassign */
import React from 'react';
import Input, { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { ListItemText } from 'material-ui/List';
import SelectMUI from 'material-ui/Select';
import Checkbox from 'material-ui/Checkbox';
import { withStyles } from 'material-ui/styles';
import { FormControl } from 'material-ui/Form';
import TextField from 'material-ui/TextField';

const styles = {
  container: {
    marginTop: 15
  },
  search: {
    border: 'solid 1px #8080808a',
    borderRadius: '10px',
    padding: '5px 7px',
    margin: '6px 20px',
    backgroundColor: 'white'
  },
  searchRoot: {
    backgroundColor: '#e0e0e0'
  }
};

const MenuProps = {
  MenuListProps: {
    style: {
      padding: 0
    }
  }
};

class Select extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      options: this.props.options,
      selected: this.props.value ? Object.keys(this.props.value) : [],
      searchText: ''
    };
  }

  onChangeSearchText = (event) => {
    this.setState({
      searchText: event.target.value
    });
  };

  toggleOption = (event) => {
    this.setState(
      {
        selected: event.target.value
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

  render() {
    const { label, classes } = this.props;
    const { options, searchText } = this.state;
    const optionsResult = Object.keys(options).reduce((filtered, id) => {
      const title = options[id];
      if (title.toLowerCase().search(searchText) >= 0) filtered[id] = title;
      return filtered;
    }, {});
    return (
      <div style={styles.container}>
        <FormControl>
          <InputLabel htmlFor="tag-multiple">
            {label}
          </InputLabel>
          <SelectMUI
            multiple
            value={this.state.selected}
            onChange={this.toggleOption}
            input={<Input id="tag-multiple" />}
            renderValue={(selected) => {
              return selected.join(', ');
            }}
            MenuProps={MenuProps}
          >
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

            {Object.keys(optionsResult).map((id) => {
              const title = optionsResult[id];
              return (
                <MenuItem key={id} value={id}>
                  <Checkbox checked={this.state.selected.includes(id)} />
                  <ListItemText primary={title} />
                </MenuItem>
              );
            })}
          </SelectMUI>
        </FormControl>
      </div>
    );
  }
}

export default withStyles(styles)(Select);