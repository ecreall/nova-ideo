import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import Grid from 'material-ui/Grid';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import ChannelNavbar from './channels/Navbar';
import App from './common/App';
import { commentsQuery } from '../graphql/queries';
import EntitiesList from './common/EntitiesList';
import CommentItem from './channels/CommentItem';
import ChatAppRight from './channels/ChatAppRight';

const styles = {
  container: {
    height: 'calc(100vh - 64px)'
  },
  comments: {
    backgroundColor: 'white'
  },
  commentsWithRight: {
    paddingRight: '0 !important'
  },
  right: {
    backgroundColor: '#f9f9f9',
    borderLeft: '1px solid #e8e8e8'
  }
};

const commentsActions = ['comment', 'general_discuss', 'discuss'];

export class DumbChatApp extends React.Component {
  render() {
    const { data, active, left, rightOpen, classes } = this.props;
    const channelData = data.node ? data.node : null;
    return (
      <App active={active} left={left} Navbar={ChannelNavbar} data={{ channel: channelData }}>
        <Grid className={classes.container} container>
          <Grid
            className={classNames(classes.comments, {
              [classes.commentsWithRight]: rightOpen
            })}
            item
            xs={12}
            md={rightOpen ? 9 : 12}
          >
            <EntitiesList
              reverted
              onEndReachedThreshold={0.5}
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
                height: '100%'
              }}
            />
          </Grid>
          {rightOpen &&
            <Grid className={classes.right} item xs={12} md={3}>
              <ChatAppRight />
            </Grid>}
        </Grid>
      </App>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    channel: state.apps.chatApp.channel,
    rightOpen: state.apps.chatApp.right.open
  };
};

export default withStyles(styles)(
  connect(mapStateToProps)(
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
  )
);