import React from 'react';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import IconButton from 'material-ui/IconButton';
import MenuIcon from 'material-ui-icons/Menu';
import ChatIcon from 'material-ui-icons/Chat';
import Drawer from 'material-ui/Drawer';
import { connect } from 'react-redux';
import AppMenu from './AppMenu';

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
  state = {
    drawerMenu: false
  };

  toggleDrawer = (drawer, open) => {
    return () => {
      this.setState({
        [drawer]: open
      });
    };
  };

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
              onClick={this.toggleDrawer('drawerMenu', true)}
            >
              <MenuIcon />
            </IconButton>
            <IconButton
              className={classes.menuButton}
              color="primary"
              aria-label="Menu"
              onClick={toggleChannels(!channelsOpened)}
            >
              <ChatIcon />
            </IconButton>
            <Typography type="title" color="primary" className={classes.flex}>
              Nova-Ideo
            </Typography>
            <Button color="primary">Login</Button>
          </Toolbar>
        </AppBar>
        <Drawer open={this.state.drawerMenu} onClose={this.toggleDrawer('drawerMenu', false)}>
          <div
            tabIndex={0}
            role="button"
            onClick={this.toggleDrawer('drawerMenu', false)}
            onKeyDown={this.toggleDrawer('drawerMenu', false)}
          >
            <AppMenu />
          </div>
        </Drawer>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {};
};

export default withStyles(styles)(connect(mapStateToProps)(NavBar));