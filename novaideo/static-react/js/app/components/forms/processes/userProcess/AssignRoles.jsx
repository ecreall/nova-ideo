/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { Form, Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';
import Snackbar from '@material-ui/core/Snackbar';

import SnackbarContent from '../../../common/SnackbarContent';
import { renderSelectList } from '../../utils';
import Button from '../../../styledComponents/Button';
import { assignRoles } from '../../../../graphql/processes/userProcess';
import AssignRoles from '../../../../graphql/processes/userProcess/mutations/AssignRoles.graphql';

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
    success: false,
    error: false
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { formData, valid, account } = this.props;
    if (valid) {
      this.setState({ loading: true }, () => {
        this.props
          .assignRoles({
            context: account,
            roles: Object.keys(formData.values.roles)
          })
          .then((value) => {
            const status = value.data.assignRoles.status;
            this.setState({ loading: false, success: status, error: !status }, this.initializeForm);
          })
          .catch(() => {
            this.setState({ loading: false, success: false, error: true });
          });
      });
    }
  };

  initializeForm = () => {
    const { form, account } = this.props;
    this.props.dispatch(initialize(form, { roles: this.getRoles(account.roles) }));
  };

  getRoles = (rolesIds) => {
    const roles = {};
    rolesIds.forEach((role) => {
      roles[role] = I18n.t(`roles.${role}`);
    });
    return roles;
  };

  handleSnackbarClose = () => {
    this.setState({ success: false, error: false });
  };

  render() {
    const {
      globalProps: { site },
      valid,
      classes,
      theme
    } = this.props;
    const { loading, error, success } = this.state;
    return (
      <Form className={classes.form} onSubmit={this.handleSubmit}>
        <Field
          props={{
            label: I18n.t('forms.assignRoles.roles'),
            options: this.getRoles(site.roles)
          }}
          withRef
          name="roles"
          component={renderSelectList}
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
            message={I18n.t('forms.assignRoles.confirmation')}
          />
        </Snackbar>
        <Snackbar
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          autoHideDuration={6000}
          open={error}
          onClose={this.handleSnackbarClose}
        >
          <SnackbarContent onClose={this.handleSnackbarClose} variant="error" message={I18n.t('forms.assignRoles.error')} />
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
              {I18n.t('forms.assignRoles.save')}
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
  if (!values.roles || Object.keys(values.roles).length === 0) {
    errors.roles = requiredMessage;
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

const AssignRolesReduxFormWithMutation = graphql(AssignRoles, {
  props: function (props) {
    return {
      assignRoles: assignRoles(props)
    };
  }
})(AssignRolesReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(AssignRolesReduxFormWithMutation));