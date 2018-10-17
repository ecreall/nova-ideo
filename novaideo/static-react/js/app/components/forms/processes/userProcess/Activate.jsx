/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import { activate } from '../../../../graphql/processes/userProcess';
import Activate from '../../../../graphql/processes/userProcess/mutations/Activate.graphql';
import Button, { CancelButton } from '../../../styledComponents/Button';
import Form from '../../Form';

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

export class DumbActivate extends React.Component {
  form = null;

  handleSubmit = () => {
    const { account } = this.props;
    this.closeForm();
    this.props.activate({
      context: account
    });
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const {
      action, onClose, classes, theme
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
      </Form>
    );
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(Activate, {
    props: function (props) {
      return {
        activate: activate(props)
      };
    }
  })(DumbActivate)
);