/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';
import ForumIcon from 'material-ui-icons/Forum';
import { connect } from 'react-redux';

import RightContent from './RightContent';
import Comments from '../channels/Comments';

const styles = {
  container: {
    height: 'calc(100vh - 122px)'
  },
  appTitle: {
    display: 'flex',
    alignItems: 'center'
  },
  appIcon: {
    marginRight: 5
  }
};

const ChatApp = (props) => {
  const { classes, appProps } = props;
  return (
    <RightContent
      title={
        <div>
          <div className={classes.appTitle}>
            <ForumIcon className={classes.appIcon} />
            <span>
              {(appProps && appProps.channelTitle) || I18n.t('channels.comments')}
            </span>
          </div>
        </div>
      }
    >
      <Comments
        inline
        customScrollbar
        reverted
        dynamicDivider={false}
        channelId={appProps.channel}
        formProps={{ autoFocus: true }}
        classes={{ container: classes.container }}
      />
    </RightContent>
  );
};

export const mapStateToProps = (state) => {
  return {
    appProps: state.apps.collaborationApp.right.props
  };
};

export default withStyles(styles)(connect(mapStateToProps)(ChatApp));