/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { connect } from 'react-redux';
import {
  Form, Field, reduxForm, initialize
} from 'redux-form';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';
import Snackbar from '@material-ui/core/Snackbar';

import { renderTextInput } from '../../utils';
import SnackbarContent from '../../../common/SnackbarContent';
import { updateUserToken } from '../../../../actions/authActions';
import Button from '../../../styledComponents/Button';
import { editApiToken } from '../../../../graphql/processes/userProcess';
import EditApiToken from '../../../../graphql/processes/userProcess/mutations/EditApiToken.graphql';

const styles = {
  buttonFooter: {
    minHeight: 35,
    fontSize: 17,
    marginTop: '15px !important',
    float: 'right'
  },
  loading: {
    display: 'flex',
    justifyContent: 'center'
  },
  message: {
    marginBottom: 10
  }
};

export class DumbEditApiToken extends React.Component {
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
          .editApiToken({
            context: account,
            password: formData.values.password
          })
          .then((value) => {
            const token = value.data.editApiToken.apiToken;
            const status = value.data.editApiToken.status;
            this.setState({ loading: false, success: status, error: !status }, () => {
              if (token) {
                this.initializeForm();
                this.props.updateUserToken(token);
              }
            });
          })
          .catch(() => {
            this.setState({ loading: false, success: false, error: true });
          });
      });
    }
  };

  initializeForm = () => {
    const { form, account } = this.props;
    this.props.dispatch(initialize(form, { email: account.email }));
  };

  handleSnackbarClose = () => {
    this.setState({ success: false, error: false });
  };

  render() {
    const {
      valid, account, classes, theme
    } = this.props;
    const { loading, error, success } = this.state;
    return (
      <div>
        <div className={classes.message}>
          {I18n.t('forms.editApiToken.message')}
          {' '}
          <strong>{account.apiToken}</strong>
        </div>
        <Form className={classes.form} onSubmit={this.handleSubmit}>
          <Field
            props={{
              placeholder: I18n.t('forms.editApiToken.password'),
              label: I18n.t('forms.editApiToken.password'),
              type: 'password',
              autoComplete: 'current-password'
            }}
            name="password"
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
              message={I18n.t('forms.editApiToken.confirmation')}
            />
          </Snackbar>
          <Snackbar
            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            autoHideDuration={6000}
            open={error}
            onClose={this.handleSnackbarClose}
          >
            <SnackbarContent onClose={this.handleSnackbarClose} variant="error" message={I18n.t('forms.editApiToken.error')} />
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
                {I18n.t('forms.editApiToken.save')}
              </Button>
            )}
          </div>
        </Form>
      </div>
    );
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.password) {
    errors.password = requiredMessage;
  }
  return errors;
};

// Decorate the form component
const DumbEditApiTokenReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true
})(DumbEditApiToken);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form]
  };
};

export const mapDispatchToProps = {
  updateUserToken: updateUserToken
};

const EditApiTokenReduxFormWithMutation = graphql(EditApiToken, {
  props: function (props) {
    return {
      editApiToken: editApiToken(props)
    };
  }
})(DumbEditApiTokenReduxForm);

export default withStyles(styles, { withTheme: true })(
  connect(
    mapStateToProps,
    mapDispatchToProps
  )(EditApiTokenReduxFormWithMutation)
);