/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { connect } from 'react-redux';
import { I18n, Translate } from 'react-redux-i18n';
import { withStyles } from 'material-ui/styles';
import Zoom from 'material-ui/transitions/Zoom';
import Avatar from 'material-ui/Avatar';
import { withApollo } from 'react-apollo';
import { Fade } from 'material-ui/transitions';
import classNames from 'classnames';

import Alert from '../../../common/Alert';
import { DEFAULT_LOGO } from '../../../../constants';
import { PROCESSES, ACTIONS } from '../../../../processes';
import { goTo, get } from '../../../../utils/routeMap';
import { filterActions } from '../../../../utils/processes';
import Button from '../../../styledComponents/Button';
import Form from '../../Form';
import LoginForm from './LoginForm';
import Registration from './Registration';

const styles = (theme) => {
  return {
    maxContainer: {
      padding: 5,
      paddingTop: 35,
      maxWidth: 600
    },
    form: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 6,
      border: '1px solid #e8e8e8',
      background: 'white',
      boxShadow: '0 1px 1px rgba(0, 0, 0, 0.15)',
      padding: 32,
      marginBottom: 32
    },
    formContainer: {
      maxWidth: 400,
      width: '100%'
    },
    siteTitle: {
      fontSize: 32,
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: 35,
      color: '#2c2d30',
      letterSpacing: -1
    },
    description: {
      fontSize: 16,
      marginBottom: 20,
      color: '#2c2d30'
    },
    paper: {
      backgroundColor: '#fafafa'
    },
    sectionHeaderTitle: {
      display: 'flex',
      position: 'relative',
      justifyContent: 'center'
    },
    sectionHeaderAddon: {
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      textDecoration: 'none',
      color: '#a0a0a2',
      fontWeight: 500,
      fontSize: 15
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
    button: {
      height: 40,
      width: 40,
      color: theme.palette.primary[500]
    },
    buttonFooter: {
      width: '100%',
      minHeight: 45,
      fontSize: 18,
      fontWeight: 900
    },
    titleRoot: {
      height: 45
    },
    formTitle: {
      flexGrow: 1
    },
    header: {
      display: 'flex',
      flexDirection: 'column',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: 900,
      display: 'flex',
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
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
    loading: {
      display: 'flex',
      justifyContent: 'center'
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
};

export const LOGIN_VIEWS = {
  login: 'login',
  registration: 'registration'
};

export class DumbLogin extends React.Component {
  state = {
    view: LOGIN_VIEWS.login
  };

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

  render() {
    const { action, message, messageType, globalProps: { site, rootActions }, classes } = this.props;
    const { view } = this.state;
    let loginAction = action;
    if (!loginAction) {
      const userProcessNodes = PROCESSES.usermanagement.nodes;
      loginAction = filterActions(rootActions, {
        tags: [ACTIONS.mainMenu, ACTIONS.site],
        behaviorId: userProcessNodes.login.nodeId
      })[0];
    }
    const picture = site && site.logo;
    const userProcessNodes = PROCESSES.registrationmanagement.nodes;
    const registrationAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      behaviorId: userProcessNodes.registration.nodeId
    })[0];
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        fullScreen
        transition={Zoom}
        onClose={this.close}
        appBar={
          <div className={classes.appBarHeaderTitle}>
            <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : DEFAULT_LOGO} />
            <div className={classes.appBarHeaderTitleText}>
              {site && site.title}
            </div>
          </div>
        }
        classes={{
          closeBtn: classes.closeBtn,
          maxContainer: classes.maxContainer,
          paper: classes.paper
        }}
      >
        {message &&
          <Alert type={messageType} classes={{ container: classes.alertContainer }}>
            {message}
          </Alert>}
        <div className={classes.slidesContainer}>
          <Fade in={view === LOGIN_VIEWS.login}>
            <div className={classNames({ [classes.open]: view === LOGIN_VIEWS.login })}>
              {loginAction &&
                <LoginForm
                  form="user-login"
                  key="user-login"
                  action={loginAction}
                  onSucces={this.closeForm}
                  switchView={this.switchView}
                />}
            </div>
          </Fade>
          <Fade in={view === LOGIN_VIEWS.registration}>
            <div className={classNames({ [classes.open]: view === LOGIN_VIEWS.registration })}>
              {registrationAction &&
                <Registration
                  form="user-registration"
                  key="user-registration"
                  action={registrationAction}
                  onSucces={this.closeForm}
                  switchView={this.switchView}
                />}
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