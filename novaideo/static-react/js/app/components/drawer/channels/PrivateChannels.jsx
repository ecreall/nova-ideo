/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from 'material-ui/styles';

import ChannelItem from './ChannelItem';
import FlatList from '../../common/FlatList';
import Discussions from '../../../graphql/queries/Discussions.graphql';

const styles = {
  list: {
    height: 'calc(50% - 64px)'
  },
  thumbVertical: {
    backgroundColor: 'rgba(255, 255, 255, 0.22)',
    border: 'none'
  }
};

export const DumbPrivateChannels = ({ classes }) => {
  return (
    <Query notifyOnNetworkStatusChange fetchPolicy="cache-and-network" query={Discussions} variables={{ first: 25, after: '' }}>
      {(data) => {
        return (
          <FlatList
            customScrollbar
            data={data}
            getEntities={(entities) => {
              return entities.data ? entities.data.account && entities.data.account.discussions : entities.account.discussions;
            }}
            ListItem={ChannelItem}
            itemProps={{ isDiscussion: true }}
            className={classes.list}
            progressStyle={{ size: 20, color: 'white' }}
            classes={{ thumbVertical: classes.thumbVertical }}
          />
        );
      }}
    </Query>
  );
};

export default withStyles(styles)(DumbPrivateChannels);