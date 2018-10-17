import React from 'react';
import IconButtonBase from '@material-ui/core/IconButton';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  label: {
    height: 0
  }
};

const IconButton = (props) => {
  return <IconButtonBase {...props} />;
};

export default withStyles(styles)(IconButton);