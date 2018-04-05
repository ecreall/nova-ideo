import React from 'react';
import Typography from 'material-ui/Typography';
import { connect } from 'react-redux';

import IdeasList from '../idea/IdeasList';
import CreateIdeaHome from '../idea/CreateIdeaHome';
import Idea from '../idea/Idea';
import { openChatApp } from '../../actions/actions';

const styles = {
  container: {
    marginTop: 25,
    maxWidth: 588,
    marginLeft: 'auto',
    marginRight: 'auto'
  }
};

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
        drawer: !smallScreen,
        channel: channelId,
        ...rightOpen
      });
    }
  };

  render() {
    const { ideaId } = this.props.params;
    return (
      <div>
        {ideaId && <Idea id={ideaId} open />}
        <Typography component="div" style={styles.container}>
          <CreateIdeaHome />
          <IdeasList />
        </Typography>
      </div>
    );
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

export default connect(mapStateToProps, mapDispatchToProps)(Home);