import React from 'react';
import { I18n } from 'react-redux-i18n';
import { withStyles } from 'material-ui/styles';
import Button from 'material-ui/Button';
import FormatIndentIncreaseIcon from 'material-ui-icons/FormatIndentIncrease';

import Dialog from '../common/Dialog';
import Search from '../forms/Search';

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
    },
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
          directDisplay
          appBar={
            <div className={classes.titleContainer}>
              <span className={classes.title}>Rechercher</span>
            </div>
          }
          open={this.state.open}
          onClose={this.handleClose}
        >
          <div className={classes.container}>
            <Search
              form={'globalSearch'}
              key={'globalSearch'}
              onSearch={this.handelSearch}
              onCancel={this.handleSearchCancel}
              title={'Search'}
            />
          </div>
        </Dialog>
      </ShortcutsManager>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Jump);