/* eslint-disable react/no-array-index-key */
import React from 'react';
import Moment from 'moment';
import Avatar from 'material-ui/Avatar';
import Tooltip from 'material-ui/Tooltip';
import Icon from 'material-ui/Icon';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import { I18n } from 'react-redux-i18n';

import ImagesPreview from '../common/ImagesPreview';
import IconWithText from '../common/IconWithText';
import Url from '../common/Url';

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
    anonymousAvatar: {
      color: theme.palette.tertiary.hover.color,
      backgroundColor: theme.palette.tertiary.color,
      fontWeight: 900
    },
    tooltip: {
      marginBottom: 4
    }
  };
};

const ignoreTimeInterval = 5; // 5 minutes

export class DumbCommentItem extends React.Component {
  ignoreMetaData = () => {
    const { node, next } = this.props;
    if (!next) return false;
    const author = node.author.id;
    const nextAuthor = next.author.id;
    const optimisticAuthorId = `${nextAuthor}comment`;
    const createdAt = new Date(node.createdAt);
    const nextCreatedAt = new Date(next.createdAt);
    const dateDiff = (createdAt - nextCreatedAt) / 60000; // minutes
    return (author === nextAuthor || author === optimisticAuthorId) && dateDiff < ignoreTimeInterval;
  };

  render() {
    const { node, classes } = this.props;
    const ignoreMetaData = this.ignoreMetaData();
    const author = node.author;
    const authorPicture = author.picture;
    const isAnonymous = author.isAnonymous;
    const createdAt = Moment(node.createdAt).format(I18n.t('time.format'));
    const today = Moment();
    const isToday = today.isSame(Moment(node.createdAt), 'day');
    const yesterday = today.subtract(1, 'days').startOf('day');
    const isYesterday = yesterday.isSame(Moment(node.createdAt), 'day');
    const format = (isToday && 'date.todayFormat') || (isYesterday && 'date.yesterdayFormat') || 'date.format3';
    const createdAtF3 = Moment(node.createdAt).format(I18n.t(format));
    const images = node.attachedFiles
      ? node.attachedFiles.filter((image) => {
        return image.isImage;
      })
      : [];
    return (
      <div>
        <div className={classes.container}>
          <div
            className={classNames(classes.left, {
              [classes.leftDateOnly]: ignoreMetaData
            })}
          >
            {ignoreMetaData
              ? <Tooltip id={node.id} title={createdAtF3} placement="top">
                <div className={classNames('creation-date', classes.creationDate)}>
                  {createdAt}
                </div>
              </Tooltip>
              : <Avatar
                className={isAnonymous && classes.anonymousAvatar}
                classes={{ root: classes.avatar }}
                size={35}
                src={authorPicture ? `${authorPicture.url}/profil` : ''}
              >
                {isAnonymous && <Icon className={'mdi-set mdi-guy-fawkes-mask'} />}
              </Avatar>}
          </div>
          <div className={classes.body}>
            {!ignoreMetaData &&
              <div className={classes.header}>
                <span className={classes.headerTitle}>
                  {author.title}
                </span>
                <Tooltip classes={{ root: classes.tooltip }} id={node.id} title={createdAtF3} placement="top">
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