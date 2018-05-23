// @flow

import React from 'react';
import { withStyles } from '@material-ui/core/styles';

import Informations from './Informations';
import Pinned from './Pinned';
import Files from './Files';
import Members from './Members';
import { CONTENTS_IDS } from '.';

const styles = {
  container: {
    height: '100%',
    backgroundColor: '#fff'
  }
};

class Details extends React.Component {
  onOpen = (id) => {
    const { componentId, updateRight } = this.props;
    const isCurrent = componentId === id;
    updateRight({ open: true, componentId: isCurrent ? CONTENTS_IDS.details : id });
  };

  render() {
    const { classes, componentId } = this.props;
    return (
      <div className={classes.container}>
        <Informations {...this.props} id={CONTENTS_IDS.info} open={componentId === CONTENTS_IDS.info} onOpen={this.onOpen} />
        <Pinned {...this.props} id={CONTENTS_IDS.pinned} open={componentId === CONTENTS_IDS.pinned} onOpen={this.onOpen} />
        <Files {...this.props} id={CONTENTS_IDS.files} open={componentId === CONTENTS_IDS.files} onOpen={this.onOpen} />
        <Members {...this.props} id={CONTENTS_IDS.members} open={componentId === CONTENTS_IDS.members} onOpen={this.onOpen} />
      </div>
    );
  }
}

export default withStyles(styles)(Details);