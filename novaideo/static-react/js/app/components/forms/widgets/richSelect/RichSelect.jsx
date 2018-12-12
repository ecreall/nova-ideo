import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import AddCircleOutlineIcon from '@material-ui/icons/AddCircleOutline';
import IconButton from '@material-ui/core/IconButton';

import Dialog from '../../../common/Dialog';
import SearchList from './SearchList';
import SelectChipPreview from '../SelectChipPreview';

const styles = {
  container: {
    padding: '0px 25px 20px',
    width: '100%',
    fontSize: 17,
    lineHeight: 1.5
  },
  control: {
    display: 'flex',
    alignItems: 'flex-end',
    marginBottom: 10
  },
  placeholder: {
    color: 'gray',
    height: 32
  },
  titleContainer: {
    fontWeight: 900
  },
  title: {
    marginLeft: 5
  }
};

export class DumbRichSelect extends React.Component {
  state = {
    open: false,
    items: this.props.value || []
  };

  handleOpen = () => {
    this.setState({ open: true });
    // preventDefault
    return false;
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  selectItem = (item) => {
    const { items } = this.state;
    const { onChange } = this.props;
    const current = [...items, item];
    this.setState({ items: current }, () => {
      return onChange(current);
    });
  };

  deselectItem = (id) => {
    const { items } = this.state;
    const { onChange } = this.props;
    const current = [...items];
    const currentItem = items.find((item) => {
      return item.id === id;
    });
    if (currentItem) {
      current.splice(current.indexOf(currentItem), 1);
    }
    this.setState({ items: current }, () => {
      return onChange(current);
    });
  };

  render() {
    const {
      id, query, getData, Item, classes, placeholder
    } = this.props;
    const { open, items } = this.state;
    const hasItems = items.length > 0;
    return (
      <React.Fragment>
        <div className={classes.control}>
          {hasItems ? (
            <SelectChipPreview
              items={items.map((item) => {
                return { id: item.id, label: item.title, picture: item.picture };
              })}
              variant="outlined"
              onItemDelete={this.deselectItem}
            />
          ) : (
            <div className={classes.placeholder}>{placeholder}</div>
          )}
          <IconButton color="primary" className={classes.button} component="span" onClick={this.handleOpen}>
            <AddCircleOutlineIcon />
          </IconButton>
        </div>
        {open && (
          <Dialog
            directDisplay
            appBar={(
              <div className={classes.titleContainer}>
                <span className={classes.title}>{placeholder}</span>
              </div>
            )}
            open={open}
            onClose={this.handleClose}
          >
            <div className={classes.container}>
              <SearchList
                id={id}
                selected={items.map((item) => {
                  return item.id;
                })}
                query={query}
                getData={getData}
                Item={Item}
                onItemSelect={this.selectItem}
                onItemDeselect={(item) => {
                  return this.deselectItem(item.id);
                }}
                onValidate={this.handleClose}
              />
            </div>
          </Dialog>
        )}
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(DumbRichSelect);