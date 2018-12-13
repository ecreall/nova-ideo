import React from 'react';
import { Translate, I18n } from 'react-redux-i18n';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';
import debounce from 'lodash.debounce';
import classNames from 'classnames';

import CommentQuery from '../../../graphql/queries/Comment.graphql';
import FlatList from '../../common/FlatList';
import Alert from '../../common/Alert';
import LoginButton from '../../common/LoginButton';
import { filterActions } from '../../../utils/processes';
import CommentItem from '../CommentItem';
import Illustration from '../../common/Illustration';
import Divider from '../Divider';
import Comment from '../../forms/processes/common/Comment';
import { PROCESSES, ACTIONS } from '../../../processes';
import { NO_COMMENT, CT_COMMENT } from '../../../constants';
import { markAsRead } from '../../../graphql/processes/commentProcess';
import MarkAsRead from '../../../graphql/processes/commentProcess/mutations/MarkAsRead.graphql';
import { getFormId } from '../../../utils/globalFunctions';

const styles = (theme) => {
  return {
    container: {
      height: 'calc(100vh - 132px)'
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
      paddingTop: '0 !important',
      [theme.breakpoints.only('xs')]: {
        display: 'none'
      }
    },
    right: {
      backgroundColor: '#f9f9f9',
      borderLeft: '1px solid #e8e8e8',
      padding: '0 !important'
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
      bottom: 7,
      width: 'calc(100% - 49px)'
    },
    alertsContainer: {
      padding: 16,
      position: 'absolute',
      width: 'calc(100% - 32px)',
      zIndex: 15
    },
    alertsContainerInline: {
      position: 'initial'
    },
    alertContainer: {
      boxShadow: '0 2px 6px rgba(0, 0, 0, 0.4)'
    },
    alertMessageContainer: {
      width: '100%',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }
  };
};

const ReplyFooter = (classes, inline) => {
  return (props) => {
    const { data } = props;
    return (
      <div className={classes.commentsFooter}>
        {!inline && <CommentItem disableReply node={data.node} />}
        <div className={classes.commentsFooterMessage}>{I18n.t('channels.replyCommentFooter')}</div>
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

  renderAlert = () => {
    const {
      data, inline, account, theme, classes
    } = this.props;
    if (account) return null;
    const comment = data.node;
    const channel = comment && comment.channel;
    return (
      <div className={classNames(classes.alertsContainer, { [classes.alertsContainerInline]: inline })}>
        <Alert
          dismissible
          type="warning"
          classes={{ container: classes.alertContainer, messageContainer: classes.alertMessageContainer }}
        >
          <div>
            <Translate value="channels.noUserCtReply" name={channel ? channel.title : '...'} />
          </div>
          <LoginButton color={theme.palette.warning[500]} />
        </Alert>
      </div>
    );
  };

  renderCommentForm = (commentAction) => {
    const {
      id, rightProps, data, inline, formProps, classes
    } = this.props;
    const comment = data.node;
    const channel = comment && comment.channel;
    const formId = getFormId(id || rightProps.id);
    return (
      commentAction && (
        <Comment
          placeholder={<Translate value="channels.reply" name={comment && comment.author.title} />}
          form={formId}
          key={formId}
          channel={channel}
          context={comment && comment.oid}
          subject={comment && comment.rootOid}
          action={commentAction}
          {...formProps}
          classes={{
            container: inline ? classes.inlineFormContainer : classes.blockComments,
            containerAddon: inline && classes.inlineContainerAddon
          }}
        />
      )
    );
  };

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
      classes,
      moreBtn,
      NoItems
    } = this.props;
    const comment = data.node;
    const channel = comment && comment.channel;
    const commentAction = displayForm
      && comment
      && comment.actions
      && filterActions(comment.actions, { behaviorId: PROCESSES.commentmanagement.nodes.respond.nodeId })[0];
    const commentForm = this.renderCommentForm(commentAction);
    return (
      <Grid className={classNames(classes.container, { [classes.containerInline]: inline })} container>
        <Grid className={classNames(classes.comments, { [classes.commentsInline]: inline })} item>
          {this.renderAlert()}
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
    rightProps: state.apps.chatApp.right.props,
    account: state.globalProps.account
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(CommentQuery, {
      options: (props) => {
        return {
          fetchPolicy: 'cache-and-network',
          notifyOnNetworkStatusChange: true,
          variables: {
            filter: props.filter ? props.filter : {},
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
      graphql(MarkAsRead, {
        props: function (props) {
          return {
            markAsReadReplies: markAsRead(props)
          };
        }
      })(RenderComment)
    )
  )
);