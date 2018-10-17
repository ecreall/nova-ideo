/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import { deleteComment } from '../../../../graphql/processes/commentProcess';
import Delete from '../../../../graphql/processes/commentProcess/mutations/Delete.graphql';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';
import { StyledCommentItem } from '../../../chatApp/CommentItem';

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

export class DumbDelete extends React.Component {
  form = null;

  handleSubmit = () => {
    const { comment, channel } = this.props;
    this.props.deleteComment({
      context: comment,
      channel: channel
    });
    this.closeForm();
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const {
      action, comment, classes, theme, onClose
    } = this.props;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        appBar={I18n.t(action.description)}
        onClose={onClose}
        footer={[
          <CancelButton onClick={this.closeForm}>{I18n.t('forms.cancel')}</CancelButton>,
          <Button onClick={this.handleSubmit} background={theme.palette.danger.primary} className={classes.button}>
            {I18n.t(action.submission)}
          </Button>
        ]}
      >
        {I18n.t(action.confirmation)}
        <div className={classes.contextContainer}>
          <StyledCommentItem node={comment} disableReply />
        </div>
      </Form>
    );
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(Delete, {
    props: function (props) {
      return {
        deleteComment: deleteComment(props)
      };
    }
  })(DumbDelete)
);