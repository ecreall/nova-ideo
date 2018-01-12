/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import { connect } from 'react-redux';
import Avatar from 'material-ui/Avatar';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';

import ImagesPreview from '../common/ImagesPreview';
import IconWithText from '../common/IconWithText';
import Url from '../common/Url';
import Divider from './Divider';

const styles = {
  container: {
    paddingLeft: 30,
    paddingRight: 30,
    paddingTop: 1,
    paddingBottom: 2,
    display: 'flex',
    '&:hover': {
      backgroundColor: '#f9f9f9'
    }
  },
  body: {
    display: 'flex',
    flexDirection: 'column',
    width: '100%'
  },
  left: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'start',
    paddingRight: 10,
    width: 45,
    margin: '8px 0'
  },
  header: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    margin: '10px 0'
  },
  headerTitle: {
    display: 'flex',
    fontSize: 15,
    color: '#2c2d30',
    fontWeight: '900',
    justifyContent: 'space-around'
  },
  headerAddOn: {
    color: '#999999ff',
    paddingLeft: 5,
    fontSize: 13
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
    '&p': {
      margin: 0
    }
  },
  urlsContainer: {
    paddingRight: 30,
    paddingLeft: 10,
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
    color: 'gray',
    marginLeft: 8,
    marginRight: 50
  },
  actionsIcon: {
    marginTop: 1
  }
};

const ignoreTimeInterval = 5; // 5 min

export class DumbCommentItem extends React.Component {
  ignoreMetaData = () => {
    const { node, next } = this.props;
    if (!next) return false;
    const author = node.author.id;
    const nextAuthor = next.author.id;
    const createdAt = new Date(node.createdAt);
    const nextCreatedAt = new Date(next.createdAt);
    const dateDiff = (createdAt - nextCreatedAt) / 3600000;
    const optimisticAuthorId = `${nextAuthor}comment`;
    return (author === nextAuthor || author === optimisticAuthorId) && dateDiff < ignoreTimeInterval;
  };

  addDateSeparator = () => {
    const { node, next } = this.props;
    if (!next) return true;
    const createdAt = Moment(node.createdAt).format('D-M-YYYY');
    const nextCreatedAt = Moment(next.createdAt).format('D-M-YYYY');
    return nextCreatedAt !== createdAt;
  };

  addUnread = () => {
    const { node, next, itemdata } = this.props;
    if (!next) return false;
    const unreadComments = itemdata.unreadCommentsIds;
    const isUnread = unreadComments.includes(node.id);
    const nextIsUnread = unreadComments.includes(next.id);
    return isUnread && !nextIsUnread;
  };

  render() {
    const { node, classes, index, channelsDrawer } = this.props;
    const ignoreMetaData = this.ignoreMetaData();
    const addUnread = this.addUnread();
    const addDateSeparator = this.addDateSeparator();
    const dateSeparator = addDateSeparator && Moment(node.createdAt).format(I18n.t('date.format'));
    const author = node.author;
    const authorPicture = author.picture;
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    return (
      <div>
        {(dateSeparator || addUnread) &&
          <Divider
            index={index}
            alert={addUnread}
            message={dateSeparator}
            alertMessage="Unread"
            eventId="comments-scroll"
            shift={channelsDrawer ? 220 : 0}
            fixedTop={65}
          />}
        <div className={classes.container}>
          <div className={classes.left}>
            {!ignoreMetaData && <Avatar size={35} src={authorPicture ? `${authorPicture.url}/profil` : ''} />}
          </div>
          <div className={classes.body}>
            {!ignoreMetaData &&
              <div className={classes.header}>
                <span className={classes.headerTitle}>
                  {author.title}
                </span>
                <span className={classes.headerAddOn}>
                  {createdAt}
                </span>
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
                    return <Url key={key} data={url} onPressUrlImage />;
                  })}
                </div>}
              {node.lenComments > 0
                ? <div className={classes.bodyFooter}>
                  <IconWithText
                    styleText={styles.actionsText}
                    styleIcon={styles.actionsIcon}
                    name="comment-multiple-outline"
                    iconSize={15}
                    iconColor="gray"
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

export const mapStateToProps = (state) => {
  return {
    channelsDrawer: state.apps.chatApp.drawer
  };
};

export default withStyles(styles)(connect(mapStateToProps)(DumbCommentItem));