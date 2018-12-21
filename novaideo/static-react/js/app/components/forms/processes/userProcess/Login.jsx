/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import Zoom from '@material-ui/core/Zoom';
import Avatar from '@material-ui/core/Avatar';
import { withApollo } from 'react-apollo';
import { Fade } from '@material-ui/core';
import classNames from 'classnames';

import Alert from '../../../common/Alert';
import { DEFAULT_LOGO } from '../../../../constants';
import { PROCESSES, ACTIONS } from '../../../../processes';
import { goTo, get } from '../../../../utils/routeMap';
import { filterActions } from '../../../../utils/processes';
import Form from '../../Form';
import LoginForm from './LoginForm';
import Registration from './Registration';
import ResetPassword from './ResetPassword';
import { getFormId } from '../../../../utils/globalFunctions';

const styles = {
  maxContainer: {
    padding: 5,
    paddingTop: 35,
    maxWidth: 600
  },
  paper: {
    backgroundColor: '#fafafa'
  },
  appBarHeaderTitle: {
    display: 'flex',
    position: 'relative',
    justifyContent: 'center',
    alignItems: 'center'
  },
  appBarHeaderTitleText: {
    color: '#2c2d30',
    fontSize: 18,
    fontWeight: 900,
    marginLeft: 7
  },
  avatar: {
    width: 36,
    height: 36,
    borderRadius: 4
  },
  closeBtn: {
    '&::after': {
      display: 'block',
      position: 'absolute',
      top: '50%',
      right: 'auto',
      bottom: 'auto',
      left: -4,
      height: 20,
      transform: 'translateY(-50%)',
      borderRadius: 0,
      borderRight: '1px solid #e5e5e5',
      content: '""',
      color: '#2c2d30'
    }
  },
  alertContainer: {
    marginBottom: 20
  },
  slidesContainer: {
    position: 'relative'
  },
  open: {
    position: 'absolute',
    top: 0,
    width: '100%',
    zIndex: 1
  }
};

export const LOGIN_VIEWS = {
  login: 'login',
  registration: 'registration',
  resetPassword: 'resetPassword'
};

export class DumbLogin extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      view: props.view || LOGIN_VIEWS.login
    };
  }

  form = null;

  close = () => {
    const { onClose, params, location } = this.props;
    if (onClose) onClose();
    if (params) {
      goTo((location && location.camfrom && location.camfrom) || get('root'));
    }
  };

  closeForm = () => {
    this.form.close();
  };

  switchView = (view) => {
    this.setState({ view: view });
  };

  renderLogin = () => {
    const { globalProps: { rootActions } } = this.props;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const loginAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      nodeId: userProcessNodes.login.nodeId
    })[0];
    const loginFormId = getFormId('user-login');
    return loginAction ? (
      <LoginForm
        form={loginFormId}
        key={loginFormId}
        action={loginAction}
        onSucces={this.closeForm}
        switchView={this.switchView}
      />
    ) : null;
  };

  renderResetPassword = () => {
    const { globalProps: { rootActions } } = this.props;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const loginAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      nodeId: userProcessNodes.login.nodeId
    })[0];
    const resetPasswordFormId = getFormId('user-reset_password');
    return loginAction ? (
      <ResetPassword
        form={resetPasswordFormId}
        key={resetPasswordFormId}
        onSucces={this.closeForm}
        switchView={this.switchView}
      />
    ) : null;
  };

  renderRegistration = () => {
    const { globalProps: { rootActions } } = this.props;
    const registrationProcessNodes = PROCESSES.registrationmanagement.nodes;
    const registrationAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      nodeId: registrationProcessNodes.registration.nodeId
    })[0];
    const registrationFormId = getFormId('user-registration');
    return registrationAction ? (
      <Registration
        form={registrationFormId}
        key={registrationFormId}
        action={registrationAction}
        onSucces={this.closeForm}
        switchView={this.switchView}
      />
    ) : null;
  };

  render() {
    const {
      message, messageType, globalProps: { site }, classes
    } = this.props;
    const { view } = this.state;
    const picture = site && site.logo;
    const isLoginView = view === LOGIN_VIEWS.login;
    const isResetPasswordView = view === LOGIN_VIEWS.resetPassword;
    const isRegistrationView = view === LOGIN_VIEWS.registration;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        fullScreen
        transition={Zoom}
        onClose={this.close}
        appBar={(
          <div className={classes.appBarHeaderTitle}>
            <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : DEFAULT_LOGO} />
            <div className={classes.appBarHeaderTitleText}>{site && site.title}</div>
          </div>
        )}
        classes={{
          closeBtn: classes.closeBtn,
          maxContainer: classes.maxContainer,
          paper: classes.paper
        }}
      >
        {message && (
          <Alert type={messageType} classes={{ container: classes.alertContainer }}>
            {message}
          </Alert>
        )}
        <div className={classes.slidesContainer}>
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
      </Form>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps
  };
};

export default withStyles(styles, { withTheme: true })(withApollo(connect(mapStateToProps)(DumbLogin)));