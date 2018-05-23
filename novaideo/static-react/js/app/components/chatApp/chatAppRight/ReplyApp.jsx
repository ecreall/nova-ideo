import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';
import MIcon from '@material-ui/core/Icon';
import ForumIcon from '@material-ui/icons/Forum';
import { connect } from 'react-redux';

import { updateChatAppRight } from '../../../actions/chatAppActions';
import { goTo, get } from '../../../utils/routeMap';
import RightContent from './RightContent';
import Reply from './Reply';

const styles = {
  appTitle: {
    display: 'flex',
    alignItems: 'center'
  },
  appIcon: {
    marginRight: 5
  },
  replyTitle: {
    cursor: 'pointer',
    fontSize: 13,
    color: '#585858',
    fontWeight: 100,
    marginLeft: 30,
    '&:hover': {
      textDecoration: 'underline'
    }
  }
};

const ReplyApp = (props) => {
  const { classes, rightProps, updateRight } = props;
  return (
    <RightContent
      title={
        <div>
          <div className={classes.appTitle}>
            <ForumIcon className={classes.appIcon} />
            <span>
              {I18n.t('channels.thread')}
            </span>
          </div>
          <div
            onClick={() => {
              updateRight({ full: false });
              goTo(get('messages', { channelId: rightProps.channelId }));
            }}
            className={classes.replyTitle}
          >
            <MIcon className="mdi-set mdi-pound" />
            {rightProps.channelTitle}
          </div>
        </div>
      }
    >
      <Reply {...props} />
    </RightContent>
  );
};

export const mapDispatchToProps = {
  updateRight: updateChatAppRight
};

export const mapStateToProps = (state) => {
  return {
    rightProps: state.apps.chatApp.right.props
  };
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(ReplyApp));