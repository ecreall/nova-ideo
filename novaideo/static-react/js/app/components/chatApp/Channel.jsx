import React from 'react';
import { connect } from 'react-redux';

import { openChatApp } from '../../actions/chatAppActions';

class Channel extends React.Component {
  constructor(props) {
    super(props);
    this.openChannel(this.props);
  }

  componentWillReceiveProps(nextProps) {
    this.openChannel(nextProps);
  }

  openChannel = (props) => {
    const {
      params: { channelId },
      location: { query }
    } = props;
    if (channelId) {
      const { smallScreen } = props;
      const toOpen = query && query.right;
      const rightOpen = toOpen
        ? {
          right: {
            open: !smallScreen,
            componentId: toOpen
          }
        }
        : {};
      this.props.openChatApp({
        channel: channelId,
        ...rightOpen
      });
    }
  };

  render() {
    return null;
  }
}

export const mapDispatchToProps = {
  openChatApp: openChatApp
};

export const mapStateToProps = (state) => {
  return {
    smallScreen: state.globalProps.smallScreen
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Channel);