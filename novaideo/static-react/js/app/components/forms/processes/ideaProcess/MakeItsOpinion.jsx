/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Form as ReduxForm, Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import { renderTextInput, renderSelectField } from '../../utils';
import { makeItsOpinion } from '../../../../graphql/processes/ideaProcess';
import MakeItsOpinion from '../../../../graphql/processes/ideaProcess/mutations/MakeItsOpinion.graphql';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';
import { OPINIONS } from '../../../../constants';

const styles = {
  button: {
    marginLeft: '5px !important'
  }
};

export class DumMakeItsOpinion extends React.Component {
  handleSubmit = () => {
    const { formData, valid, idea } = this.props;
    if (valid) {
      this.closeForm();
      this.props.makeItsOpinion({
        context: idea,
        opinion: formData.values.opinion,
        explanation: formData.values.explanation
      });
    }
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const {
      action, adapters, onClose, valid, classes, theme, pristine
    } = this.props;
    const opinionsBase = adapters.opinions || OPINIONS;
    const opinions = {};
    Object.keys(opinionsBase).forEach((key) => {
      opinions[key] = I18n.t(opinionsBase[key]);
    });
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
              {I18n.t('forms.makeItsOpinion.submit')}
            </Button>
          </React.Fragment>
        )}
      >
        <ReduxForm className={classes.form} onSubmit={this.handleSubmit}>
          <Field
            props={{
              label: I18n.t('forms.makeItsOpinion.opinion'),
              options: opinions
            }}
            name="opinion"
            component={renderSelectField}
          />
          <Field
            props={{
              placeholder: I18n.t('forms.makeItsOpinion.explanation'),
              label: I18n.t('forms.makeItsOpinion.explanation'),
              multiline: true
            }}
            name="explanation"
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
  if (!values.opinion) {
    errors.opinion = requiredMessage;
  }
  if (!values.explanation) {
    errors.explanation = requiredMessage;
  }
  return errors;
};

// Decorate the form component
const DumMakeItsOpinionReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true
})(DumMakeItsOpinion);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    adapters: state.adapters
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(MakeItsOpinion, {
      props: function (props) {
        return {
          makeItsOpinion: makeItsOpinion(props)
        };
      }
    })(DumMakeItsOpinionReduxForm)
  )
);