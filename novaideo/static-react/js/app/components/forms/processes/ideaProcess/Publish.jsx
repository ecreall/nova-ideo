/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';

import { publish } from '../../../../graphql/processes/ideaProcess';
import { publishMutation } from '../../../../graphql/processes/ideaProcess/publish';
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

export class Dumbpublish extends React.Component {
  form = null;

  handleSubmit = () => {
    const { idea } = this.props;
    this.closeForm();
    this.props.publishIdea({
      context: idea
    });
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const { action, idea, onClose, classes, theme } = this.props;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        appBar={I18n.t(action.description)}
        onClose={onClose}
        footer={[
          <CancelButton onClick={this.closeForm}>
            {I18n.t('forms.cancel')}
          </CancelButton>,
          <Button onClick={this.handleSubmit} background={theme.palette.success[500]} className={classes.button}>
            {I18n.t(action.submission)}
          </Button>
        ]}
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
  graphql(publishMutation, {
    props: function (props) {
      return {
        publishIdea: publish(props)
      };
    }
  })(Dumbpublish)
);