import React from 'react';
import { graphql, withApollo } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import Dialog from '@material-ui/core/Dialog';
import { I18n } from 'react-redux-i18n';

import { goTo, get } from '../../../../utils/routeMap';
import { confirmRegistration } from '../../../../graphql/processes/userProcess';
import ConfirmRegistration from '../../../../graphql/processes/userProcess/mutations/ConfirmRegistration.graphql';
import { updateUserToken } from '../../../../actions/authActions';
import Illustration from '../../../common/Illustration';
import { REGISTRATION_CONFIRMATION } from '../../../../constants';

const styles = {
  message: {
    color: 'white',
    textAlign: 'center'
  },
  paper: {
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center'
  }
};

export class DumbConfirmRegistration extends React.Component {
  componentDidMount() {
    const { params: { registrationId } } = this.props;
    if (registrationId) {
      this.props
        .confirmRegistration({
          registration: registrationId
        })
        .then((result) => {
          const { data: { confirmRegistration: { status, token } } } = result;
          if (status && token) {
            this.props.updateUserToken(token);
            this.props.client.resetStore();
            goTo(get('root'));
          }
        });
    }
  }

  render() {
    const { classes } = this.props;
    return (
      <Dialog
        fullScreen
        open
        classes={{
          paper: classes.paper
        }}
      >
        <div className={classes.message}>
          <Illustration
            img={REGISTRATION_CONFIRMATION}
            message={<div className={classes.message}>{I18n.t('user.confirmRegistration')}</div>}
            classes={{
              container: classes.illustrationContainer,
              image: classes.imgIllustration
            }}
          />
          <CircularProgress size={50} style={{ color: 'white' }} />
        </div>
      </Dialog>
    );
  }
}

export const mapDispatchToProps = {
  updateUserToken: updateUserToken
};

export default withStyles(styles)(
  graphql(ConfirmRegistration, {
    props: function (props) {
      return {
        confirmRegistration: confirmRegistration(props)
      };
    }
  })(withApollo(connect(null, mapDispatchToProps)(DumbConfirmRegistration)))
);