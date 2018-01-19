import React from 'react';
import { withStyles } from 'material-ui/styles';
import Chip from 'material-ui/Chip';

const styles = {
  chipContainer: {
    display: 'flex',
    padding: 5
  },
  chip: {
    marginRight: 5,
    color: 'rgb(107, 107, 107)'
  }
};

class SelectChipPreview extends React.Component {
  render() {
    const { classes, items, onItemDelete } = this.props;
    return (
      <div className={classes.chipContainer}>
        {Object.keys(items).map((id) => {
          const option = items[id];
          return (
            <Chip
              label={option}
              onDelete={() => {
                onItemDelete(id);
              }}
              className={classes.chip}
            />
          );
        })}
      </div>
    );
  }
}

export default withStyles(styles)(SelectChipPreview);