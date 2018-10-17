/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import { pinComment } from '../../../../graphql/processes/commentProcess';
import Pin from '../../../../graphql/processes/commentProcess/mutations/Pin.graphql';
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

export class DumbPin extends React.Component {
  form = null;

  handleSubmit = () => {
    const { comment, channel } = this.props;
    this.closeForm();
    this.props.pinComment({
      context: comment,
      channel: channel
    });
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const {
      action, comment, onClose, classes, theme
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
          <Button onClick={this.handleSubmit} background={theme.palette.success[500]} className={classes.button}>
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
  graphql(Pin, {
    props: function (props) {
      return {
        pinComment: pinComment(props)
      };
    }
  })(DumbPin)
);