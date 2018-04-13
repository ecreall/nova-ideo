/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from 'material-ui/styles';

import ChannelItem from './ChannelItem';
import FlatList from '../../common/FlatList';
import Channels from '../../../graphql/queries/Channels.graphql';

const styles = {
  list: {
    height: 'calc(50% - 64px)'
  },
  thumbVertical: {
    backgroundColor: 'rgba(255, 255, 255, 0.22)',
    border: 'none'
  }
};

export const DumbPublicChannels = ({ classes }) => {
  return (
    <Query notifyOnNetworkStatusChange fetchPolicy="cache-and-network" query={Channels} variables={{ first: 25, after: '' }}>
      {(data) => {
        return (
          <FlatList
            customScrollbar
            data={data}
            getEntities={(entities) => {
              return entities.data ? entities.data.account && entities.data.account.channels : entities.account.channels;
            }}
            ListItem={ChannelItem}
            progressStyle={{ size: 20, color: 'white' }}
            className={classes.list}
            classes={{ thumbVertical: classes.thumbVertical }}
          />
        );
      }}
    </Query>
  );
};

export default withStyles(styles)(DumbPublicChannels);