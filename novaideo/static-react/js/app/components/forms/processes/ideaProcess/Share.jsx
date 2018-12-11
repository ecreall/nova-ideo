/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import {
  Form as ReduxForm, Field, reduxForm, initialize
} from 'redux-form';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import { renderRichSelect, renderTextInput } from '../../utils';
import { share } from '../../../../graphql/processes/ideaProcess';
import Share from '../../../../graphql/processes/ideaProcess/mutations/Share.graphql';
import Members from '../../../../graphql/queries/Members.graphql';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';
import MemberItem from './MemberItem';

const styles = {
  button: {
    marginLeft: '5px !important'
  }
};

export class DumShare extends React.Component {
  handleSubmit = () => {
    const { formData, valid, idea } = this.props;
    if (valid) {
      this.props.share({
        context: idea,
        message: formData.values.message,
        subject: formData.values.subject,
        members: formData.values.members.map((member) => {
          return member.oid;
        })
      });
      this.initializeForm();
    }
  };

  closeForm = () => {
    this.form.close();
  };

  initializeForm = () => {
    const { form, dispatch } = this.props;
    dispatch(initialize(form));
    this.closeForm();
  };

  render() {
    const {
      action, idea, onClose, valid, classes, theme
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
              disabled={!valid}
            >
              {I18n.t('forms.share.submit')}
            </Button>
          </React.Fragment>
        )}
      >
        <ReduxForm className={classes.form} onSubmit={this.handleSubmit}>
          <Field
            props={{
              label: I18n.t('forms.share.opinion'),
              query: Members,
              Item: MemberItem,
              id: idea.id,
              placeholder: I18n.t('forms.share.addMembers'),
              getData: (entities) => {
                return entities.data ? entities.data.members : entities.members;
              }
            }}
            name="members"
            component={renderRichSelect}
          />
          <Field
            props={{
              placeholder: I18n.t('forms.share.placeholderSubject'),
              label: I18n.t('forms.share.subject')
            }}
            name="subject"
            component={renderTextInput}
          />
          <Field
            props={{
              placeholder: I18n.t('forms.share.placeholderMessage'),
              label: I18n.t('forms.share.message'),
              multiline: true
            }}
            name="message"
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
  if (!values.members || values.members.length === 0) {
    errors.members = requiredMessage;
  }
  if (!values.subject) {
    errors.subject = requiredMessage;
  }
  if (!values.message) {
    errors.message = requiredMessage;
  }
  return errors;
};

// Decorate the form component
const DumShareReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  touchOnChange: true
})(DumShare);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form]
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps)(
    graphql(Share, {
      props: function (props) {
        return {
          share: share(props)
        };
      }
    })(DumShareReduxForm)
  )
);