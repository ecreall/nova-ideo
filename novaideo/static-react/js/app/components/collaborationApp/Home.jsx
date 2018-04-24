import React from 'react';
import Typography from 'material-ui/Typography';
import { connect } from 'react-redux';

import IdeasList from './IdeasList';
import CreateIdeaHome from '../idea/CreateIdeaHome';
import Idea from '../idea/Idea';
import User from '../user/User';
import { openChatApp } from '../../actions/chatAppActions';

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.openChannel(this.props);
  }

  componentWillReceiveProps(nextProps) {
    this.openChannel(nextProps);
  }

  openChannel = (props) => {
    const { params: { channelId }, location: { query } } = props;
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
    const { ideaId, userId } = this.props.params;
    const { filter } = this.props;
    const hasFilter = filter && filter.text;
    const searchId = 'globalSearch';
    return [
      ideaId && <Idea id={ideaId} open />,
      userId && <User id={userId} open />,
      <Typography component="div">
        {!hasFilter && <CreateIdeaHome />}
        <IdeasList searchId={searchId} />
      </Typography>
    ];
  }
}

export const mapDispatchToProps = {
  openChatApp: openChatApp
};

export const mapStateToProps = (state) => {
  return {
    smallScreen: state.globalProps.smallScreen,
    filter: state.search.globalSearch
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);