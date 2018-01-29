import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import KeyboardArrowDownIcon from 'material-ui-icons/KeyboardArrowDown';

import AccountInformation from '../AccountInformation';
import Menu from '../common/Menu';

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
        },
        '& .arrow': {
          color: 'white'
        }
      }
    },
    drawerHeaderActive: {
      backgroundColor: 'rgba(0, 0, 0, 0.12)',
      '& .account-title-text': {
        color: 'white'
      },
      '& .arrow': {
        color: 'white'
      }
    },
    siteInfo: {
      display: 'flex',
      alignItems: 'center',
      paddingTop: 9,
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
      color: theme.palette.primary.light,
      width: 17,
      height: 17
    }
  };
};

class ChannelsMenu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      menu: false
    };
  }

  onMenuOpen = () => {
    this.setState({ menu: true });
  };

  onMenuClose = () => {
    this.setState({ menu: false });
  };

  render() {
    const { site, classes, theme } = this.props;
    const { menu } = this.state;
    return (
      <Menu
        id="user-menu"
        onOpen={this.onMenuOpen}
        onClose={this.onMenuClose}
        fields={[
          {
            title: 'Test'
          },
          {
            title: 'Un autre test avec couleurUn autre test avec couleur',
            color: '#d72b3f',
            hoverColor: '#d72b3f'
          }
        ]}
        classes={{
          menu: classes.menu
        }}
      >
        <div className={classNames(classes.drawerHeader, { [classes.drawerHeaderActive]: menu })}>
          <div className={classes.siteInfo}>
            <div className={classes.siteTitle}>
              {site.title}
            </div>
            <KeyboardArrowDownIcon className={classNames('arrow', classes.arrow)} />
          </div>
          <AccountInformation color={theme.palette.primary.light} />
        </div>
      </Menu>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    site: state.globalProps.siteConf
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(ChannelsMenu));