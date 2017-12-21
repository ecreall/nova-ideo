import React from 'react';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import IconButton from 'material-ui/IconButton';
import CloseIcon from 'material-ui-icons/Close';
import { connect } from 'react-redux';

const styles = {
  root: {
    width: '100%'
  },
  flex: {
    flex: 1
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20
  }
};

class NavBar extends React.Component {
  render() {
    const { classes, className, toggleChannels, channelsOpened } = this.props;
    return (
      <div>
        <AppBar className={className} color="inherit">
          <Toolbar>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={toggleChannels(!channelsOpened)}
            >
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {};
};

export default withStyles(styles)(connect(mapStateToProps)(NavBar));