/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { Form, Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';
import Grid from '@material-ui/core/Grid';

import { renderTextInput, renderImageField, renderSelectField } from '../../utils';
import Alert from '../../../common/Alert';
import Button from '../../../styledComponents/Button';
import { asyncValidateLogin } from '../../../../utils/user';
import { LOGIN_VIEWS } from './Login';
import { registration } from '../../../../graphql/processes/userProcess';
import Registration from '../../../../graphql/processes/userProcess/mutations/Registration.graphql';
import { LANGUAGES_TITLES } from '../../../../constants';

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

export class DumbEditProfile extends React.Component {
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
      formData,
      ction,
      globalProps: { site },
      classes,
      theme
    } = this.props;
    const { loading, error, submitted } = this.state;
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
                placeholder: I18n.t('forms.singin.firstName'),
                label: I18n.t('forms.singin.firstName'),
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
                placeholder: I18n.t('forms.singin.lastName'),
                label: I18n.t('forms.singin.lastName'),
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
                placeholder: 'Description',
                label: 'Description',
                multiline: true,
                optional: true,
                classes: {
                  root: classes.titleRoot
                }
              }}
              name="description"
              component={renderTextInput}
              onChange={() => {}}
            />
            <Field
              props={{
                placeholder: 'Fonction',
                label: 'Fonction',
                optional: true,
                classes: {
                  root: classes.titleRoot
                }
              }}
              name="function"
              component={renderTextInput}
              onChange={() => {}}
            />
            <Field
              props={{
                placeholder: I18n.t('forms.singin.email'),
                label: 'Email',
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
                label: 'Langue',
                options: LANGUAGES_TITLES
              }}
              name="locale"
              component={renderSelectField}
            />

            <Grid container spacing={16}>
              <Grid item xs={12} md={6}>
                <Field
                  props={{
                    label: 'Photo de profil',
                    helper: 'Changer votre photo de profil'
                  }}
                  name="image"
                  component={renderImageField}
                  onChange={() => {}}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <Field
                  props={{
                    label: 'Image de couverture',
                    helper: 'Changer votre image de couverture'
                  }}
                  name="test"
                  component={renderImageField}
                  onChange={() => {}}
                />
              </Grid>
            </Grid>
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
const EditProfileReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  asyncValidate: asyncValidate,
  asyncChangeFields: ['email'],
  touchOnChange: true
})(DumbEditProfile);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

const EditProfileReduxFormWithMutation = graphql(Registration, {
  props: function (props) {
    return {
      registration: registration(props)
    };
  }
})(EditProfileReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EditProfileReduxFormWithMutation));