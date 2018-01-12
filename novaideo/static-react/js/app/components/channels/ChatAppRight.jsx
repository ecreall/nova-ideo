import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import IconButton from 'material-ui/IconButton';
import CloseIcon from 'material-ui-icons/Close';

import { updateApp } from '../../actions/actions';
import Idea from './Idea';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100%'
  },
  menuButton: {
    alignSelf: 'flex-end',
    color: '#717274',
    fontSize: 18
  }
};

const ChatAppRightContent = (props) => {
  switch (props.componentId) {
  case 'idea':
    return <Idea {...props} />;
  case 'person':
    return <div />;
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

  render() {
    const { classes, updateChatApp } = this.props;
    return (
      <div className={classes.container}>
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