/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import Tooltip from 'material-ui/Tooltip';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { I18n } from 'react-redux-i18n';

import ImagesPreview from '../common/ImagesPreview';
import IconWithText from '../common/IconWithText';
import Url from '../common/Url';
import { getFormattedDate } from '../../utils/globalFunctions';
import CommentMenu from './CommentMenu';
import UserTitle from '../user/UserTitle';
import UserAvatar from '../user/UserAvatar';
import { COMMENTS_TIME_INTERVAL } from '../../constants';

const styles = {
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
  bodyFooter: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'flex-end'
  },
  actionsText: {
    fontSize: 14,
    marginLeft: 8,
    marginRight: 50
  },
  actionsIcon: {
    fontSize: 14
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

export class DumbCommentItem extends React.Component {
  constructor(props) {
    super(props);
    this.menu = null;
  }

  ignoreMetaData = () => {
    const { node, reverted } = this.props;
    const item = reverted ? this.props.next : this.props.previous;
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

  onMouseOver = () => {
    if (this.menu) this.menu.open();
  };

  onMouseLeave = () => {
    if (this.menu) this.menu.close();
  };

  render() {
    const { node, classes } = this.props;
    const ignoreMetaData = this.ignoreMetaData();
    const author = node.author;
    const authorPicture = author.picture;
    const isAnonymous = author.isAnonymous;
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
    const createdAtF = getFormattedDate(node.createdAt, 'date.format3');
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    return (
      <div onMouseOver={this.onMouseOver} onMouseLeave={this.onMouseLeave}>
        <div className={classes.container}>
          <CommentMenu
            initRef={(menu) => {
              this.menu = menu;
            }}
            comment={node}
          />
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
              {node.lenComments > 0
                ? <div className={classes.bodyFooter}>
                  <IconWithText
                    styleText={classes.actionsText}
                    styleIcon={classes.actionsIcon}
                    name="comment-multiple-outline"
                    text={`${node.lenComments} ${`reply${node.lenComments > 1 ? '*' : ''}`}`}
                  />
                </div>
                : null}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(DumbCommentItem);