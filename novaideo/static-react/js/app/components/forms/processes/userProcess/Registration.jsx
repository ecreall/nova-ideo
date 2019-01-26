/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import {
  Form, Field, reduxForm, initialize
} from 'redux-form';
import { connect } from 'react-redux';
import { I18n, Translate } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';

import { renderTextInput, renderCheckboxField } from '../../utils';
import Alert from '../../../common/Alert';
import TermsAndConditions from '../../../common/TermsAndConditions';
import Button from '../../../styledComponents/Button';
import { asyncValidateLogin } from '../../../../utils/user';
import { LOGIN_VIEWS } from './Login';
import { registration } from '../../../../graphql/processes/userProcess';
import Registration from '../../../../graphql/processes/userProcess/mutations/Registration.graphql';

const styles = {
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
    maxWidth: 450,
    width: '100%'
  },
  validationContainer: {
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
  buttonFooter: {
    width: '100%',
    minHeight: 45,
    fontSize: 18,
    fontWeight: 900
  },
  formTitle: {
    flexGrow: 1
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

export class DumbRegistrationForm extends React.Component {
  state = {
    loading: false,
    submitted: false
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { formData, valid } = this.props;
    if (valid) {
      this.setState({ loading: true }, () => {
        this.props
          .registration({
            firstName: formData.values.firstName,
            lastName: formData.values.lastName,
            email: formData.values.email,
            password: formData.values.password
          })
          .then(() => {
            this.setState({ submitted: true }, this.initializeForm);
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
    const {
      valid, action, globalProps: { site }, classes, theme
    } = this.props;
    const { loading, error, submitted } = this.state;
    return (
      <React.Fragment>
        {error ? (
          <Alert type="danger" classes={{ container: classes.alertContainer }}>
            {I18n.t('common.failedLogin')}
          </Alert>
        ) : null}
        <Form className={classes.form} onSubmit={this.handleSubmit}>
          <div className={submitted ? classes.validationContainer : classes.formContainer}>
            <div className={classes.formTitle}>
              <div className={classes.siteTitle}>
                <div>
                  {submitted ? I18n.t('forms.singin.accountCreated') : <Translate value={action.title} siteTitle={site.title} />}
                </div>
              </div>
            </div>
            {submitted ? (
              <div>{I18n.t('forms.singin.confirmationSent')}</div>
            ) : (
              <div>
                <Field
                  props={{
                    placeholder: I18n.t('forms.singin.firstName'),
                    autoFocus: true
                  }}
                  name="firstName"
                  component={renderTextInput}
                />
                <Field
                  props={{
                    placeholder: I18n.t('forms.singin.lastName')
                  }}
                  name="lastName"
                  component={renderTextInput}
                />
                <Field
                  props={{
                    placeholder: I18n.t('forms.singin.email'),
                    type: 'email'
                  }}
                  name="email"
                  component={renderTextInput}
                />
                <Field
                  props={{
                    placeholder: I18n.t('forms.singin.password'),
                    type: 'password',
                    autoComplete: 'current-password'
                  }}
                  name="password"
                  component={renderTextInput}
                />
                <Field
                  props={{
                    placeholder: I18n.t('forms.singin.passwordConfirmation'),
                    type: 'password',
                    autoComplete: 'current-password'
                  }}
                  name="confirmPassword"
                  component={renderTextInput}
                />
                <Field
                  props={{
                    label: (
                      <div>
                        {I18n.t('common.readAccept')}
                        {' '}
                        <TermsAndConditions />
                      </div>
                    )
                  }}
                  name="terms"
                  component={renderCheckboxField}
                />

                {loading ? (
                  <div className={classes.loading}>
                    <CircularProgress disableShrink size={30} style={{ color: theme.palette.success[800] }} />
                  </div>
                ) : (
                  <Button
                    disabled={!valid}
                    type="submit"
                    background={theme.palette.success[800]}
                    className={classes.buttonFooter}
                  >
                    {I18n.t('common.singUp')}
                  </Button>
                )}
              </div>
            )}
          </div>
        </Form>
        <div className={classes.newAccountContainer}>
          <div className={classes.newAccountTitle}>{I18n.t('common.haveAccount')}</div>
          <div className={classes.newAccountDescription}>
            <Button onClick={this.goToLogin} background={theme.palette.info[500]} className={classes.buttonSubscription}>
              {I18n.t('common.signIn')}
            </Button>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.firstName) {
    errors.firstName = requiredMessage;
  }
  if (!values.lastName) {
    errors.lastName = requiredMessage;
  }
  if (!values.email) {
    errors.email = requiredMessage;
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = I18n.t('forms.singin.invalidEmail');
  }
  if (!values.password) {
    errors.password = requiredMessage;
  } else if (!values.confirmPassword) {
    errors.confirmPassword = requiredMessage;
  } else if (values.password !== values.confirmPassword) {
    errors.confirmPassword = I18n.t('forms.singin.passwordsNotMatch');
  }
  if (!values.terms) {
    errors.terms = I18n.t('forms.singin.acceptTerms');
  }

  return errors;
};

const asyncValidate = (values) => {
  return asyncValidateLogin(values.email).then((value) => {
    if (value.status) {
      throw { email: I18n.t('forms.singin.emailInUse') };
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

const RegistrationReduxFormWithMutation = graphql(Registration, {
  props: function (props) {
    return {
      registration: registration(props)
    };
  }
})(RegistrationReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(RegistrationReduxFormWithMutation));