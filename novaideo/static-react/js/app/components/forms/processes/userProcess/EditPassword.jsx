/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { Form, Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';
import Snackbar from '@material-ui/core/Snackbar';

import { renderTextInput } from '../../utils';
import Alert from '../../../common/Alert';
import SnackbarContent from '../../../common/SnackbarContent';
import Button from '../../../styledComponents/Button';
import { LOGIN_VIEWS } from './Login';
import { editPassword } from '../../../../graphql/processes/userProcess';
import EditPassword from '../../../../graphql/processes/userProcess/mutations/EditPassword.graphql';

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
    success: false,
    error: false
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { formData, valid, account } = this.props;
    if (valid) {
      this.setState({ loading: true }, () => {
        this.props
          .editPassword({
            context: account,
            currentPassword: formData.values.currentPassword,
            password: formData.values.password
          })
          .then((value) => {
            const edited = value.data.editPassword.status;
            this.setState({ loading: false, success: edited, error: !edited }, edited ? this.initializeForm : undefined);
          })
          .catch(() => {
            this.setState({ loading: false, success: false, error: true });
          });
      });
    }
  };

  initializeForm = () => {
    const { form } = this.props;
    this.props.dispatch(initialize(form));
  };

  handleSnackbarClose = () => {
    this.setState({ success: false, error: false });
  };

  render() {
    const { action, classes, valid, theme } = this.props;
    const { loading, error, success } = this.state;
    return (
      <Form className={classes.form} onSubmit={this.handleSubmit}>
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
        />
        <Snackbar
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          autoHideDuration={6000}
          open={success}
          onClose={this.handleSnackbarClose}
        >
          <SnackbarContent
            onClose={this.handleSnackbarClose}
            variant="success"
            message={I18n.t('forms.editPassword.confirmation')}
          />
        </Snackbar>
        <Snackbar
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          autoHideDuration={6000}
          open={error}
          onClose={this.handleSnackbarClose}
        >
          <SnackbarContent onClose={this.handleSnackbarClose} variant="error" message={I18n.t('forms.editPassword.error')} />
        </Snackbar>
        <div className={classes.loading}>
          {loading ? (
            <CircularProgress size={30} style={{ color: theme.palette.success[800] }} />
          ) : (
            <Button
              type="submit"
              background={theme.palette.success[800]}
              className={classes.buttonFooter}
              disabled={this.props.pristine || !valid}
            >
              {I18n.t('forms.editPassword.save')}
            </Button>
          )}
        </div>
      </Form>
    );
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.currentPassword) {
    errors.currentPassword = requiredMessage;
  }
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
    formData: state.form[props.form]
  };
};

const EditPasswordReduxFormWithMutation = graphql(EditPassword, {
  props: function (props) {
    return {
      editPassword: editPassword(props)
    };
  }
})(EditPasswordReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EditPasswordReduxFormWithMutation));