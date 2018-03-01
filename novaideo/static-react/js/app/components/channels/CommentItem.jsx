/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import Tooltip from 'material-ui/Tooltip';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { Translate, I18n } from 'react-redux-i18n';
import Icon from 'material-ui/Icon';
import ForumIcon from 'material-ui-icons/Forum';

import ImagesPreview from '../common/ImagesPreview';
import Url from '../common/Url';
import { getFormattedDate } from '../../utils/globalFunctions';
import CommentMenu from './CommentMenu';
import UserTitle from '../user/UserTitle';
import UserAvatar from '../user/UserAvatar';
import { COMMENTS_TIME_INTERVAL } from '../../constants';
import CommentProcessManager from './CommentProcessManager';
import { CONTENTS_IDS } from './chatAppRight';

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
    }
  };
};

class RenderCommentItem extends React.Component {
  constructor(props) {
    super(props);
    this.menu = null;
  }

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

  render() {
    const { node, classes, processManager, disableReply } = this.props;
    const ignoreMetaData = this.ignoreMetaData();
    const author = node.author;
    const authorPicture = author.picture;
    const isAnonymous = author.isAnonymous;
    const edited = node.edited;
    const pinned = node.pinned;
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
    const createdAtF = getFormattedDate(node.createdAt, 'date.format3');
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    return (
      <div onMouseOver={this.onMouseOver} onMouseLeave={this.onMouseLeave}>
        <div className={pinned ? classes.pinned : ''}>
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
              [classes.pinnedContainer]: pinned
            })}
          >
            {processManager &&
              <CommentMenu
                initRef={(menu) => {
                  this.menu = menu;
                }}
                comment={node}
                onActionClick={processManager.performAction}
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
              <div className={classes.bodyContent}>
                <div>
                  <div className={classes.contentText}>
                    <div className="comment-text" dangerouslySetInnerHTML={{ __html: node.text }} />
                  </div>
                  <ImagesPreview images={images} />
                </div>
                {node.urls.length > 0 &&
                  <div className={classes.urlsContainer}>
                    {node.urls.map((url, key) => {
                      return <Url key={key} data={url} />;
                    })}
                  </div>}
                {!disableReply && node.lenComments > 0
                  ? <div
                    onClick={() => {
                      processManager.openRight(CONTENTS_IDS.reply, { id: node.id });
                    }}
                    className={classes.replyContainer}
                  >
                    <ForumIcon className={classes.replyIcon} />
                    <span>
                      <Translate value="channels.replies" count={node.lenComments} />
                    </span>
                  </div>
                  : null}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export const CommentItem = withStyles(styles, { withTheme: true })(RenderCommentItem);

function DumbCommentItem(props) {
  const { node, onActionClick } = props;
  return (
    <CommentProcessManager comment={node} onActionClick={onActionClick}>
      <RenderCommentItem {...props} />
    </CommentProcessManager>
  );
}

export default withStyles(styles, { withTheme: true })(DumbCommentItem);