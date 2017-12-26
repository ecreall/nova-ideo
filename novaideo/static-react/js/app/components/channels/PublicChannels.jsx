/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';

import ChannelItem from './ChannelItem';
import EntitiesList from '../common/EntitiesList';
import { channelsQuery } from '../../graphql/queries';

export class DumbPublicChannels extends React.Component {
  render() {
    const { data, listStyle } = this.props;
    return (
      <EntitiesList
        data={data}
        getEntities={(entities) => {
          return entities.account ? entities.account.channels : [];
        }}
        noContentIcon="comment-outline"
        noContentMessage={'noChannels'}
        ListItem={ChannelItem}
        style={listStyle}
        itemHeightEstimation={30}
        activityIndicatorColor="white"
      />
    );
  }
}

export default graphql(channelsQuery, {
  options: () => {
    return {
      fetchPolicy: 'cache-and-network',
      notifyOnNetworkStatusChange: true,
      variables: { first: 15, after: '' }
    };
  }
})(DumbPublicChannels);