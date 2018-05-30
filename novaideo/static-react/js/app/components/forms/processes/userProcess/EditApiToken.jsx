/* eslint-disable react/no-array-index-key, no-confusing-arrow, no-throw-literal */
import React from 'react';
import { connect } from 'react-redux';
import { I18n, Translate } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';
import { graphql } from 'react-apollo';
import CircularProgress from '@material-ui/core/CircularProgress';

import Button from '../../../styledComponents/Button';
import { registration } from '../../../../graphql/processes/userProcess';
import Registration from '../../../../graphql/processes/userProcess/mutations/Registration.graphql';

const styles = {
  buttonFooter: {
    width: '50%',
    minHeight: 45,
    fontSize: 18,
    fontWeight: 900,
    marginTop: 15,
    float: 'right'
  },
  loading: {
    display: 'flex',
    justifyContent: 'center'
  }
};

export class DumbEditApiToken extends React.Component {
  state = {
    loading: false
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { formData, valid } = this.props;
    if (valid) {
      this.setState({ loading: true }, () => {
        this.props
          .registration({
            firstName: formData.values.firstName,
            lastName: formData.values.lastName,
            email: formData.values.email,
            password: formData.values.password
          })
          .then(() => {
            this.setState({ loading: false }, this.initializeForm);
          });
      });
    }
  };

  render() {
    const { action, user, classes, theme } = this.props;
    const { loading } = this.state;
    return (
      <div>
        {user.token}
        {loading
          ? <div className={classes.loading}>
            <CircularProgress size={30} style={{ color: theme.palette.success[800] }} />
          </div>
          : <Button type="submit" background={theme.palette.success[800]} className={classes.buttonFooter}>
              Demander un nouveau jeton d'API
          </Button>}
      </div>
    );
  }
}

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps,
    user: state.user
  };
};

const EditApiTokenReduxFormWithMutation = graphql(Registration, {
  props: function (props) {
    return {
      registration: registration(props)
    };
  }
})(DumbEditApiToken);

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(EditApiTokenReduxFormWithMutation));