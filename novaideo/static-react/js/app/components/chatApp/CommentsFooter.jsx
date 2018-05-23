/* eslint-disable no-underscore-dangle */
import React from 'react';
import { Translate, I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';

import UserTitle from '../user/UserTitle';
import UserAvatar from '../user/UserAvatar';

const styles = {
  commentsFooter: {
    margin: '48px 32px 16px 16px',
    color: '#656565',
    fontSize: 15,
    lineHeight: 1.5
  },
  header: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'flex-start',
    margin: '0 10px',
    position: 'relative'
  },
  headerTitle: {
    fontSize: 15,
    color: '#2c2d30',
    fontWeight: 900,
    lineHeight: 'normal'
  },
  titleContainer: {
    display: 'flex',
    marginBottom: 20
  },
  headerAddOn: {
    color: '#999999ff',
    fontSize: 12,
    lineHeight: 'normal'
  }
};

const CommentsIdeaFooter = ({ data, classes }) => {
  const author = data.node.subject.author;
  const authorPicture = author.picture;
  const isAnonymous = author.isAnonymous;
  const authorTitle = author && author.title;
  const title = data.node && data.node.title;
  return (
    <div className={classes.commentsFooter}>
      <div className={classes.titleContainer}>
        <UserAvatar isAnonymous={isAnonymous} picture={authorPicture} title={authorTitle} />
        <div className={classes.header}>
          <span className={classes.headerTitle}>
            <UserTitle node={author} />
          </span>
          <span className={classes.headerAddOn}>
            {title}
          </span>
        </div>
      </div>
      <b>{<Translate value="channels.ideasCommentsFooterTitle" name={title} />}</b> {I18n.t('channels.ideasCommentsFooter')}
    </div>
  );
};

const CommentsUserFooter = ({ data, classes }) => {
  const user = data.node.subject;
  const userPicture = user.picture;
  const userTitle = user && user.title;
  return (
    <div className={classes.commentsFooter}>
      <div className={classes.titleContainer}>
        <UserAvatar picture={userPicture} title={userTitle} />
        <div className={classes.header}>
          <span className={classes.headerTitle}>
            <UserTitle node={user} />
          </span>
        </div>
      </div>
      <b>{<Translate value="channels.usersCommentsFooterTitle" name={data.node && data.node.title} />}</b>{' '}
      {<Translate value="channels.usersCommentsFooter" name={data.node && data.node.title} />}
    </div>
  );
};

export const DumbCommentsFooter = (props) => {
  const { data } = props;
  switch (data.node.subject.__typename) {
  case 'Idea':
    return <CommentsIdeaFooter {...props} />;
  case 'Person':
    return <CommentsUserFooter {...props} />;
  default:
    return null;
  }
};

export default withStyles(styles)(DumbCommentsFooter);