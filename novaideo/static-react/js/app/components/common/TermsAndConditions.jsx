/* eslint-disable react/no-array-index-key, no-underscore-dangle */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import Dialog from '../common/Dialog';

const styles = (theme) => {
  return {
    container: {
      padding: '20px 25px',
      width: '100%',
      fontSize: 17,
      lineHeight: 1.5
    },
    titleContainer: {
      fontWeight: 900
    },
    title: {
      marginLeft: 5
    },
    button: {
      fontWeight: 'bold',
      color: theme.palette.info[500],
      '&:hover': {
        textDecoration: 'underline'
      }
    }
  };
};

export class DumbTermsAndConditions extends React.Component {
  state = {
    open: false
  };

  handleClickOpen = (event) => {
    event.preventDefault();
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  render() {
    const { classes } = this.props;
    return [
      <span className={classes.button} onClick={this.handleClickOpen}>
        {I18n.t('common.termesConditions')}
      </span>,
      this.state.open &&
        <Dialog
          directDisplay
          appBar={
            <div className={classes.titleContainer}>
              <span className={classes.title}>
                {I18n.t('common.termesConditions')}
              </span>
            </div>
          }
          open={this.state.open}
          onClose={this.handleClose}
        >
          <div className={classes.container}>Termes & conditions text</div>
        </Dialog>
    ];
  }
}

export default withStyles(styles, { withTheme: true })(DumbTermsAndConditions);