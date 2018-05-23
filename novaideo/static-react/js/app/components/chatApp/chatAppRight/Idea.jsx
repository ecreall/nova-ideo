import React from 'react';
import { withStyles } from '@material-ui/core/styles';

import Idea from '../../idea/IdeaPopover';

const styles = {
  container: {
    maxWidth: 'inherit'
  }
};

const DumbIdea = ({ subject, onActionClick, classes }) => {
  return <Idea id={subject} onActionClick={onActionClick} classes={{ container: classes.container }} />;
};

export default withStyles(styles)(DumbIdea);