import React from 'react';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import 'emoji-mart/css/emoji-mart.css';

import Navbar from './Navbar';
import Footer from './Footer';
import App from './common/App';
import Scrollbar from './common/Scrollbar';

export const styles = {
  root: {
    height: 'calc(100vh - 66px)',
    overflow: 'auto'
  },
  maxContainer: {
    maxWidth: 1400,
    marginRight: 'auto',
    marginLeft: 'auto'
  },
  scroll: {
    paddingLeft: 8,
    paddingRight: 8
  }
};

function CollaborationApp({ children, active, left, classes }) {
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
              <Grid item xs={12} md={3} />
              <Grid item xs={12} md={6}>
                {children}
              </Grid>
              <Grid item xs={12} md={3}>
                <Footer />
              </Grid>
            </Grid>
          </div>
        </Scrollbar>
      </div>
    </App>
  );
}

export default withStyles(styles)(CollaborationApp);