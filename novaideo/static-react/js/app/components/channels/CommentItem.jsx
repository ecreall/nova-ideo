/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import Tooltip from 'material-ui/Tooltip';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { Translate, I18n } from 'react-redux-i18n';
import Icon from 'material-ui/Icon';
import CancelIcon from 'material-ui-icons/Cancel';
import ForumIcon from 'material-ui-icons/Forum';
import Collapse from 'material-ui/transitions/Collapse';
import IconButton from 'material-ui/IconButton';

import ImagesPreview from '../common/ImagesPreview';
import FilesPreview from '../common/FilesPreview';
import Url from '../common/Url';
import EmojiEvaluation from '../common/EmojiEvaluation';
import { getFormattedDate } from '../../utils/globalFunctions';
import { emojiConvert } from '../../utils/emojiConvertor';
import CommentMenu from './CommentMenu';
import UserTitle from '../user/UserTitle';
import UserAvatar from '../user/UserAvatar';
import Edit from '../forms/processes/commentProcess/Edit';
import CommentProcessManager from './CommentProcessManager';
import Reply from './chatAppRight/Reply';
import { COMMENTS_TIME_INTERVAL } from '../../constants';
import { CONTENTS_IDS } from './chatAppRight';
import { PROCESSES } from '../../processes';
import { getActions } from '../../utils/processes';

const styles = (theme) => {
  return {
    container: {
      paddingRight: 30,
      paddingTop: 1,
      paddingBottom: 2,
      display: 'flex',
      position: 'relative',
      '&:hover': {
        backgroundColor: '#f9f9f9',
        '& .creation-date': {
          display: 'block'
        }
      }
    },
    editContainer: {
      backgroundColor: `${theme.palette.warning[100]} !important`
    },
    pinnedContainer: {
      '&:hover': {
        backgroundColor: theme.palette.warning[50]
      }
    },
    pinned: {
      display: 'flex',
      flexDirection: 'column',
      backgroundColor: theme.palette.warning[50]
    },
    pinnedLabel: {
      display: 'flex',
      paddingTop: 5
    },
    pinnedIcon: {
      display: 'flex',
      justifyContent: 'flex-end',
      width: 70,
      paddingRight: 10,
      color: theme.palette.warning[500]
    },
    pinnedText: {
      fontFamily: 'LatoWebLight',
      color: '#4d4e4e',
      fontSize: 12
    },
    body: {
      display: 'flex',
      flexDirection: 'column',
      width: '100%'
    },
    left: {
      display: 'flex',
      justifyContent: 'flex-end',
      alignItems: 'start',
      paddingRight: 10,
      width: 75,
      margin: '5px 0'
    },
    leftDateOnly: {
      margin: '5px 0'
    },
    header: {
      display: 'flex',
      flexDirection: 'row',
      alignItems: 'center',
      margin: '5px 0'
    },
    headerAddOn: {
      color: '#999999ff',
      paddingLeft: 5,
      fontSize: 12
    },
    creationDate: {
      display: 'none',
      color: '#999999ff',
      fontSize: 12,
      height: 0
    },

    bodyContent: {
      display: 'flex',
      justifyContent: 'space-between',
      flexDirection: 'column',
      width: '100%',
      height: '100%'
    },
    contentText: {
      color: '#2c2d30',
      fontSize: 15,
      lineHeight: 1.5,
      wordWrap: 'break-word',
      '& a': {
        color: '#0576b9',
        textDecoration: 'none',
        '&:hover': {
          textDecoration: 'underline'
        }
      },
      '&p': {
        margin: 0
      }
    },
    urlsContainer: {
      paddingRight: 30,
      marginTop: 15,
      maxWidth: 400
    },
    replyContainer: {
      display: 'flex',
      alignItems: 'center',
      cursor: 'pointer',
      fontSize: 12,
      marginLeft: 5,
      color: theme.palette.info[500],
      '&:hover': {
        color: theme.palette.info[700]
      }
    },
    replyIcon: {
      width: 18,
      height: 18,
      marginRight: 5
    },
    avatar: {
      borderRadius: 4,
      width: 36,
      height: 36
    },
    tooltip: {
      marginBottom: 4
    },
    badgeUnread: {
      color: 'white',
      backgroundColor: theme.palette.danger['500'],
      padding: '3px 6px',
      marginLeft: 5,
      borderRadius: '1em',
      fontSize: 10,
      fontWeight: 700
    },
    commentText: {
      width: '100%',
      display: 'inline-block'
    },
    edited: {
      color: '#a0a0a2',
      fontSize: 13,
      whiteSpace: 'nowrap',
      marginLeft: 5
    },
    replyCommentsContainer: {
      position: 'relative',
      marginBottom: 10,
      '&:hover': {
        '& .close-reply': {
          display: 'block'
        }
      }
    },
    iconStart: {
      position: 'absolute',
      fontSize: '25px !important',
      color: '#bfbfbf',
      top: -23,
      left: 25
    },
    iconEnd: {
      position: 'absolute',
      fontSize: '25px !important',
      color: '#bfbfbf',
      bottom: -15,
      left: 25
    },
    closeReply: {
      display: 'none',
      position: 'absolute',
      top: 8,
      left: 13,
      fontSize: '20px !important',
      color: theme.palette.success['500'],
      backgroundColor: 'white'
    }
  };
};

class RenderCommentItem extends React.Component {
  state = { action: null };

  menu = null;

  ignoreMetaData = () => {
    const { node, reverted, next, previous } = this.props;
    const item = reverted ? next : previous;
    if (!item) return false;
    const currentNode = reverted ? node : item;
    const nextNode = reverted ? item : node;
    const author = currentNode.author.id;
    const nextAuthor = nextNode.author.id;
    const optimisticAuthorId = `${nextAuthor}comment`;
    const createdAt = new Date(currentNode.createdAt);
    const nextCreatedAt = new Date(nextNode.createdAt);
    const dateDiff = (createdAt - nextCreatedAt) / 60000; // minutes
    return (author === nextAuthor || author === optimisticAuthorId) && dateDiff < COMMENTS_TIME_INTERVAL;
  };

  ignorePinned = () => {
    const { node, reverted, next, previous } = this.props;
    const item = reverted ? next : previous;
    if (!item) return false;
    const currentNode = reverted ? node : item;
    const nextNode = reverted ? item : node;
    return currentNode.pinned && nextNode.pinned;
  };

  onMouseOver = () => {
    if (this.menu) this.menu.open();
  };

  onMouseLeave = () => {
    if (this.menu) this.menu.close();
  };

  onActionClick = (action, data) => {
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    const { processManager, itemProps } = this.props;
    const inline = itemProps && itemProps.inline;
    if (action.behaviorId === commentProcessNodes.edit.nodeId) return this.setState({ action: action });
    if (inline && action.behaviorId === commentProcessNodes.respond.nodeId) return this.setState({ action: action });
    return processManager.performAction(action, data);
  };

  onEdit = () => {
    this.setState({ action: null });
  };

  toggleReply = () => {
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    const { node, processManager, itemProps } = this.props;
    const inline = itemProps && itemProps.inline;
    const channel = (itemProps && itemProps.channel) || node.channel;
    if (inline) {
      const { action } = this.state;
      const isReply = action && action.behaviorId === commentProcessNodes.respond.nodeId;
      this.setState({ action: !isReply ? { behaviorId: commentProcessNodes.respond.nodeId } : null });
    } else {
      processManager.openRight(CONTENTS_IDS.reply, { id: node.id, channelTitle: channel.title, channelId: channel.id });
    }
  };

  render() {
    const { node, classes, processManager, disableReply } = this.props;
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    const abstractProcessNodes = PROCESSES.novaideoabstractprocess.nodes;
    const { action } = this.state;
    const edit = action && action.behaviorId === commentProcessNodes.edit.nodeId;
    const reply = action && action.behaviorId === commentProcessNodes.respond.nodeId;
    const ignoreMetaData = this.ignoreMetaData();
    const author = node.author;
    const authorPicture = author.picture;
    const isAnonymous = author.isAnonymous;
    const edited = node.edited;
    const pinned = node.pinned;
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
    const createdAtF = getFormattedDate(node.createdAt, 'date.format3');
    const images = node.attachedFiles
      ? node.attachedFiles.filter((file) => {
        return file.isImage;
      })
      : [];
    const files = node.attachedFiles
      ? node.attachedFiles.filter((file) => {
        return !file.isImage;
      })
      : [];
    const addReactionAction = getActions(node.actions, { behaviorId: abstractProcessNodes.addreaction.nodeId })[0];
    return (
      <div>
        <div onMouseOver={this.onMouseOver} onMouseLeave={this.onMouseLeave} className={pinned && classes.pinned}>
          {pinned &&
            !this.ignorePinned() &&
            <div className={classes.pinnedLabel}>
              <div className={classes.pinnedIcon}>
                <Icon className="mdi-set mdi-pin" />
              </div>
              <div className={classes.pinnedText}>
                {I18n.t('common.pinned')}
              </div>
            </div>}
          <div
            className={classNames(classes.container, {
              [classes.pinnedContainer]: !edit && pinned,
              [classes.editContainer]: edit
            })}
          >
            {!edit &&
              processManager &&
              <CommentMenu
                initRef={(menu) => {
                  this.menu = menu;
                }}
                comment={node}
                onActionClick={this.onActionClick}
              />}
            <div
              className={classNames(classes.left, {
                [classes.leftDateOnly]: ignoreMetaData
              })}
            >
              {ignoreMetaData
                ? <Tooltip id={node.id} title={createdAtF} placement="top">
                  <div className={classNames('creation-date', classes.creationDate)}>
                    {createdAt}
                  </div>
                </Tooltip>
                : <UserAvatar
                  isAnonymous={isAnonymous}
                  picture={authorPicture}
                  title={author.title}
                  classes={{ avatar: classes.avatar }}
                />}
            </div>
            <div className={classes.body}>
              {!ignoreMetaData &&
                <div className={classes.header}>
                  <UserTitle node={author} />
                  <Tooltip classes={{ root: classes.tooltip }} id={node.id} title={createdAtF} placement="top">
                    <span className={classes.headerAddOn}>
                      {createdAt}
                    </span>
                  </Tooltip>
                </div>}
              {edit
                ? <Edit
                  key={`edit-${node.id}`}
                  form={`edit-${node.id}`}
                  context={node}
                  onSubmit={this.onEdit}
                  action={action}
                  initialValues={{
                    comment: node.text,
                    files: node.attachedFiles.map((file) => {
                      return {
                        id: file.id,
                        oid: file.oid,
                        name: file.title,
                        size: file.size || 0,
                        mimetype: file.mimetype,
                        type: file.mimetype,
                        preview: { url: file.url, type: file.isImage ? 'image' : 'file' }
                      };
                    })
                  }}
                />
                : <div className={classes.bodyContent}>
                  <div>
                    <div className={classes.contentText}>
                      <div
                        className={classNames('comment-text', classes.commentText)}
                        dangerouslySetInnerHTML={{
                          __html: emojiConvert(node.formattedText)
                        }}
                      />

                      {edited &&
                      <span className={classes.edited}>
                            ({I18n.t('channels.edited')})
                      </span>}
                    </div>
                    <ImagesPreview images={images} />
                    <FilesPreview files={files} />
                  </div>
                  {node.urls.length > 0 &&
                  <div className={classes.urlsContainer}>
                    {node.urls.map((url, key) => {
                      return <Url key={key} data={url} />;
                    })}
                  </div>}
                  {node.emojis &&
                  <EmojiEvaluation
                    emojis={node.emojis}
                    onEmojiClick={(emoji) => {
                      if (addReactionAction) this.onActionClick(addReactionAction, { emoji: emoji });
                    }}
                  />}
                  {!disableReply && node.lenComments > 0
                    ? <div onClick={this.toggleReply} className={classes.replyContainer}>
                      <ForumIcon className={classes.replyIcon} />
                      <span>
                        <Translate value="channels.replies" count={node.lenComments} />
                        {node.lenUnreadReplies > 0 &&
                        <span className={classes.badgeUnread}>
                          <Translate value="channels.unreadReplies" count={node.lenUnreadReplies} />
                        </span>}
                      </span>
                    </div>
                    : null}
                </div>}
            </div>
          </div>
        </div>
        <div className={reply && classes.replyCommentsContainer}>
          {reply && <Icon className={classNames('mdi-set mdi-source-commit-start-next-local', classes.iconStart)} />}
          {reply &&
            <IconButton onClick={this.toggleReply} className={classNames('close-reply', classes.closeReply)}>
              <CancelIcon />
            </IconButton>}
          <Collapse in={reply}>
            {reply &&
              <Reply
                inline
                formTop
                dynamicDivider={false}
                id={node.id}
                moreBtn={
                  <span>
                    {I18n.t('common.moreResult')}
                  </span>
                }
              />}
          </Collapse>
          {reply && <Icon className={classNames('mdi-set mdi-source-commit-end-local', classes.iconEnd)} />}
        </div>
      </div>
    );
  }
}

export const CommentItem = withStyles(styles, { withTheme: true })(RenderCommentItem);

function DumbCommentItem(props) {
  const { node, itemProps, onActionClick } = props;
  return (
    <CommentProcessManager
      comment={node}
      channel={(itemProps && itemProps.channel) || node.channel}
      onActionClick={onActionClick}
    >
      <RenderCommentItem {...props} />
    </CommentProcessManager>
  );
}

export default withStyles(styles, { withTheme: true })(DumbCommentItem);