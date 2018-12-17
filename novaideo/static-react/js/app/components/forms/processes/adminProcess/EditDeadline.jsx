/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import { graphql } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';
import DatePicker from 'react-datepicker';
import Moment from 'moment';

import { editDeadline } from '../../../../graphql/processes/adminProcess';
import EditDeadline from '../../../../graphql/processes/adminProcess/mutations/EditDeadline.graphql';
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
  },
  formContainer: {
    display: 'flex',
    justifyContent: 'center'
  }
};

export class DumbEditDeadline extends React.Component {
  state = { date: this.props.date };

  form = null;

  handleChange = (date) => {
    this.setState({ date: date });
  };

  handleSubmit = () => {
    const { root } = this.props;
    const { date } = this.state;
    this.closeForm();
    this.props.editDeadline({
      context: root,
      date: date
    });
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const {
      action, onClose, classes, theme
    } = this.props;
    const { date } = this.state;
    const now = Moment();
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
              {I18n.t('forms.edit')}
            </Button>
          </React.Fragment>
        )}
        classes={{ container: classes.formContainer }}
      >
        <DatePicker
          showDisabledMonthNavigation
          inline
          showTimeSelect
          onChange={this.handleChange}
          selected={date}
          minDate={now}
          timeFormat="HH:mm"
          timeIntervals={10}
          dateFormat="MMMM d, yyyy h:mm aa"
          locale="fr"
        />
      </Form>
    );
  }
}

export default withStyles(styles, { withTheme: true })(
  graphql(EditDeadline, {
    props: function (props) {
      return {
        editDeadline: editDeadline(props)
      };
    }
  })(DumbEditDeadline)
);