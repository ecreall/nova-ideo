import React from 'react';
import { withStyles } from '@material-ui/core/styles';

const styles = {
  container: {
    textAlign: 'center',
    padding: 15
  },
  image: {
    width: 350
  },
  message: {
    marginBottom: 15,
    marginTop: 15,
    fontSize: 15,
    fontWeight: 900,
    color: '#717274',
    lineHeight: '20px'
  }
};

export const DumbIllustration = ({ message, img, classes }) => {
  return (
    <div className={classes.container}>
      <img alt="Sticker" className={classes.image} src={img} />
      {message && <div className={classes.message}>{message}</div>}
    </div>
  );
};

export default withStyles(styles)(DumbIllustration);