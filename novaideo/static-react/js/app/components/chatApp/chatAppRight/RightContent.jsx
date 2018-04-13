import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import IconButton from 'material-ui/IconButton';
import CloseIcon from 'material-ui-icons/Close';
import Icon from 'material-ui/Icon';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import classNames from 'classnames';

import { updateChatAppRight } from '../../../actions/chatAppActions';
import Scrollbar from '../../common/Scrollbar';

const styles = {
  content: {
    height: 'calc(100vh - 128px)',
    overflow: 'auto'
  },
  container: {
    display: 'block',
    flexDirection: 'column',
    height: '100%'
  },
  toolbar: {
    paddingLeft: 5,
    paddingRight: 5
  },
  menuIcon: {
    color: '#717274',
    fontSize: '18px !important'
  },
  appBar: {
    position: 'relative',
    backgroundColor: 'transparent',
    boxShadow: 'none',
    borderBottom: '1px solid #e8e8e8'
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

class RightContent extends React.Component {
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

  toggleWidth = () => {
    const { rightFull, updateRight } = this.props;
    updateRight({ full: !rightFull });
  };

  render() {
    const { title, children, classes, updateRight, rightFull } = this.props;
    return (
      <div className={classes.container}>
        <AppBar className={classes.appBar}>
          <Toolbar className={classes.toolbar}>
            <IconButton onClick={this.toggleWidth}>
              {rightFull
                ? <Icon className={classNames(classes.menuIcon, 'mdi-set mdi-arrow-collapse-right')} />
                : <Icon className={classNames(classes.menuIcon, 'mdi-set mdi-arrow-collapse-left')} />}
            </IconButton>
            <Typography type="title" color="primary" className={classes.appBarContent}>
              {title}
            </Typography>
            <IconButton
              color="primary"
              aria-label="Menu"
              onClick={() => {
                return updateRight({ open: false, componentId: undefined, full: false, props: {} });
              }}
            >
              <CloseIcon className={classes.menuIcon} />
            </IconButton>
          </Toolbar>
        </AppBar>
        <div className={classes.content}>
          <Scrollbar>
            {children}
          </Scrollbar>
        </div>
      </div>
    );
  }
}

export const mapDispatchToProps = {
  updateRight: updateChatAppRight
};

export const mapStateToProps = (state) => {
  return {
    rightFull: state.apps.chatApp.right.full
  };
};
export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(RightContent));