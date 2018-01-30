import React from 'react';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import { Scrollbars } from 'react-custom-scrollbars';
import 'emoji-mart/css/emoji-mart.css';

import Navbar from './Navbar';
import Footer from './Footer';
import App from './common/App';

const styles = {
  root: {
    height: 'calc(100vh - 66px)',
    overflow: 'auto'
  },
  maxContainer: {
    maxWidth: 1400,
    marginRight: 'auto',
    marginLeft: 'auto'
  },
  trackVertical: {
    width: 8,
    height: '100%',
    top: 0,
    right: 6
  },
  thumbVertical: {
    zIndex: 1,
    cursor: 'pointer',
    borderRadius: 6,
    backgroundColor: 'rgba(0, 0, 0, 0.1)',
    border: '3px solid #fff'
  }
};

function CollaborationApp({ children, active, left, classes }) {
  return (
    <App active={active} left={left} Navbar={Navbar}>
      <div className={classes.root}>
        <Scrollbars
          renderTrackVertical={(props) => {
            return <div {...props} style={{ ...props.style, ...styles.trackVertical }} />;
          }}
          renderThumbVertical={(props) => {
            return <div {...props} style={{ ...props.style, ...styles.thumbVertical }} />;
          }}
          onScrollFrame={(values) => {
            const event = document.createEvent('HTMLEvents');
            event.initEvent('scroll', true, true);
            event.values = values;
            document.dispatchEvent(event);
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
        </Scrollbars>
      </div>
    </App>
  );
}

export default withStyles(styles)(CollaborationApp);