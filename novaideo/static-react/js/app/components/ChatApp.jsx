import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';

import ChannelNavbar from './channels/Navbar';
import App from './common/App';
import { commentsQuery } from '../graphql/queries';
import EntitiesList from './common/EntitiesList';
import CommentItem from './channels/CommentItem';

const commentsActions = ['comment', 'general_discuss', 'discuss'];

export class DumbChatApp extends React.Component {
  render() {
    const { data, active, left } = this.props;
    const channelData = data.node ? data.node : null;
    return (
      <App active={active} left={left} Navbar={ChannelNavbar} data={{ channel: channelData }}>
        <EntitiesList
          data={data}
          getEntities={(entities) => {
            return entities.node ? entities.node.comments : undefined;
          }}
          noContentIcon="comment-outline"
          noContentMessage={'noComment'}
          offlineFilter={(entity, text) => {
            return entity.node.text.toLowerCase().search(text) >= 0;
          }}
          ListItem={CommentItem}
          itemdata={{
            channel: channelData
          }}
          itemHeightEstimation={120}
          style={{
            height: 'calc(95vh - 56px)'
          }}
          scrollbarStyle={{
            display: 'flex',
            flexDirection: 'column-reverse'
          }}
        />
      </App>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    channel: state.apps.chatApp.channel
  };
};

export default connect(mapStateToProps)(
  graphql(commentsQuery, {
    options: (props) => {
      return {
        notifyOnNetworkStatusChange: true,
        variables: {
          first: 15,
          after: '',
          filter: '',
          id: props.channel,
          processId: '',
          nodeIds: commentsActions
        }
      };
    }
  })(DumbChatApp)
);