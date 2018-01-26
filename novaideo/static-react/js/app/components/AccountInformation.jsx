import React from 'react';
import { withStyles } from 'material-ui/styles';
import classNames from 'classnames';
import Avatar from 'material-ui/Avatar';
import { connect } from 'react-redux';

const styles = (theme) => {
  return {
    accountInfo: {},
    accountTitle: {
      display: 'flex',
      position: 'relative',
      alignItems: 'center',
      justifyContent: 'flex-start'
    },
    accountTitleText: {
      color: theme.palette.primary.light,
      fontSize: 14,
      fontWeight: 400,
      paddingLeft: 7,
      fontFamily: 'LatoWebLight'
    },
    avatar: {
      width: 18,
      height: 18,
      borderRadius: 4
    }
  };
};

class AccountInformation extends React.Component {
  render() {
    const { account, classes, onlyIcon } = this.props;
    const picture = account.picture;
    return (
      <div className={classes.accountInfo}>
        <div className={classes.accountTitle}>
          <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : ''} />
          {!onlyIcon &&
            <div className={classNames('account-title-text', classes.accountTitleText)}>
              {account.title}
            </div>}
        </div>
      </div>
    );
  }
}

export const mapStateToProps = (state) => {
  return {
    account: state.globalProps.account
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(AccountInformation));