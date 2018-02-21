/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import { I18n } from 'react-redux-i18n';

import { pinComment } from '../../../../graphql/processes/commentProcess';
import { pinMutation } from '../../../../graphql/processes/commentProcess/pin';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';
import { CommentItem } from '../../../channels/CommentItem';

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

export class DumbPin extends React.Component {
  componentWillReceiveProps(nextProps) {
    const comment = this.props.comment;
    const nextComment = nextProps.comment;
    if (comment.id === nextComment.id && this.form) this.form.open();
  }

  form = null;

  handleSubmit = () => {
    const { comment } = this.props;
    this.props
      .pinComment({
        context: comment
      })
      .then(this.closeForm);
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const { action, comment, classes, theme, onFormClose } = this.props;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        appBar={I18n.t(action.description)}
        onClose={onFormClose}
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
          <CommentItem node={comment} />
        </div>
      </Form>
    );
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(pinMutation, {
    props: function (props) {
      return {
        pinComment: pinComment(props)
      };
    }
  })(DumbPin)
);