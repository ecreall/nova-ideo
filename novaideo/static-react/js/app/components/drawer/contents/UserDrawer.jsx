import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';

import Contents from './Contents';
import Jump from './Jump';
import Illustration from '../../common/Illustration';
import LoginButton from '../../common/LoginButton';
import { NOT_LOGGED } from '../../../constants';

const styles = {
  imgIllustration: {
    width: 180,
    opacity: 0.8
  },
  illustrationContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '80%',
    overflow: 'hidden'
  },
  illustrationMessage: {
    color: 'white',
    opacity: 0.7,
    fontWeight: 100,
    fontSize: 13,
    marginBottom: 7
  }
};

function UserDrawer({ account, classes }) {
  return account ? (
    [<Jump />, <Contents />]
  ) : (
    <Illustration
      img={NOT_LOGGED}
      message={(
        <React.Fragmet>
          <div className={classes.illustrationMessage}>{I18n.t('user.noUserContents')}</div>
          <LoginButton />
        </React.Fragmet>
      )}
      classes={{
        container: classes.illustrationContainer,
        image: classes.imgIllustration
      }}
    />
  );
}

export const mapStateToProps = (state) => {
  return {
    account: state.globalProps.account
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(UserDrawer));