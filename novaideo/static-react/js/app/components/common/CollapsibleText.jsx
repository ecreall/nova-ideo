/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

import { truncateText } from '../../utils/globalFunctions';

const styles = {
  icon: {},
  btn: {
    height: 22,
    width: 22
  }
};

export class DumbCollapsibleText extends React.Component {
  state = {
    open: false
  };

  open = () => {
    this.setState({ open: true });
  };

  close = () => {
    this.setState({ open: false });
  };

  render() {
    const { text, className, textLen, classes } = this.props;
    const { open } = this.state;
    const smallText = !text || text.length <= textLen;
    return (
      <div className={className}>
        {smallText || open ? text : truncateText(text, textLen)}
        {!smallText && (
          <IconButton onClick={open ? this.close : this.open} className={classes.btn}>
            {open ? <ExpandLessIcon className={classes.icon} /> : <ExpandMoreIcon className={classes.icon} />}
          </IconButton>
        )}
      </div>
    );
  }
}

export default withStyles(styles)(DumbCollapsibleText);