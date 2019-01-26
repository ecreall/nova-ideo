/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import {
  Form, Field, reduxForm, initialize
} from 'redux-form';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';

import { renderTextInput } from '../../utils';
import Alert from '../../../common/Alert';
import Button from '../../../styledComponents/Button';
import { asyncValidateLogin } from '../../../../utils/user';
import { LOGIN_VIEWS } from './Login';
import { resetPassword } from '../../../../graphql/processes/userProcess';
import ResetPassword from '../../../../graphql/processes/userProcess/mutations/ResetPassword.graphql';

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
  description: {
    fontSize: 16,
    marginBottom: 20,
    color: '#2c2d30',
    textAlign: 'center'
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
  alertContainer: {
    marginBottom: 20
  },
  newAccountDescription: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  buttonSubscription: {
    marginLeft: '10px !important'
  }
};

export class DumbResetPasswordForm extends React.Component {
  state = {
    submitted: false
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { formData, valid } = this.props;
    if (valid) {
      this.props
        .resetPassword({
          email: formData.values.email
        })
        .then(() => {
          this.setState({ submitted: true }, this.initializeForm);
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
      valid, globalProps: { site }, classes, theme
    } = this.props;
    const { error, submitted } = this.state;
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
                <div>{I18n.t('forms.resetPassword.title')}</div>
              </div>
              {!submitted ? (
                <div className={classes.description}>
                  <div dangerouslySetInnerHTML={{ __html: I18n.t('forms.resetPassword.description', { site: site.title }) }} />
                </div>
              ) : null}
            </div>
            {submitted ? (
              <div>{I18n.t('forms.resetPassword.resetPasswordSended')}</div>
            ) : (
              <div>
                <Field
                  props={{
                    placeholder: I18n.t('forms.singin.email'),
                    type: 'email'
                  }}
                  name="email"
                  component={renderTextInput}
                />
                <Button disabled={!valid} type="submit" background={theme.palette.success[800]} className={classes.buttonFooter}>
                  {I18n.t('forms.resetPassword.submit')}
                </Button>
              </div>
            )}
          </div>
        </Form>
        <div className={classes.newAccountDescription}>
          {I18n.t('common.tryingCreateAccount')}
          <Button onClick={this.goToRegistration} background={theme.palette.info[500]} className={classes.buttonSubscription}>
            {I18n.t('common.createAccount')}
          </Button>
        </div>
      </React.Fragment>
    );
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.email) {
    errors.email = requiredMessage;
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
    errors.email = I18n.t('forms.singin.invalidEmail');
  }

  return errors;
};

const asyncValidate = (values) => {
  return asyncValidateLogin(values.email).then((value) => {
    if (!value.status) {
      throw { email: I18n.t('forms.singin.loginNotValid') };
    }
  });
};

// Decorate the form component
const ResetPasswordReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  asyncValidate: asyncValidate,
  asyncChangeFields: ['email'],
  touchOnChange: true
})(DumbResetPasswordForm);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

const ResetPasswordReduxFormWithMutation = graphql(ResetPassword, {
  props: function (props) {
    return {
      resetPassword: resetPassword(props)
    };
  }
})(ResetPasswordReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(ResetPasswordReduxFormWithMutation));