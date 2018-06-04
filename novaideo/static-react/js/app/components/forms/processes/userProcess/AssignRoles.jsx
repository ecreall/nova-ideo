/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { Form, Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';

import { renderSelectList } from '../../utils';
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
  loading: {
    display: 'flex',
    justifyContent: 'center'
  },
  alertContainer: {
    marginBottom: 20
  }
};

export class DumbAssignRoles extends React.Component {
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
      action,
      globalProps: { site },
      classes,
      theme
    } = this.props;
    const { loading, error, submitted } = this.state;
    const roles = {
      admin: 'Admin',
      examiner: 'Examiner',
      member: 'Member'
    };
    return [
      error && (
        <Alert type="danger" classes={{ container: classes.alertContainer }}>
          {I18n.t('common.failedLogin')}
        </Alert>
      ),
      <Form className={classes.form} onSubmit={this.handleSubmit}>
        {submitted ? (
          <div>{I18n.t('forms.singin.confirmationSent')}</div>
        ) : (
          <div>
            <Field
              props={{
                label: 'Current password',
                options: roles
              }}
              withRef
              name="roles"
              component={renderSelectList}
            />
            {loading ? (
              <div className={classes.loading}>
                <CircularProgress size={30} style={{ color: theme.palette.success[800] }} />
              </div>
            ) : (
              <Button type="submit" background={theme.palette.success[800]} className={classes.buttonFooter}>
                Enregistrer
              </Button>
            )}
          </div>
        )}
      </Form>
    ];
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.roles || values.roles.length === 0) {
    errors.firstName = requiredMessage;
  }
  return errors;
};

// Decorate the form component
const AssignRolesReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true
})(DumbAssignRoles);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

const AssignRolesReduxFormWithMutation = graphql(Registration, {
  props: function (props) {
    return {
      registration: registration(props)
    };
  }
})(AssignRolesReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(AssignRolesReduxFormWithMutation));