import React from 'react';
import { withStyles } from 'material-ui/styles';
import { Translate } from 'react-redux-i18n';
import { connect } from 'react-redux';

import { updateChatAppRight } from '../../../actions/chatAppActions';
import RightContent from './RightContent';
import Details from './Details';

const styles = {
  appTitle: {
    display: 'flex',
    alignItems: 'center'
  }
};

export const DumbDetailsApp = (props) => {
  const { classes, channel } = props;
  return (
    <RightContent
      title={
        <div className={classes.appTitle}>
          <span>
            <Translate value="channels.rightTitleAbout" name={channel.title} />
          </span>
        </div>
      }
    >
      <Details {...props} />
    </RightContent>
  );
};

export const mapDispatchToProps = {
  updateRight: updateChatAppRight
};

export const mapStateToProps = (state) => {
  return {
    componentId: state.apps.chatApp.right.componentId,
    subject: state.apps.chatApp.subject
  };
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(DumbDetailsApp));