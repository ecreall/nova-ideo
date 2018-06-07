/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { Form, Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';
import Grid from '@material-ui/core/Grid';
import Snackbar from '@material-ui/core/Snackbar';

import { renderTextInput, renderImageField, renderSelectField } from '../../utils';
import SnackbarContent from '../../../common/SnackbarContent';
import Button from '../../../styledComponents/Button';
import { asyncValidateLogin } from '../../../../utils/user';
import { editProfile } from '../../../../graphql/processes/userProcess';
import EditProfileMutation from '../../../../graphql/processes/userProcess/mutations/EditProfile.graphql';
import { LANGUAGES_TITLES } from '../../../../constants';

const styles = {
  form: {
    padding: 15
  },
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
  alertContainer: {
    marginBottom: 20
  }
};

export class DumbEditProfile extends React.Component {
  state = {
    loading: false,
    success: false,
    error: false
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { formData, valid, account } = this.props;
    if (valid) {
      const picture = formData.values.picture;
      const coverPicture = formData.values.coverPicture;
      const oldPicture = picture && picture.oid;
      const oldCoverPicture = coverPicture && coverPicture.oid;
      this.setState({ loading: true }, () => {
        this.props
          .editProfile({
            context: account,
            firstName: formData.values.firstName,
            lastName: formData.values.lastName,
            description: formData.values.description,
            userFunction: formData.values.function,
            email: formData.values.email,
            locale: formData.values.locale,
            picture: picture,
            oldPicture: oldPicture,
            coverPicture: coverPicture,
            oldCoverPicture: oldCoverPicture
          })
          .then(() => {
            this.setState({ loading: false, success: true, error: false }, this.initializeForm);
          })
          .catch(() => {
            this.setState({ loading: false, success: false, error: true });
          });
      });
    }
  };

  initializeForm = () => {
    const { form, account } = this.props;
    this.props.reset();
    const functionKey = 'function';
    this.props.dispatch(
      initialize(form, {
        firstName: account.firstName,
        lastName: account.lastName,
        description: account.description,
        [functionKey]: account.function,
        email: account.email,
        locale: account.locale,
        picture: account.picture && {
          id: account.picture.id,
          oid: account.picture.oid,
          name: account.picture.title,
          size: account.picture.size || 0,
          mimetype: account.picture.mimetype,
          type: account.picture.mimetype,
          preview: { url: account.picture.url, type: 'image' }
        },
        coverPicture: account.coverPicture && {
          id: account.coverPicture.id,
          oid: account.coverPicture.oid,
          name: account.coverPicture.title,
          size: account.coverPicture.size || 0,
          mimetype: account.coverPicture.mimetype,
          type: account.coverPicture.mimetype,
          preview: { url: account.coverPicture.url, type: 'image' }
        }
      })
    );
  };

  handleSnackbarClose = () => {
    this.setState({ success: false, error: false });
  };

  render() {
    const { classes, valid, theme } = this.props;
    const { loading, error, success } = this.state;
    return (
      <Form className={classes.form} onSubmit={this.handleSubmit}>
        <Field
          props={{
            placeholder: I18n.t('forms.singin.firstName'),
            label: I18n.t('forms.singin.firstName'),
            autoFocus: true
          }}
          name="firstName"
          component={renderTextInput}
        />
        <Field
          props={{
            placeholder: I18n.t('forms.singin.lastName'),
            label: I18n.t('forms.singin.lastName')
          }}
          name="lastName"
          component={renderTextInput}
        />
        <Field
          props={{
            placeholder: 'Description',
            label: 'Description',
            multiline: true,
            optional: true
          }}
          name="description"
          component={renderTextInput}
        />
        <Field
          props={{
            placeholder: 'Fonction',
            label: 'Fonction',
            optional: true
          }}
          name="function"
          component={renderTextInput}
        />
        <Field
          props={{
            placeholder: I18n.t('forms.singin.email'),
            label: 'Email',
            type: 'email'
          }}
          name="email"
          component={renderTextInput}
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
              name="picture"
              component={renderImageField}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <Field
              props={{
                label: 'Image de couverture',
                helper: 'Changer votre image de couverture'
              }}
              name="coverPicture"
              component={renderImageField}
            />
          </Grid>
        </Grid>
        <Snackbar
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          autoHideDuration={6000}
          open={success}
          onClose={this.handleSnackbarClose}
        >
          <SnackbarContent
            onClose={this.handleSnackbarClose}
            variant="success"
            message={I18n.t('forms.editProfile.confirmation')}
          />
        </Snackbar>
        <Snackbar
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
          autoHideDuration={6000}
          open={error}
          onClose={this.handleSnackbarClose}
        >
          <SnackbarContent onClose={this.handleSnackbarClose} variant="error" message={I18n.t('forms.editProfile.error')} />
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
              {I18n.t('forms.editProfile.save')}
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
    formData: state.form[props.form]
  };
};

const EditProfileReduxFormWithMutation = graphql(EditProfileMutation, {
  props: function (props) {
    return {
      editProfile: editProfile(props)
    };
  }
})(EditProfileReduxForm);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EditProfileReduxFormWithMutation));