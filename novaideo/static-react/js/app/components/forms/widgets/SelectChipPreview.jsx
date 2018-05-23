import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Chip from '@material-ui/core/Chip';

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

export const DumbSelectChipPreview = ({ classes, items, onItemDelete }) => {
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
};

export default withStyles(styles)(DumbSelectChipPreview);