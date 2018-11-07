import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Icon from '@material-ui/core/Icon';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import classNames from 'classnames';

import { updateCollaborationAppRight, closeCollaborationRight } from '../../../actions/collaborationAppActions';
import { createEvent } from '../../../utils/globalFunctions';
import Scrollbar from '../../common/Scrollbar';

const styles = {
  content: {
    height: 'calc(100vh - 130px)',
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
    createEvent('resize', true);
  }

  componentWillUnmount() {
    createEvent('resize', true);
  }

  toggleWidth = () => {
    const { rightFull, updateRight } = this.props;
    updateRight({ full: !rightFull });
  };

  render() {
    const {
      title, children, classes, rightFull, closeRight
    } = this.props;
    return (
      <div className={classes.container}>
        <AppBar className={classes.appBar}>
          <Toolbar className={classes.toolbar}>
            <IconButton onClick={this.toggleWidth}>
              {rightFull ? (
                <Icon className={classNames(classes.menuIcon, 'mdi-set mdi-arrow-collapse-right')} />
              ) : (
                <Icon className={classNames(classes.menuIcon, 'mdi-set mdi-arrow-collapse-left')} />
              )}
            </IconButton>
            <Typography component="div" type="title" color="primary" className={classes.appBarContent}>
              {title}
            </Typography>
            <IconButton
              color="primary"
              aria-label="Menu"
              onClick={() => {
                closeRight({});
              }}
            >
              <CloseIcon className={classes.menuIcon} />
            </IconButton>
          </Toolbar>
        </AppBar>
        <div className={classes.content}>
          <Scrollbar>{children}</Scrollbar>
        </div>
      </div>
    );
  }
}

export const mapDispatchToProps = {
  updateRight: updateCollaborationAppRight,
  closeRight: closeCollaborationRight
};

export const mapStateToProps = (state) => {
  return {
    rightFull: state.apps.collaborationApp.right.full
  };
};
export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(RightContent));