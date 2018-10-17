import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';

import ChannelNavbar from './Navbar';
import App from '../common/App';
import Channel from '../../graphql/queries/Channel.graphql';
import { updateChatApp } from '../../actions/chatAppActions';
import Comments from './Comments';

export class DumbChatApp extends React.Component {
  componentWillReceiveProps(nextProps) {
    const { data: { node }, subject } = nextProps;
    const { updateChatAppSubject } = this.props;
    const subjectId = node && node.subject && node.subject.id;
    if (subjectId !== subject) {
      updateChatAppSubject({ subject: subjectId });
    }
  }

  render() {
    const {
      data, active, channel, left
    } = this.props;
    const channelData = data.node ? data.node : null;
    return (
      <App active={active} left={left} Navbar={ChannelNavbar} data={{ channel: channelData }}>
        <Comments customScrollbar reverted channelId={channel} formProps={{ autoFocus: true }} />
      </App>
    );
  }
}

export const mapDispatchToProps = {
  updateChatAppSubject: updateChatApp
};

export const mapStateToProps = (state) => {
  return {
    channel: state.apps.chatApp.channel,
    subject: state.apps.chatApp.subject
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(
  graphql(Channel, {
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