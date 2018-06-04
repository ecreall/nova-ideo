/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';

const styles = {
  divider: {
    position: 'relative',
    minHeight: 1,
    backgroundColor: '#ddd',
    margin: '17px 14px'
  },
  full: {
    margin: '17px 0 !important'
  },
  title: {
    position: 'absolute',
    left: 0,
    backgroundColor: 'white',
    top: -8,
    fontSize: 13,
    color: '#717274',
    cursor: 'default',
    paddingRight: 12
  }
};

export const DumbDivider = ({ title, classes }) => {
  return (
    <div className={classNames(classes.divider, { [classes.full]: !title })}>
      {title && <div className={classes.title}>{title}</div>}
    </div>
  );
};

export default withStyles(styles)(DumbDivider);