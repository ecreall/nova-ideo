import React from 'react';
import { withStyles } from 'material-ui/styles';
import KeyboardArrowDownIcon from 'material-ui-icons/KeyboardArrowDown';
import { connect } from 'react-redux';

import AccountInformation from '../AccountInformation';

const styles = (theme) => {
  return {
    drawerHeader: {
      padding: '0 15px',
      paddingBottom: 2,
      cursor: 'pointer',
      ...theme.mixins.toolbar,
      '&:hover': {
        backgroundColor: 'rgba(0, 0, 0, 0.12)',
        '& .account-title-text': {
          color: 'white'
        }
      }
    },
    siteInfo: {
      display: 'flex',
      alignItems: 'center',
      marginTop: 9,
      marginBottom: 5
    },
    siteTitle: {
      display: 'block',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      fontSize: 17,
      lineHeight: 1.375,
      fontWeight: 900,
      color: '#fff'
    },
    arrow: {
      color: 'white',
      width: 17,
      height: 17
    }
  };
};

class ChannelsMenu extends React.Component {
  render() {
    const { site, classes, theme } = this.props;
    return (
      <div className={classes.drawerHeader}>
        <div className={classes.siteInfo}>
          <div className={classes.siteTitle}>
            {site.title}
          </div>
          <KeyboardArrowDownIcon className={classes.arrow} />
        </div>
        <AccountInformation color={theme.palette.primary.light} />
      </div>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    site: state.globalProps.siteConf
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(ChannelsMenu));