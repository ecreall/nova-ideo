import React from 'react';
import Icon from '@material-ui/core/Icon';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  containerStyle: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'baseline'
  },
  styleText: {
    fontSize: 15,
    color: '#a0a0a2'
  },
  styleIcon: {
    fontSize: 15,
    color: '#a0a0a2'
  }
};

export const DumbIconWithText = ({ name, text, containerStyle, styleText, styleIcon, classes }) => {
  return (
    <div className={classNames(classes.containerStyle, containerStyle)}>
      <Icon className={classNames(classes.styleIcon, styleIcon, name)} />
      <span className={classNames(classes.styleText, styleText)}>
        {text}
      </span>
    </div>
  );
};

export default withStyles(styles)(DumbIconWithText);