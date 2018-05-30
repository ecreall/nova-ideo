/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { Form, Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';

import { renderTextInput } from '../../utils';
import Alert from '../../../common/Alert';
import Button from '../../../styledComponents/Button';
import { LOGIN_VIEWS } from './Login';
import { registration } from '../../../../graphql/processes/userProcess';
import Registration from '../../../../graphql/processes/userProcess/mutations/Registration.graphql';

const styles = {
  form: {
    padding: 15
  },
  buttonFooter: {
    width: '50%',
    minHeight: 45,
    fontSize: 18,
    fontWeight: 900,
    marginTop: 15,
    float: 'right'
  },
  titleRoot: {
    height: 45
  },
  loading: {
    display: 'flex',
    justifyContent: 'center'
  },
  alertContainer: {
    marginBottom: 20
  }
};

export class DumbEditPassword extends React.Component {
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
    const { action, globalProps: { site }, classes, theme } = this.props;
    const { loading, error, submitted } = this.state;
    return [
      error &&
        <Alert type="danger" classes={{ container: classes.alertContainer }}>
          {I18n.t('common.failedLogin')}
        </Alert>,
      <Form className={classes.form} onSubmit={this.handleSubmit}>
        {submitted
          ? <div>
            {I18n.t('forms.singin.confirmationSent')}
          </div>
          : <div>
            <Field
              props={{
                placeholder: 'Current password',
                label: 'Current password',
                type: 'password',
                autoComplete: 'current-password',
                classes: {
                  root: classes.titleRoot
                }
              }}
              name="currentPassword"
              component={renderTextInput}
              onChange={() => {}}
            />
            <Field
              props={{
                placeholder: I18n.t('forms.singin.password'),
                label: 'New password',
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
                placeholder: I18n.t('forms.singin.passwordConfirmation'),
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
                <CircularProgress size={30} style={{ color: theme.palette.success[800] }} />
              </div>
              : <Button type="submit" background={theme.palette.success[800]} className={classes.buttonFooter}>
                    Enregistrer
              </Button>}
          </div>}
      </Form>
    ];
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.password) {
    errors.password = requiredMessage;
  } else if (!values.confirmPassword) {
    errors.confirmPassword = requiredMessage;
  } else if (values.password !== values.confirmPassword) {
    errors.confirmPassword = I18n.t('forms.singin.passwordsNotMatch');
  }
  return errors;
};

// Decorate the form component
const EditPasswordReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true
})(DumbEditPassword);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

const EditPasswordReduxFormWithMutation = graphql(Registration, {
  props: function (props) {
    return {
      registration: registration(props)
    };
  }
})(EditPasswordReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EditPasswordReduxFormWithMutation));