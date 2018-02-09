import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';

import ChannelNavbar from './channels/Navbar';
import App from './common/App';
import { channelQuery } from '../graphql/queries';
import { updateApp } from '../actions/actions';
import Comments from './channels/Comments';

export class DumbChatApp extends React.Component {
  componentWillReceiveProps(nextProps) {
    const { data: { node }, subject } = nextProps;
    const subjectId = node && node.subject.id;
    if (subjectId !== subject) {
      this.props.updateApp('chatApp', { subject: subjectId });
    }
  }

  render() {
    const { data, active, channel, left } = this.props;
    const channelData = data.node ? data.node : null;
    return (
      <App active={active} left={left} Navbar={ChannelNavbar} data={{ channel: channelData }}>
        <Comments id="comments" customScrollbar autoFocus reverted channel={channel} />
      </App>
    );
  }
}

export const mapDispatchToProps = {
  updateApp: updateApp
};

export const mapStateToProps = (state) => {
  return {
    channel: state.apps.chatApp.channel,
    subject: state.apps.chatApp.subject
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(
  graphql(channelQuery, {
    options: (props) => {
      return {
        notifyOnNetworkStatusChange: true,
        variables: {
          id: props.channel
        }
      };
    }
  })(DumbChatApp)
);