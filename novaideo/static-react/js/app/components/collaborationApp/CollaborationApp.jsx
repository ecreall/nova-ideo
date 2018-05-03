import React from 'react';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import { connect } from 'react-redux';
import 'emoji-mart/css/emoji-mart.css';

import Navbar from './Navbar';
import Footer from './Footer';
import App from '../common/App';
import Scrollbar from '../common/Scrollbar';
import UserCard from '../user/UserCard';
import AnonymousCard from '../user/AnonymousCard';

export const styles = {
  root: {
    height: 'calc(100vh - 66px)',
    overflow: 'auto'
  },
  maxContainer: {
    maxWidth: 1110,
    marginTop: 25,
    marginRight: 'auto',
    marginLeft: 'auto'
  },
  scroll: {
    paddingLeft: 8,
    paddingRight: 8
  },
  userCardContainer: {
    float: 'right',
    marginRight: 16,
    marginLeft: 16,
    width: 'auto',
    maxWidth: 295,
    minWidth: 270
  }
};

function CollaborationApp({ children, active, left, account, smallScreen, classes }) {
  return (
    <App active={active} left={left} Navbar={Navbar}>
      <div className={classes.root}>
        <Scrollbar
          scrollEvent="scroll"
          classes={{
            scroll: classes.scroll
          }}
        >
          <div className={classes.maxContainer}>
            <Grid container>
              <Grid item xs={12} md={4}>
                {!account && !smallScreen ? <AnonymousCard classes={{ container: classes.userCardContainer }} /> : null}
                {account && !smallScreen ? <UserCard id={account.id} classes={{ container: classes.userCardContainer }} /> : null}
              </Grid>
              <Grid item xs={12} md={6}>
                {children}
              </Grid>
              <Grid item xs={12} md={2}>
                <Footer />
              </Grid>
            </Grid>
          </div>
        </Scrollbar>
      </div>
    </App>
  );
}

export const mapStateToProps = (state) => {
  return {
    account: state.globalProps.account,
    smallScreen: state.globalProps.smallScreen
  };
};

export default withStyles(styles)(connect(mapStateToProps)(CollaborationApp));