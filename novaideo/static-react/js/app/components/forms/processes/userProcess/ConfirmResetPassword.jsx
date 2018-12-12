import React from 'react';
import { graphql, withApollo } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import { I18n } from 'react-redux-i18n';
import {
  Form as ReduxForm, Field, reduxForm, initialize
} from 'redux-form';

import Alert from '../../../common/Alert';
import { renderTextInput } from '../../utils';
import { goTo, get } from '../../../../utils/routeMap';
import { confirmResetPassword } from '../../../../graphql/processes/userProcess';
import ConfirmResetPassword from '../../../../graphql/processes/userProcess/mutations/ConfirmResetPassword.graphql';
import { updateUserToken } from '../../../../actions/authActions';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';

const styles = {
  button: {
    marginLeft: '5px !important'
  },
  message: {
    color: 'white',
    textAlign: 'center'
  },
  paper: {
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
  },
  loading: {
    display: 'flex',
    justifyContent: 'center'
  },
  alertContainer: {
    marginBottom: 20
  }
};

const REST_FORM_ID = 'resetFormId';

export class DumbConfirmResetPassword extends React.Component {
  state = {
    loading: false,
    error: null
  };

  handleSubmit = () => {
    const { valid, params: { resetpasswordId }, formData } = this.props;
    if (valid && resetpasswordId) {
      const { password } = formData.values;
      this.setState({ loading: true, error: null }, () => {
        this.props
          .confirmResetPassword({
            context: resetpasswordId,
            password: password
          })
          .then((result) => {
            const { data: { confirmResetPassword: { token } } } = result;
            if (token) {
              this.props.updateUserToken(token);
              this.props.client.resetStore();
              this.initializeForm();
              goTo(get('root'));
            }
          })
          .catch((error) => {
            this.setState({ loading: false, error: error.graphQLErrors[0].message });
          });
      });
    }
  };

  form = null;

  closeForm = () => {
    this.form.close();
  };

  cancel = () => {
    this.initializeForm();
    goTo(get('root'));
  };

  initializeForm = () => {
    const { form, dispatch } = this.props;
    dispatch(initialize(form));
    this.closeForm();
  };

  render() {
    const { valid, classes, theme } = this.props;
    const { error, loading } = this.state;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        appBar={I18n.t('forms.confirmResetPassword.title')}
        footer={
          loading ? (
            <div className={classes.loading}>
              <CircularProgress disableShrink size={30} style={{ color: theme.palette.success[800] }} />
            </div>
          ) : (
            <React.Fragment>
              <CancelButton onClick={this.cancel}>{I18n.t('forms.cancel')}</CancelButton>
              <Button
                onClick={this.handleSubmit}
                background={theme.palette.success[800]}
                className={classes.button}
                disabled={!valid}
              >
                {I18n.t('forms.confirmResetPassword.submit')}
              </Button>
            </React.Fragment>
          )
        }
      >
        {error && (
          <Alert type="danger" classes={{ container: classes.alertContainer }}>
            {error}
          </Alert>
        )}
        <ReduxForm className={classes.form} onSubmit={this.handleSubmit}>
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
        </ReduxForm>
      </Form>
    );
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
const ConfirmResetPasswordReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true,
  form: REST_FORM_ID
})(DumbConfirmResetPassword);

const mapStateToProps = (state) => {
  return {
    formData: state.form[REST_FORM_ID]
  };
};

export const mapDispatchToProps = {
  updateUserToken: updateUserToken
};

export default withStyles(styles, { withTheme: true })(
  graphql(ConfirmResetPassword, {
    props: function (props) {
      return {
        confirmResetPassword: confirmResetPassword(props)
      };
    }
  })(withApollo(connect(mapStateToProps, mapDispatchToProps)(ConfirmResetPasswordReduxForm)))
);