import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import Grid from 'material-ui/Grid';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';

import { commentsQuery } from '../../graphql/queries';
import EntitiesList from '../common/EntitiesList';
import { filterActions } from '../../utils/processes';
import CommentItem from './CommentItem';
import ChatAppRight from './ChatAppRight';
import Divider from './Divider';
import Comment from '../forms/processes/common/Comment';
import { COMMENTS_ACTIONS, ACTIONS } from '../../processes';

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

export class DumbComments extends React.Component {
  render() {
    const {
      channelId,
      data,
      customScrollbar,
      reverted,
      ignorDrawer,
      fullScreen,
      rightDisabled,
      rightOpen,
      fetchMoreOnEvent,
      formTop,
      formProps,
      classes
    } = this.props;
    const channel = data.node;
    const subject = channel && channel.subject;
    const commentAction = subject && subject.actions && filterActions(subject.actions, { behaviorId: COMMENTS_ACTIONS })[0];
    const contextOid = subject ? subject.oid : '';
    const displayRightBlock = !rightDisabled && rightOpen;
    const commentForm =
      commentAction &&
      <Comment
        key={channelId}
        form={channelId}
        channel={channel}
        context={contextOid}
        subject={contextOid}
        action={commentAction}
        {...formProps}
        classes={{ container: classes.formContainer }}
      />;
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
            listId={channelId}
            reverted={reverted}
            // virtualized
            onEndReachedThreshold={0.5}
            data={data}
            getEntities={(entities) => {
              return entities.node && entities.node.comments;
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
              channel: channel,
              unreadCommentsIds:
                channel && channel.unreadComments
                  ? channel.unreadComments.map((comment) => {
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
          channel &&
          <Grid className={classes.right} item xs={12} md={4} sm={5}>
            <ChatAppRight channel={channel} />
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
          fetchPolicy: 'cache-and-network',
          notifyOnNetworkStatusChange: true,
          variables: {
            filter: '',
            first: 25,
            after: '',
            id: props.channelId,
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary],
            subjectActionsNodeIds: COMMENTS_ACTIONS
          }
        };
      }
    })(DumbComments)
  )
);