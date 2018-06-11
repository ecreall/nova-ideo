/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { Form, Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n, Translate } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { withApollo } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';

import { renderTextInput } from '../../utils';
import Alert from '../../../common/Alert';
import Button from '../../../styledComponents/Button';
import { asyncValidateLogin } from '../../../../utils/user';
import { userLogin, updateUserToken } from '../../../../actions/authActions';
import { LOGIN_VIEWS } from './Login';

const styles = (theme) => {
  return {
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
    newAccountContainer: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    },
    newAccountTitle: {
      fontWeight: 'bold',
      marginBottom: 5
    },
    newAccountDescription: {
      display: 'flex',
      alignItems: 'center'
    },
    buttonSubscription: {
      marginLeft: '10px !important'
    }
  };
};

export class DumbLoginForm extends React.Component {
  state = {
    loading: false,
    error: false
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { formData, valid, onSucces } = this.props;
    // context if transformation (transform a comment in to idea)
    if (valid) {
      this.setState({ loading: true }, () => {
        this.props
          .userLogin(formData.values.login, formData.values.password)
          .then(({ value }) => {
            // update the user token (see the history reducer)
            // this.props.updateUserToken(value.token);
            if (value.status) {
              this.setState({ loading: false }, () => {
                this.props.client.resetStore();
                this.initializeForm();
                if (onSucces) onSucces();
              });
            } else {
              this.setState({ loading: false, error: true });
            }
          })
          .catch(() => {
            this.setState({ loading: false });
          });
      });
    }
  };

  initializeForm = () => {
    const { form } = this.props;
    this.props.dispatch(initialize(form));
  };

  goToRegistration = () => {
    const { switchView } = this.props;
    switchView(LOGIN_VIEWS.registration);
  };

  render() {
    const {
      valid,
      action,
      globalProps: { site },
      classes,
      theme
    } = this.props;
    const { loading, error } = this.state;
    return [
      error && (
        <Alert type="danger" classes={{ container: classes.alertContainer }}>
          {I18n.t('common.failedLogin')}
        </Alert>
      ),
      <Form className={classes.form} onSubmit={this.handleSubmit}>
        <div className={classes.formContainer}>
          <div className={classes.formTitle}>
            <div className={classes.siteTitle}>
              <div>
                <Translate value={action.title} siteTitle={site.title} />
              </div>
              <div className={classes.sectionHeaderTitle}>
                <div className={classes.sectionHeaderAddon}>{window.location.host}</div>
              </div>
            </div>
            <div className={classes.description}>
              <div dangerouslySetInnerHTML={{ __html: I18n.t('forms.singin.enterLogin') }} />
            </div>
          </div>
          <Field
            props={{
              placeholder: I18n.t('forms.singin.email'),
              autoFocus: true
            }}
            name="login"
            component={renderTextInput}
            onChange={() => {}}
          />
          <Field
            props={{
              placeholder: I18n.t('forms.singin.password'),
              type: 'password',
              autoComplete: 'current-password'
            }}
            name="password"
            component={renderTextInput}
            onChange={() => {}}
          />
          {loading ? (
            <div className={classes.loading}>
              <CircularProgress size={30} style={{ color: theme.palette.success[800] }} />
            </div>
          ) : (
            <Button type="submit" background={theme.palette.success[800]} className={classes.buttonFooter}>
              {I18n.t('common.signIn')}
            </Button>
          )}
        </div>
      </Form>,
      <div className={classes.newAccountContainer}>
        <div className={classes.newAccountTitle}>{I18n.t('common.dontHaveAccount')}</div>
        {site.onlyInvitation ? (
          <div className={classes.newAccountInvitation}>{I18n.t('common.requestInvitation')}</div>
        ) : (
          <div className={classes.newAccountDescription}>
            {I18n.t('common.tryingCreateAccount')}
            <Button
              disabled={!valid}
              onClick={this.goToRegistration}
              background={theme.palette.info[500]}
              className={classes.buttonSubscription}
            >
              {I18n.t('common.createAccount')}
            </Button>
          </div>
        )}
      </div>
    ];
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.login) {
    errors.login = requiredMessage;
  }
  if (!values.password) {
    errors.password = requiredMessage;
  }
  return errors;
};

const asyncValidate = (values /* , dispatch */) => {
  return asyncValidateLogin(values.login).then((value) => {
    if (!value.status) {
      throw { login: I18n.t('forms.singin.loginNotValid') };
    }
  });
};

// Decorate the form component
const LoginReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  asyncValidate: asyncValidate,
  asyncChangeFields: ['login'],
  touchOnChange: true
})(DumbLoginForm);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

export const mapDispatchToProps = {
  userLogin: userLogin,
  updateUserToken: updateUserToken
};

export default withStyles(styles, { withTheme: true })(
  withApollo(
    connect(
      mapStateToProps,
      mapDispatchToProps
    )(LoginReduxForm)
  )
);