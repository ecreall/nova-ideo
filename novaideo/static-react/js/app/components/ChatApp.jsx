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
import Divider from './channels/Divider';
import Comment from './forms/Comment';

const styles = (theme) => {
  return {
    container: {
      height: 'calc(100vh - 64px)'
    },
    comments: {
      backgroundColor: 'white',
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column'
    },
    commentsWithRight: {
      paddingRight: '0 !important',
      [theme.breakpoints.only('xs')]: {
        display: 'none'
      }
    },
    right: {
      backgroundColor: '#f9f9f9',
      borderLeft: '1px solid #e8e8e8'
    },
    list: {
      height: 'calc(100% - 55px)'
    }
  };
};

const commentsActions = ['comment', 'general_discuss', 'discuss'];

export class DumbChatApp extends React.Component {
  render() {
    const { data, active, channel, left, rightOpen, classes } = this.props;
    const commentAction = data.node
      ? data.node.subject.actions.filter((action) => {
        return commentsActions.includes(action.behaviorId);
      })[0]
      : null;
    const contextOid = data.node ? data.node.subject.oid : '';
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
            md={rightOpen ? 8 : 12}
            sm={rightOpen ? 7 : 12}
          >
            <EntitiesList
              listId="comments"
              reverted
              onEndReachedThreshold={0.5}
              data={data}
              getEntities={(entities) => {
                return entities.node ? entities.node.comments : undefined;
              }}
              offlineFilter={(entity, text) => {
                return entity.node.text.toLowerCase().search(text) >= 0;
              }}
              ListItem={CommentItem}
              Divider={Divider}
              itemdata={{
                channel: channelData,
                unreadCommentsIds: channelData
                  ? channelData.unreadComments.map((comment) => {
                    return comment.id;
                  })
                  : []
              }}
              itemHeightEstimation={120}
              className={classes.list}
            />
            <Comment
              key={channel}
              form={channel}
              action={commentAction}
              context={contextOid}
              rootContext={contextOid}
              channel={data.node}
            />
          </Grid>
          {rightOpen &&
            <Grid className={classes.right} item xs={12} md={4} sm={5}>
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

export default withStyles(styles, { withTheme: true })(
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