/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Form as ReduxForm, Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import { renderTextInput } from '../../utils';
import { moderationArchive } from '../../../../graphql/processes/ideaProcess';
import ModerationArchive from '../../../../graphql/processes/ideaProcess/mutations/ModerationArchive.graphql';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';
import IdeaItem from '../../../idea/IdeaItem';

const styles = {
  button: {
    marginLeft: '5px !important'
  },
  contextContainer: {
    marginTop: 10,
    border: '1px solid #e8e8e8',
    borderRadius: 4,
    padding: 8
  }
};

export class DumArchive extends React.Component {
  handleSubmit = () => {
    const { formData, valid, idea } = this.props;
    if (valid) {
      this.closeForm();
      this.props.archiveIdea({
        context: idea,
        explanation: formData.values.explanation
      });
    }
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const {
      action, idea, onClose, valid, classes, theme, pristine
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
              background={theme.palette.danger.primary}
              className={classes.button}
              disabled={pristine || !valid}
            >
              {I18n.t(action.submission)}
            </Button>
          </React.Fragment>
        )}
      >
        <ReduxForm className={classes.form} onSubmit={this.handleSubmit}>
          {I18n.t(action.confirmation)}
          <div className={classes.contextContainer}>
            <IdeaItem node={idea} passive />
          </div>
          <Field
            props={{
              placeholder: I18n.t('forms.archiveIdea.explanation'),
              label: I18n.t('forms.archiveIdea.explanation'),
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
  if (!values.explanation) {
    errors.explanation = requiredMessage;
  }
  return errors;
};

// Decorate the form component
const DumArchiveReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true
})(DumArchive);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    adapters: state.adapters
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(ModerationArchive, {
      props: function (props) {
        return {
          archiveIdea: moderationArchive(props)
        };
      }
    })(DumArchiveReduxForm)
  )
);