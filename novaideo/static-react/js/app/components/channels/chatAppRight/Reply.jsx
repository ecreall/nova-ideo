import React from 'react';
import { Translate, I18n } from 'react-redux-i18n';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import Grid from 'material-ui/Grid';
import { withStyles } from 'material-ui/styles';
import debounce from 'lodash.debounce';
import classNames from 'classnames';

import { commentQuery } from '../../../graphql/queries';
import FlatList from '../../common/FlatList';
import { filterActions } from '../../../utils/processes';
import CommentItem from '../CommentItem';
import Illustration from '../../common/Illustration';
import Divider from '../Divider';
import Comment from '../../forms/processes/common/Comment';
import { PROCESSES, ACTIONS } from '../../../processes';
import { NO_COMMENT, CT_COMMENT } from '../../../constants';
import { markAsRead } from '../../../graphql/processes/commentProcess';
import { markAsReadMutation } from '../../../graphql/processes/commentProcess/markAsRead';

const styles = (theme) => {
  return {
    container: {
      height: 'calc(100vh - 122px)'
    },
    containerInline: {
      height: 'auto',
      paddingRight: 0,
      margin: 0,
      width: '100%',
      paddingLeft: 36
    },
    comments: {
      backgroundColor: 'white',
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column',
      height: '100%',
      width: '100%',
      position: 'relative'
    },
    commentsInline: {
      paddingLeft: '0 !important',
      paddingRight: '0 !important',
      borderLeft: 'solid 1px #e6e6e6',
      position: 'inherit'
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
    commentsFooter: {
      margin: 15,
      color: '#656565',
      fontSize: 15,
      lineHeight: 1.5
    },
    commentsFooterMessage: {
      marginTop: 10
    },
    inlineFormContainer: {
      paddingLeft: 29
    },
    inlineContainerAddon: {
      boxShadow: 'none'
    },
    iconStart: {
      marginLeft: -12,
      marginTop: -16,
      fontSize: '25px !important',
      color: '#bfbfbf',
      marginBottom: -9,
      backgroundColor: 'white'
    },
    iconEnd: {
      marginLeft: -12,
      marginTop: -9,
      fontSize: '25px !important',
      color: '#bfbfbf',
      marginBottom: -16,
      backgroundColor: 'white'
    },
    blockComments: {
      position: 'absolute',
      bottom: 15,
      width: 'calc(100% - 49px)'
    }
  };
};

const ReplyFooter = (classes, inline) => {
  return (props) => {
    const { data } = props;
    return (
      <div className={classes.commentsFooter}>
        {!inline && <CommentItem disableReply node={data.node} />}
        <div className={classes.commentsFooterMessage}>
          {I18n.t('channels.replyCommentFooter')}
        </div>
      </div>
    );
  };
};

const NoComments = () => {
  return <Illustration img={NO_COMMENT} message={I18n.t('channels.noMessage')} />;
};

const CtComment = () => {
  return <Illustration img={CT_COMMENT} message={I18n.t('channels.ctComment')} />;
};

export class RenderComment extends React.Component {
  static defaultProps = {
    displayForm: true,
    dynamicDivider: true,
    displayFooter: true
  };

  componentDidUpdate() {
    const { data, markAsReadReplies } = this.props;
    const comment = data.node;
    if (comment && comment.unreadReplies && comment.unreadReplies.length > 0) {
      debounce(() => {
        markAsReadReplies({ context: comment, isDiscussion: comment.channel.isDiscuss });
      }, 400)();
    }
  }

  render() {
    const {
      id,
      rightProps,
      data,
      customScrollbar,
      dynamicDivider,
      reverted,
      inline,
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
        key={id || rightProps.id}
        form={id || rightProps.id}
        channel={channel}
        context={comment && comment.oid}
        subject={comment && comment.rootOid}
        action={commentAction}
        {...formProps}
        classes={{
          container: inline ? classes.inlineFormContainer : classes.blockComments,
          containerAddon: inline && classes.inlineContainerAddon
        }}
      />;
    return (
      <Grid className={classNames(classes.container, { [classes.containerInline]: inline })} container>
        <Grid className={classNames(classes.comments, { [classes.commentsInline]: inline })} item>
          {formTop && commentForm}
          <FlatList
            Footer={ReplyFooter(classes, inline)}
            NoItems={NoItems || (commentAction ? NoComments : CtComment)}
            customScrollbar={customScrollbar}
            fetchMoreOnEvent={fetchMoreOnEvent}
            scrollEvent={id || rightProps.id}
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
              inline: inline,
              unreadCommentsIds:
                comment && comment.unreadReplies
                  ? comment.unreadReplies.map((comm) => {
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
            id: props.id || props.rightProps.id,
            processIds: [],
            nodeIds: [],
            processTags: [],
            actionTags: [ACTIONS.primary],
            subjectActionsTags: [ACTIONS.primary]
          }
        };
      }
    })(
      graphql(markAsReadMutation, {
        props: function (props) {
          return {
            markAsReadReplies: markAsRead(props)
          };
        }
      })(RenderComment)
    )
  )
);