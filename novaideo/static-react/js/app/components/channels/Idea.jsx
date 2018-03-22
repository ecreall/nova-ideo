/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from 'material-ui/styles';

import Idea from '../idea/IdeaPopover';

const styles = {
  container: {
    maxWidth: 'inherit'
  }
};

export class DumbIdea extends React.Component {
  render() {
    const { classes } = this.props;
    const { subject, onActionClick } = this.props;
    return <Idea id={subject} onActionClick={onActionClick} classes={{ container: classes.container }} />;
  }
}

export default withStyles(styles)(DumbIdea);