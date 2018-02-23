/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';

import { goTo, get } from '../../../../utils/routeMap';
import { deleteIdea } from '../../../../graphql/processes/ideaProcess';
import { deleteMutation } from '../../../../graphql/processes/ideaProcess/delete';
import { closeChatApp } from '../../../../actions/actions';
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
    paddingTop: 8,
    paddingBottom: 8,
    paddingRight: 8
  }
};

export class DumbDelete extends React.Component {
  form = null;

  handleSubmit = () => {
    const { idea, previousLocation } = this.props;
    this.props
      .deleteIdea({
        context: idea
      })
      .then(() => {
        this.props.closeChatApp();
        goTo(previousLocation || get('root'));
      });
    this.closeForm();
  };

  closeForm = () => {
    this.form.close();
  };

  render() {
    const { action, classes, theme, onClose } = this.props;
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
          <Button onClick={this.handleSubmit} background={theme.palette.danger.primary} className={classes.button}>
            {I18n.t(action.submission)}
          </Button>
        ]}
      >
        {I18n.t(action.confirmation)}
      </Form>
    );
  }
}

export const mapDispatchToProps = {
  closeChatApp: closeChatApp
};

export const mapStateToProps = (state) => {
  return {
    previousLocation: state.history.navigation.previous
  };
};

export default withStyles(styles, { withTheme: true })(
  connect(mapStateToProps, mapDispatchToProps)(
    graphql(deleteMutation, {
      props: function (props) {
        return {
          deleteIdea: deleteIdea(props)
        };
      }
    })(DumbDelete)
  )
);