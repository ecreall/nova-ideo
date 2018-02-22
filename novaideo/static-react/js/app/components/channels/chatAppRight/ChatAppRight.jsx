import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import IconButton from 'material-ui/IconButton';
import CloseIcon from 'material-ui-icons/Close';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import { Translate } from 'react-redux-i18n';

import { updateApp } from '../../../actions/actions';
import Details, { CONTENTS_IDS } from './Details';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%'
  },
  menuButton: {
    color: '#717274',
    fontSize: 18
  },
  appBar: {
    position: 'relative',
    backgroundColor: 'transparent',
    boxShadow: 'none'
  },
  appBarContent: {
    flex: 1,
    fontSize: 18,
    fontWeight: 900,
    overflow: 'hidden',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis'
  }
};

const ChatAppRightContent = (props) => {
  switch (props.componentId) {
  case CONTENTS_IDS.info:
    return <Details {...props} />;
  case CONTENTS_IDS.pinned:
    return <Details {...props} />;
  case CONTENTS_IDS.files:
    return <Details {...props} />;
  case CONTENTS_IDS.members:
    return <Details {...props} />;
  case CONTENTS_IDS.details:
    return <Details {...props} />;
  default:
    return <div />;
  }
};

class ChatAppRight extends React.Component {
  componentDidMount() {
    this.dispatchResize();
  }

  componentWillUnmount() {
    this.dispatchResize();
  }

  dispatchResize = () => {
    const event = document.createEvent('HTMLEvents');
    event.initEvent('resize', true, true);
    document.dispatchEvent(event);
  };

  getTitle = () => {
    const channelTitle = <Translate value="channels.rightTitleAbout" name={this.props.channel.title} />;
    switch (this.props.componentId) {
    case CONTENTS_IDS.details:
      return channelTitle;
    case CONTENTS_IDS.info:
      return channelTitle;
    case CONTENTS_IDS.pinned:
      return channelTitle;
    case CONTENTS_IDS.files:
      return channelTitle;
    case CONTENTS_IDS.members:
      return channelTitle;
    default:
      return '';
    }
  };

  render() {
    const { classes, updateChatApp } = this.props;
    return (
      <div className={classes.container}>
        <AppBar className={classes.appBar}>
          <Toolbar>
            <Typography type="title" color="primary" className={classes.appBarContent}>
              {this.getTitle()}
            </Typography>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={() => {
                return updateChatApp('chatApp', { right: { open: false, componentId: undefined } });
              }}
            >
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>

        {ChatAppRightContent(this.props)}
      </div>
    );
  }
}

export const mapDispatchToProps = {
  updateChatApp: updateApp
};

export const mapStateToProps = (state) => {
  return {
    componentId: state.apps.chatApp.right.componentId,
    subject: state.apps.chatApp.subject
  };
};
export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(ChatAppRight));