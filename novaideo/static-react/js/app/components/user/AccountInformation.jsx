import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import classNames from 'classnames';
import { connect } from 'react-redux';

import UserAvatar from './UserAvatar';

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

export const DumbAccountInformation = ({ account, classes, onlyIcon }) => {
  const picture = account && account.picture;
  const title = account && account.title;
  return (
    <div className={classes.accountInfo}>
      <div className={classes.accountTitle}>
        <UserAvatar
          isAnonymous={!account}
          anonymousIcon="account"
          picture={picture}
          classes={{ avatar: classes.avatar }}
          title={title}
        />
        {!onlyIcon &&
          <div className={classNames('account-title-text', classes.accountTitleText)}>
            {title}
          </div>}
      </div>
    </div>
  );
};

export const mapStateToProps = (state) => {
  return {
    account: state.globalProps.account
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(DumbAccountInformation));