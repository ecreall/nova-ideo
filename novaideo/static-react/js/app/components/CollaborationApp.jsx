import React from 'react';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import { Picker } from 'emoji-mart';
import 'emoji-mart/css/emoji-mart.css';

import Navbar from './Navbar';
import Footer from './Footer';
import App from './common/App';

const styles = {
  maxContainer: {
    maxWidth: 1400,
    marginRight: 'auto',
    marginLeft: 'auto'
  }
};

function CollaborationApp({ children, active, left, classes, theme }) {
  return (
    <App active={active} left={left} Navbar={Navbar}>
      <div className={classes.maxContainer}>
        <Grid container>
          <Grid item xs={12} md={3} />
          <Grid item xs={12} md={6}>
            {children}
          </Grid>
          <Grid item xs={12} md={3}>
            <Footer />
            <Picker
              color={theme.palette.primary[500]}
              title="Emoji"
              emoji="slightly_smiling_face"
              sheetSize={32}
              style={{
                fontFamily: '"LatoWebMedium", "Helvetica Neue", Helvetica, Arial, sans-serif'
              }}
              onClick={(e) => {
                console.log(e);
              }}
            />
          </Grid>
        </Grid>
      </div>
    </App>
  );
}

export default withStyles(styles, { withTheme: true })(CollaborationApp);