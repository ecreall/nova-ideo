import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Divider from '@material-ui/core/Divider';

import UserContents from './UserContents';
import UserEvaluations from './UserEvaluations';
import UserFollowings from './UserFollowings';
import { STYLE_CONST } from '../../../constants';

const styles = {
  list: {
    display: 'flex',
    flexDirection: 'column',
    width: STYLE_CONST.drawerWidth,
    height: '100%',
    marginTop: 15
  },
  divider: {
    marginBottom: 10
  }
};

const CONTENTS_IDS = {
  contents: 'contents',
  evaluation: 'evaluation',
  following: 'following'
};

export class DumbContents extends React.Component {
  state = {
    expanded: CONTENTS_IDS.contents
  };

  onOpen = (id) => {
    const { expanded } = this.state;
    const isCurrent = expanded === id;
    this.setState({ expanded: !isCurrent && id });
  };

  render() {
    const { classes } = this.props;
    const { expanded } = this.state;
    return (
      <div className={classes.list}>
        <UserContents id={CONTENTS_IDS.contents} open={expanded === CONTENTS_IDS.contents} onOpen={this.onOpen} />
        <Divider className={classes.divider} light />
        <UserEvaluations id={CONTENTS_IDS.evaluation} open={expanded === CONTENTS_IDS.evaluation} onOpen={this.onOpen} />
        <Divider className={classes.divider} light />
        <UserFollowings id={CONTENTS_IDS.following} open={expanded === CONTENTS_IDS.following} onOpen={this.onOpen} />
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbContents);