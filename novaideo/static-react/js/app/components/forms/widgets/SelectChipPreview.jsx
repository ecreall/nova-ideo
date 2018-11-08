import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Chip from '@material-ui/core/Chip';

const styles = {
  chipContainer: {
    display: 'flex',
    padding: '5px 0px 10px'
  },
  chip: {
    marginRight: 5,
    color: 'rgb(107, 107, 107)'
  }
};

export const DumbSelectChipPreview = ({
  classes, items, onItemDelete, icon
}) => {
  return (
    <div className={classes.chipContainer}>
      {Object.keys(items).map((id) => {
        const option = items[id];
        return (
          <Chip
            label={option}
            icon={icon}
            onDelete={
              onItemDelete
                ? () => {
                  onItemDelete(id);
                }
                : null
            }
            className={classes.chip}
          />
        );
      })}
    </div>
  );
};

export default withStyles(styles)(DumbSelectChipPreview);