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
import ChatAppRight from './chatAppRight/ChatAppRight';
import Divider from './Divider';
import Comment from '../forms/processes/common/Comment';
import { COMMENTS_ACTIONS, ACTIONS } from '../../processes';

const styles = (theme) => {
  return {
    container: {
      height: 'calc(100vh - 56px)'
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
      borderLeft: '1px solid #e8e8e8',
      padding: '0 !important',
      paddingRight: '8px !important',
      paddingTop: '8px !important'
    },
    list: {
      height: 'calc(100% - 55px)'
    }
  };
};

export class RenderComments extends React.Component {
  static defaultProps = {
    displayForm: true,
    dynamicDivider: true
  };

  render() {
    const {
      channelId,
      data,
      customScrollbar,
      dynamicDivider,
      reverted,
      ignorDrawer,
      fullScreen,
      rightDisabled,
      rightOpen,
      fetchMoreOnEvent,
      displayForm,
      formTop,
      formProps,
      classes
    } = this.props;
    const channel = data.node;
    const subject = channel && channel.subject;
    const commentAction =
      displayForm && subject && subject.actions && filterActions(subject.actions, { behaviorId: COMMENTS_ACTIONS })[0];
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
              ignorDrawer: ignorDrawer,
              dynamic: dynamicDivider
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
        {displayRightBlock && channel
          ? <Grid className={classes.right} item xs={12} md={4} sm={5}>
            <ChatAppRight channel={channel} />
          </Grid>
          : null}
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
            filter: props.filter ? props.filter.text : '',
            pinned: props.filter ? !!props.filter.pinned : false,
            file: props.filter ? !!props.filter.file : false,
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
    })(RenderComments)
  )
);