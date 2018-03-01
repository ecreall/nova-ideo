/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';

import ChannelItem from './ChannelItem';
import FlatList from '../common/FlatList';
import { discussionsQuery } from '../../graphql/queries';

const styles = {
  list: {
    height: 'calc(50% - 64px)'
  },
  thumbVertical: {
    backgroundColor: 'rgba(255, 255, 255, 0.22)',
    border: 'none'
  }
};
export class DumbPrivateChannels extends React.Component {
  render() {
    const { data, classes } = this.props;
    return (
      <FlatList
        customScrollbar
        data={data}
        getEntities={(entities) => {
          return entities.account && entities.account.discussions;
        }}
        ListItem={ChannelItem}
        itemProps={{ isDiscussion: true }}
        className={classes.list}
        progressStyle={{ size: 20, color: 'white' }}
        classes={{ thumbVertical: classes.thumbVertical }}
      />
    );
  }
}

export default withStyles(styles)(
  graphql(discussionsQuery, {
    options: () => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: { first: 25, after: '' }
      };
    }
  })(DumbPrivateChannels)
);