/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n, Translate } from 'react-redux-i18n';
import { withStyles } from 'material-ui/styles';
import { withApollo } from 'react-apollo';
import { CircularProgress } from 'material-ui/Progress';

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
    }
  };
};

export class DumbRegistrationForm extends React.Component {
  state = {
    loading: false
  };

  handleSubmit = () => {
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

  goToLogin = () => {
    const { switchView } = this.props;
    switchView(LOGIN_VIEWS.login);
  };

  render() {
    const { action, globalProps: { site }, classes, theme } = this.props;
    const { loading, error } = this.state;
    return [
      error &&
        <Alert type="danger" classes={{ container: classes.alertContainer }}>
          {I18n.t('common.failedLogin')}
        </Alert>,
      <form className={classes.form}>
        <div className={classes.formContainer}>
          <div className={classes.formTitle}>
            <div className={classes.siteTitle}>
              <div>
                <Translate value={action.title} siteTitle={site.title} />
              </div>
            </div>
          </div>

          <Field
            props={{
              placeholder: 'First name',
              classes: {
                root: classes.titleRoot
              }
            }}
            name="firstName"
            component={renderTextInput}
            onChange={() => {}}
          />
          <Field
            props={{
              placeholder: 'Last name',
              classes: {
                root: classes.titleRoot
              }
            }}
            name="lastName"
            component={renderTextInput}
            onChange={() => {}}
          />
          <Field
            props={{
              placeholder: 'votre.email@test.com',
              type: 'email',
              classes: {
                root: classes.titleRoot
              },
              autoFocus: true
            }}
            name="email"
            component={renderTextInput}
            onChange={() => {}}
          />
          <Field
            props={{
              placeholder: 'Password',
              type: 'password',
              autoComplete: 'current-password',
              classes: {
                root: classes.titleRoot
              }
            }}
            name="password"
            component={renderTextInput}
            onChange={() => {}}
          />
          <Field
            props={{
              placeholder: 'Repeat password',
              type: 'password',
              autoComplete: 'current-password',
              classes: {
                root: classes.titleRoot
              }
            }}
            name="confirmPassword"
            component={renderTextInput}
            onChange={() => {}}
          />
          {loading
            ? <div className={classes.loading}>
              <CircularProgress size={30} style={{ color: theme.palette.success[500] }} />
            </div>
            : <Button onClick={this.handleSubmit} background={theme.palette.success[500]} className={classes.buttonFooter}>
              {I18n.t('common.signIn')}
            </Button>}
        </div>
      </form>,
      <div>
        <strong>You have an account on this platform?</strong>
        <div onClick={this.goToLogin}>Login</div>
      </div>
    ];
  }
}

const validate = (values) => {
  const errors = {};
  if (!values.firstName) {
    errors.firstName = 'Required';
  }
  if (!values.lastName) {
    errors.lastName = 'Required';
  }
  if (!values.email) {
    errors.email = 'Required';
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = 'Invalid email address';
  }
  if (!values.password) {
    errors.password = 'Required';
  } else if (!values.confirmPassword) {
    errors.confirmPassword = 'Required';
  } else if (values.password !== values.confirmPassword) {
    errors.confirmPassword = 'The passwords that you have entered do not match';
  }

  return errors;
};

const asyncValidate = (values /* , dispatch */) => {
  return asyncValidateLogin(values.email).then((value) => {
    // simulate server latency
    if (value.status) {
      throw { email: 'Email address used' };
    }
  });
};

// Decorate the form component
const RegistrationReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  asyncValidate: asyncValidate,
  asyncChangeFields: ['email'],
  touchOnChange: true
})(DumbRegistrationForm);

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
  withApollo(connect(mapStateToProps, mapDispatchToProps)(RegistrationReduxForm))
);