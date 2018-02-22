/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';

import Comments from '../Comments';

const styles = {
  container: {
    height: '100%'
  }
};

class Search extends React.Component {
  render() {
    const { channel, classes } = this.props;
    return (
      <Comments
        rightDisabled
        customScrollbar
        dynamicDivider={false}
        displayForm={false}
        channelId={channel.id}
        filter={{ pinned: true }}
        classes={{ container: classes.container, list: classes.container }}
      />
    );
  }
}

export default withStyles(styles)(Search);