/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';

import ChannelItem from './ChannelItem';
import FlatList from '../../common/FlatList';
import { channelsQuery } from '../../../graphql/queries';

const styles = {
  list: {
    height: 'calc(50% - 64px)'
  },
  thumbVertical: {
    backgroundColor: 'rgba(255, 255, 255, 0.22)',
    border: 'none'
  }
};

export class DumbPublicChannels extends React.Component {
  render() {
    const { data, classes } = this.props;
    return (
      <FlatList
        customScrollbar
        data={data}
        getEntities={(entities) => {
          return entities.account && entities.account.channels;
        }}
        ListItem={ChannelItem}
        progressStyle={{ size: 20, color: 'white' }}
        className={classes.list}
        classes={{ thumbVertical: classes.thumbVertical }}
      />
    );
  }
}

export default withStyles(styles)(
  graphql(channelsQuery, {
    options: () => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: { first: 25, after: '' }
      };
    }
  })(DumbPublicChannels)
);