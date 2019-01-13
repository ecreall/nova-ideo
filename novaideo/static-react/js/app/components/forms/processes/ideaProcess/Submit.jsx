/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import { submit } from '../../../../graphql/processes/ideaProcess';
import Submit from '../../../../graphql/processes/ideaProcess/mutations/Submit.graphql';
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

export class Dumbsubmit extends React.Component {
  form = null;

  handleSubmit = () => {
    const { idea } = this.props;
    this.closeForm();
    this.props.submitIdea({
      context: idea
    });
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const {
      action, idea, onClose, classes, theme
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
            <Button onClick={this.handleSubmit} background={theme.palette.success[500]} className={classes.button}>
              {I18n.t(action.submission)}
            </Button>
          </React.Fragment>
        )}
      >
        {I18n.t(action.confirmation)}
        <div className={classes.contextContainer}>
          <IdeaItem node={idea} passive />
        </div>
      </Form>
    );
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(Submit, {
    props: function (props) {
      return {
        submitIdea: submit(props)
      };
    }
  })(Dumbsubmit)
);