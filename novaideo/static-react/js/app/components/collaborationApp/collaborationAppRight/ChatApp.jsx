/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';
import Icon from 'material-ui/Icon';
import { connect } from 'react-redux';
import classNames from 'classnames';

import RightContent from './RightContent';
import Comments from '../../chatApp/Comments';

const styles = {
  container: {
    height: 'calc(100vh - 132px)'
  },
  appTitle: {
    display: 'flex',
    alignItems: 'center'
  },
  appIcon: {
    fontWeight: '900 !important',
    fontSize: '16px !important'
  }
};

const ChatApp = (props) => {
  const { classes, appProps } = props;
  return (
    <RightContent
      title={
        <div>
          <Icon className={classNames('mdi-set mdi-pound', classes.appIcon)} />
          {(appProps && appProps.channelTitle) || I18n.t('channels.comments')}
        </div>
      }
    >
      <Comments
        inline
        customScrollbar
        reverted
        rightDisabled
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