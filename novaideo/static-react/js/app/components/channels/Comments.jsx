import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import Grid from 'material-ui/Grid';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import { commentsQuery } from '../../graphql/queries';
import EntitiesList from '../common/EntitiesList';
import CommentItem from './CommentItem';
import ChatAppRight from './ChatAppRight';
import Divider from './Divider';
import Comment from '../forms/Comment';

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

export class DumbComments extends React.Component {
  render() {
    const {
      id,
      channel,
      data,
      autoFocus,
      formTop,
      customScrollbar,
      reverted,
      rightDisabled,
      rightOpen,
      fetchMoreOnEvent,
      classes,
      fullScreen,
      ignorDrawer
    } = this.props;
    const commentAction = data.node
      ? data.node.subject.actions.filter((action) => {
        return commentsActions.includes(action.behaviorId);
      })[0]
      : null;
    const contextOid = data.node ? data.node.subject.oid : '';
    const channelData = data.node ? data.node : null;
    const displayRightBlock = !rightDisabled && rightOpen;
    const commentForm = (
      <Comment
        classes={{ container: classes.formContainer }}
        key={channel}
        form={channel}
        action={commentAction}
        context={contextOid}
        rootContext={contextOid}
        channel={data.node}
        autoFocus={autoFocus}
      />
    );
    return (
      <Grid className={classes.container} container>
        <Grid
          className={classNames(classes.comments, {
            [classes.commentsWithRight]: displayRightBlock
          })}
          item
          xs={12}
          md={displayRightBlock ? 8 : 12}
          sm={displayRightBlock ? 7 : 12}
        >
          {formTop && commentForm}
          <EntitiesList
            customScrollbar={customScrollbar}
            fetchMoreOnEvent={fetchMoreOnEvent}
            listId={id}
            reverted={reverted}
            // virtualized
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
            dividerProps={{
              fullScreen: fullScreen,
              ignorDrawer: ignorDrawer
            }}
            itemProps={{
              channel: channelData,
              unreadCommentsIds: channelData
                ? channelData.unreadComments.map((comment) => {
                  return comment.id;
                })
                : []
            }}
            itemHeightEstimation={50}
            className={classes.list}
          />
          {!formTop && commentForm}
        </Grid>
        {displayRightBlock &&
          data.node &&
          <Grid className={classes.right} item xs={12} md={4} sm={5}>
            <ChatAppRight />
          </Grid>}
      </Grid>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
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
            first: 25,
            after: '',
            filter: '',
            id: props.channel,
            processId: '',
            nodeIds: commentsActions
          }
        };
      }
    })(DumbComments)
  )
);