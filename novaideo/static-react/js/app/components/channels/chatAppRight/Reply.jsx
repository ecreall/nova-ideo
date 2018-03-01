import React from 'react';
import { Translate, I18n } from 'react-redux-i18n';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import Grid from 'material-ui/Grid';
import { withStyles } from 'material-ui/styles';

import { commentQuery } from '../../../graphql/queries';
import FlatList from '../../common/FlatList';
import { filterActions } from '../../../utils/processes';
import CommentItem from '../CommentItem';
import Divider from '../Divider';
import Comment from '../../forms/processes/common/Comment';
import { PROCESSES, ACTIONS } from '../../../processes';

const styles = (theme) => {
  return {
    container: {
      height: 'calc(100vh - 56px)'
    },
    comments: {
      backgroundColor: 'white',
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column',
      height: '100%'
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
    },
    header: {
      margin: '48px 32px 16px 16px',
      color: '#2c2d30',
      fontSize: 17,
      lineHeight: 1.5
    },
    noResult: {
      paddingLeft: 15,
      marginBottom: 15,
      fontSize: 15,
      color: '#717274',
      lineHeight: '20px'
    },
    commentsFooter: {
      margin: 15,
      color: '#656565',
      fontSize: 15,
      lineHeight: 1.5
    },
    commentsFooterMessage: {
      marginTop: 10
    }
  };
};

const ReplyFooter = (classes) => {
  return (props) => {
    const { data } = props;
    return (
      <div className={classes.commentsFooter}>
        <CommentItem disableReply node={data.node} />
        <div className={classes.commentsFooterMessage}>
          {I18n.t('channels.replyCommentFooter')}
        </div>
      </div>
    );
  };
};

const NoComments = (classes) => {
  return () => {
    return (
      <div className={classes.noResult}>
        {I18n.t('channels.noMessage')}
      </div>
    );
  };
};

const CtComment = (classes) => {
  return () => {
    return (
      <div className={classes.noResult}>
        {I18n.t('channels.ctComment')}
      </div>
    );
  };
};

export class RenderComment extends React.Component {
  static defaultProps = {
    displayForm: true,
    dynamicDivider: true,
    displayFooter: true
  };

  render() {
    const {
      rightProps,
      data,
      customScrollbar,
      dynamicDivider,
      reverted,
      ignorDrawer,
      fullScreen,
      fetchMoreOnEvent,
      displayForm,
      formTop,
      formProps,
      classes,
      moreBtn,
      NoItems
    } = this.props;
    const comment = data.node;
    const channel = comment && comment.channel;
    const commentAction =
      displayForm &&
      comment &&
      comment.actions &&
      filterActions(comment.actions, { behaviorId: PROCESSES.commentmanagement.nodes.respond.nodeId })[0];
    const commentForm =
      commentAction &&
      <Comment
        placeholder={<Translate value={'channels.reply'} name={comment && comment.author.title} />}
        key={rightProps.id}
        form={rightProps.id}
        channel={channel}
        context={comment && comment.oid}
        subject={comment && comment.rootOid}
        action={commentAction}
        {...formProps}
        classes={{ container: classes.formContainer }}
      />;
    return (
      <Grid className={classes.container} container>
        <Grid className={classes.comments} item>
          {formTop && commentForm}
          <FlatList
            Footer={ReplyFooter(classes)}
            NoItems={NoItems || (commentAction ? NoComments(classes) : CtComment(classes))}
            customScrollbar={customScrollbar}
            fetchMoreOnEvent={fetchMoreOnEvent}
            scrollEvent={rightProps.id}
            reverted={reverted}
            onEndReachedThreshold={reverted ? 0.3 : 0.7}
            data={data}
            getEntities={(entities) => {
              return entities.node && entities.node.comments;
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
                  ? channel.unreadComments.map((comm) => {
                    return comm.id;
                  })
                  : []
            }}
            moreBtn={moreBtn}
            className={classes.list}
          />
          {!formTop && commentForm}
        </Grid>
      </Grid>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    rightProps: state.apps.chatApp.right.props
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(commentQuery, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          notifyOnNetworkStatusChange: true,
          variables: {
            filter: props.filter ? props.filter.text : '',
            first: 25,
            after: '',
            id: props.rightProps.id,
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary],
            subjectActionsTags: [ACTIONS.primary]
          }
        };
      }
    })(RenderComment)
  )
);