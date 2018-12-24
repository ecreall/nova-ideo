/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import {
  Form as ReduxForm, Field, reduxForm, FormSection, initialize
} from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';
import Color from 'color';

import { renderCardSelect } from '../../utils';
import { editPreferences } from '../../../../graphql/processes/userProcess';
import EditPreferences from '../../../../graphql/processes/userProcess/mutations/EditPreferences.graphql';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';
import { THEMES } from '../../../../theme';

const styles = {
  button: {
    marginLeft: '5px !important'
  },
  appPreview: {
    borderRadius: 3,
    width: 110
  },
  titlePreview: {
    padding: '5px 0 1px 10px',
    fontSize: 13
  },
  listItemPreview: {
    padding: 5
  },
  listItemTextPreview: {
    padding: 3,
    borderRadius: 5
  }
};

export class DumEditPreferences extends React.Component {
  handleSubmit = () => {
    const {
      formData, valid, user, account
    } = this.props;
    if (valid) {
      const { colors: { primaryColor, secondaryColor } } = THEMES[formData.values.theme.themeId];
      this.initializeForm();
      this.props.editPreferences({
        connectedUser: account,
        context: user,
        preferences: { theme: { primaryColor: primaryColor, secondaryColor: secondaryColor } }
      });
    }
  };

  closeForm = () => {
    this.form.close();
  };

  cancel = () => {
    this.initializeForm();
  };

  initializeForm = () => {
    const { form, dispatch } = this.props;
    dispatch(initialize(form));
    this.closeForm();
  };

  renderThemePreview = (value) => {
    const { classes } = this.props;
    const { title, colors: { primaryColor, secondaryColor } } = value;
    const primary = Color(primaryColor);
    const secondary = Color(secondaryColor);
    const primaryLight = primary
      .lighten(1)
      .mix(Color('white'))
      .hex();
    const secondaryLight = secondary
      .lighten(1)
      .mix(Color('white'))
      .hex();
    return (
      <div className={classes.appPreview} style={{ backgroundColor: primaryColor }}>
        <div className={classes.titlePreview} style={{ color: primaryLight }}>
          {title}
        </div>
        <div className={classes.listPreview}>
          <div className={classes.listItemPreview} style={{ backgroundColor: secondaryColor }}>
            <div className={classes.listItemTextPreview} style={{ backgroundColor: secondaryLight }} />
          </div>
          <div className={classes.listItemPreview}>
            <div className={classes.listItemTextPreview} style={{ backgroundColor: primaryLight }} />
          </div>
          <div className={classes.listItemPreview}>
            <div className={classes.listItemTextPreview} style={{ backgroundColor: primaryLight }} />
          </div>
        </div>
      </div>
    );
  };

  getThemes = () => {
    const themes = {};
    Object.keys(THEMES).forEach((key) => {
      const value = THEMES[key];
      themes[key] = this.renderThemePreview(value);
    });
    return themes;
  };

  render() {
    const {
      action, onClose, valid, classes, theme, pristine
    } = this.props;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        appBar={I18n.t(action.description)}
        onClose={onClose}
        footer={(
          <React.Fragment>
            <CancelButton onClick={this.closeForm}>{I18n.t('forms.cancel')}</CancelButton>
            <Button
              onClick={this.handleSubmit}
              background={theme.palette.success[800]}
              className={classes.button}
              disabled={pristine || !valid}
            >
              {I18n.t('forms.save')}
            </Button>
          </React.Fragment>
        )}
      >
        <ReduxForm className={classes.form} onSubmit={this.handleSubmit}>
          <FormSection name="theme">
            <Field
              props={{
                label: I18n.t('forms.editPreferences.theme'),
                options: this.getThemes()
              }}
              name="themeId"
              component={renderCardSelect}
            />
          </FormSection>
        </ReduxForm>
      </Form>
    );
  }
}

const validate = (values) => {
  const errors = {};
  const requiredMessage = I18n.t('forms.required');
  if (!values.theme || !values.theme.themeId) {
    errors.theme = { ...errors.theme, themeId: requiredMessage };
  }
  return errors;
};

// Decorate the form component
const DumditPreferencesReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true
})(DumEditPreferences);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form]
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(EditPreferences, {
      props: function (props) {
        return {
          editPreferences: editPreferences(props)
        };
      }
    })(DumditPreferencesReduxForm)
  )
);