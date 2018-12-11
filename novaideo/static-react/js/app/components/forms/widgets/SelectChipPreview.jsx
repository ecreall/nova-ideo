import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Chip from '@material-ui/core/Chip';
import Avatar from '@material-ui/core/Avatar';

const styles = {
  chipContainer: {
    padding: '5px 0px 10px'
  },
  chip: {
    marginRight: 5,
    marginTop: 10,
    color: 'rgb(107, 107, 107)'
  }
};

export const DumbSelectChipPreview = ({
  classes, items, onItemDelete, icon, variant
}) => {
  return (
    <div className={classes.chipContainer}>
      {items.map((item) => {
        const { id, label, picture } = item;
        return (
          <Chip
            label={label}
            avatar={picture ? <Avatar alt={label} src={picture.url} /> : null}
            icon={icon}
            onDelete={
              onItemDelete
                ? () => {
                  return onItemDelete(id);
                }
                : null
            }
            className={classes.chip}
            variant={variant || 'default'}
          />
        );
      })}
    </div>
  );
};

export default withStyles(styles)(DumbSelectChipPreview);