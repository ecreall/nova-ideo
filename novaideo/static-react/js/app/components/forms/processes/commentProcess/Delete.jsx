/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';

import { deleteComment } from '../../../../graphql/processes/commentProcess';
import { deleteMutation } from '../../../../graphql/processes/commentProcess/delete';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';

const styles = {
  container: {
    padding: '15px 11px',
    borderBottom: 'none',
    display: 'flex'
  },
  form: {
    flex: 1,
    marginLeft: 10
  },
  button: {
    marginLeft: '5px !important'
  }
};

export class DumbDelete extends React.Component {
  componentWillReceiveProps() {
    if (this.form) this.form.open();
  }

  form = null;

  handleSubmit = () => {
    const { comment } = this.props;
    this.props.deleteComment({
      context: comment
    });
    this.closeForm();
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const { action, classes, theme, onFormClose } = this.props;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        appBar={action.description}
        onClose={onFormClose}
        footer={[
          <CancelButton onClick={this.closeForm}>
            {I18n.t('forms.cancel')}
          </CancelButton>,
          <Button onClick={this.handleSubmit} background={theme.palette.danger.primary} className={classes.button}>
            {action.title}
          </Button>
        ]}
      >
        <div className={classes.container}>
          <div className={classes.form}>
            {I18n.t('forms.removeComment')}
          </div>
        </div>
      </Form>
    );
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(deleteMutation, {
    props: function (props) {
      return {
        deleteComment: deleteComment(props)
      };
    }
  })(DumbDelete)
);