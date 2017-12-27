/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';

import ChannelItem from './ChannelItem';
import EntitiesList from '../common/EntitiesList';
import { discussionsQuery } from '../../graphql/queries';

export class DumbPrivateChannels extends React.Component {
  render() {
    const { data } = this.props;
    return (
      <EntitiesList
        data={data}
        getEntities={(entities) => {
          return entities.account ? entities.account.discussions : [];
        }}
        noContentIcon="comment-outline"
        noContentMessage={'noPrivateDiscussions'}
        ListItem={ChannelItem}
        itemdata={{ isDiscussion: true }}
        style={{
          height: '50%'
        }}
        itemHeightEstimation={30}
        progressStyle={{ size: 20, color: 'white' }}
        activityIndicatorColor="white"
      />
    );
  }
}

export default graphql(discussionsQuery, {
  options: () => {
    return {
      fetchPolicy: 'cache-and-network',
      notifyOnNetworkStatusChange: true,
      variables: { first: 15, after: '' }
    };
  }
})(DumbPrivateChannels);