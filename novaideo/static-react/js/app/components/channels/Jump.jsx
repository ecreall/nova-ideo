import React from 'react';
import { I18n } from 'react-redux-i18n';
import { withStyles } from 'material-ui/styles';
import Button from 'material-ui/Button';
import FormatIndentIncreaseIcon from 'material-ui-icons/FormatIndentIncrease';
import Dialog, { DialogContent, DialogContentText } from 'material-ui/Dialog';

import ShortcutsManager from '../common/ShortcutsManager';
import { STYLE_CONST } from '../../constants';

const btnMargin = 15;

const styles = (theme) => {
  return {
    jump: {
      backgroundColor: theme.palette.primary.dark,
      color: theme.palette.primary.light,
      boxShadow: 'none',
      textTransform: 'none',
      margin: `6px ${btnMargin}px 0 ${btnMargin}px`,
      padding: '0 8px',
      borderRadius: 4,
      justifyContent: 'flex-start',
      fontSize: 16,
      minWidth: STYLE_CONST.drawerWidth - btnMargin * 2,
      '&:hover': {
        backgroundColor: theme.palette.primary.dark2
      }
    },
    jumpIcon: {
      width: 20,
      height: 20,
      marginRight: 5
    }
  };
};

class Jump extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false
    };
  }

  handleOpen = () => {
    this.setState({ open: true });
    // preventDefault
    return false;
  };

  handleClose = () => {
    this.setState({ open: false });
  };
  render() {
    const { classes } = this.props;
    return (
      <ShortcutsManager domain="CHATAPP" shortcuts={{ CHATAPP_OPEN_JUMP: this.handleOpen }}>
        <Button onClick={this.handleOpen} className={classes.jump} raised dense>
          <FormatIndentIncreaseIcon className={classes.jumpIcon} />
          {I18n.t('channels.jump')}
        </Button>
        <Dialog
          open={this.state.open}
          onClose={this.handleClose}
          aria-labelledby="alert-dialog-slide-title"
          aria-describedby="alert-dialog-slide-description"
        >
          <DialogContent>
            <DialogContentText id="alert-dialog-slide-description">Test</DialogContentText>
          </DialogContent>
        </Dialog>
      </ShortcutsManager>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Jump);