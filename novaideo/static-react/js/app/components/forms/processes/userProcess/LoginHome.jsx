/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import { withApollo } from 'react-apollo';
import { Fade } from '@material-ui/core';
import classNames from 'classnames';
import Avatar from '@material-ui/core/Avatar';

import { PROCESSES, ACTIONS } from '../../../../processes';
import { goTo, get } from '../../../../utils/routeMap';
import { filterActions } from '../../../../utils/processes';
import LoginForm from './LoginForm';
import Registration from './Registration';
import ResetPassword from './ResetPassword';
import { getFormId } from '../../../../utils/globalFunctions';
import { LOGIN_VIEWS } from './Login';
import { HOME_IMG, DEFAULT_LOGO } from '../../../../constants';

const styles = {
  container: {
    display: 'flex',
    width: '100%',
    minHeight: '100vh'
  },
  form: {
    borderRadius: 0,
    border: 'none',
    background: 'transparent',
    boxShadow: 'none'
  },
  formContainer: { width: '40%' },
  sliderContainer: {
    transform: 'scale(0.9)'
  },
  open: {
    top: 0,
    width: '100%',
    zIndex: 1
  },
  img: {
    backgroundClip: ' padding-box',
    backgroundPosition: 'center',
    transition: 'background-position 150ms ease',
    width: '60%',
    backgroundRepeat: 'no-repeat'
  },
  headerTitle: {
    display: 'flex',
    position: 'relative',
    alignItems: 'center',
    padding: '10px 0px 0px 10px'
  },
  headerTitleText: {
    color: '#2c2d30',
    fontSize: 18,
    fontWeight: 900,
    marginLeft: 7
  },
  avatar: {
    width: 36,
    height: 36,
    borderRadius: 4
  }
};

export class DumbLoginHome extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      view: props.view || LOGIN_VIEWS.login
    };
  }

  close = () => {
    const { onClose, params, location } = this.props;
    if (onClose) onClose();
    if (params) {
      goTo((location && location.camfrom && location.camfrom) || get('root'));
    }
  };

  switchView = (view) => {
    this.setState({ view: view });
  };

  renderLogin = () => {
    const { globalProps: { rootActions }, classes } = this.props;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const loginAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      nodeId: userProcessNodes.login.nodeId
    })[0];
    const loginFormId = getFormId('user-login');
    return loginAction ? (
      <LoginForm
        classes={{ form: classes.form }}
        form={loginFormId}
        key={loginFormId}
        action={loginAction}
        switchView={this.switchView}
      />
    ) : null;
  };

  renderResetPassword = () => {
    const { globalProps: { rootActions }, classes } = this.props;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const loginAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      nodeId: userProcessNodes.login.nodeId
    })[0];
    const resetPasswordFormId = getFormId('user-reset_password');
    return loginAction ? (
      <ResetPassword
        classes={{ form: classes.form }}
        form={resetPasswordFormId}
        key={resetPasswordFormId}
        switchView={this.switchView}
      />
    ) : null;
  };

  renderRegistration = () => {
    const { globalProps: { rootActions }, classes } = this.props;
    const registrationProcessNodes = PROCESSES.registrationmanagement.nodes;
    const registrationAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      nodeId: registrationProcessNodes.registration.nodeId
    })[0];
    const registrationFormId = getFormId('user-registration');
    return registrationAction ? (
      <Registration
        classes={{ form: classes.form }}
        form={registrationFormId}
        key={registrationFormId}
        action={registrationAction}
        switchView={this.switchView}
      />
    ) : null;
  };

  render() {
    const { classes, globalProps: { site } } = this.props;
    const picture = site && site.logo;
    const { view } = this.state;
    const isLoginView = view === LOGIN_VIEWS.login;
    const isResetPasswordView = view === LOGIN_VIEWS.resetPassword;
    const isRegistrationView = view === LOGIN_VIEWS.registration;
    return (
      <div className={classes.container}>
        <div className={classes.formContainer}>
          <div className={classes.headerTitle}>
            <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : DEFAULT_LOGO} />
            <div className={classes.headerTitleText}>{site && site.title}</div>
          </div>
          <div className={classes.sliderContainer}>
            <Fade in={isLoginView}>
              <div className={classNames({ [classes.open]: isLoginView })}>{isLoginView ? this.renderLogin() : null}</div>
            </Fade>
            <Fade in={isResetPasswordView}>
              <div className={classNames({ [classes.open]: isResetPasswordView })}>
                {isResetPasswordView ? this.renderResetPassword() : null}
              </div>
            </Fade>
            <Fade in={isRegistrationView}>
              <div className={classNames({ [classes.open]: isRegistrationView })}>
                {isRegistrationView ? this.renderRegistration() : null}
              </div>
            </Fade>
          </div>
        </div>
        <div
          className={classNames(classes.img)}
          style={{
            backgroundImage: `url('${HOME_IMG}')`
          }}
        />
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps
  };
};

export default withStyles(styles, { withTheme: true })(withApollo(connect(mapStateToProps)(DumbLoginHome)));