/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Field, reduxForm, initialize } from 'redux-form';
import { connect } from 'react-redux';
import { I18n, Translate } from 'react-redux-i18n';
import { withStyles } from 'material-ui/styles';
import Zoom from 'material-ui/transitions/Zoom';
import Avatar from 'material-ui/Avatar';
import { withApollo } from 'react-apollo';
import { CircularProgress } from 'material-ui/Progress';

import { renderTextInput } from '../../utils';
import Alert from '../../../common/Alert';
import { DEFAULT_LOGO } from '../../../../constants';
import Button from '../../../styledComponents/Button';
import Form from '../../Form';
import { asyncValidateLogin } from '../../../../utils/user';
import { userLogin, updateUserToken } from '../../../../actions/authActions';

const styles = (theme) => {
  return {
    maxContainer: {
      padding: 5,
      paddingTop: 35,
      maxWidth: 600
    },
    form: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 6,
      border: '1px solid #e8e8e8',
      background: 'white',
      boxShadow: '0 1px 1px rgba(0, 0, 0, 0.15)',
      padding: 32
    },
    formContainer: {
      maxWidth: 400,
      width: '100%'
    },
    siteTitle: {
      fontSize: 32,
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: 35,
      color: '#2c2d30',
      letterSpacing: -1
    },
    description: {
      fontSize: 16,
      marginBottom: 20,
      color: '#2c2d30'
    },
    paper: {
      backgroundColor: '#fafafa'
    },
    sectionHeaderTitle: {
      display: 'flex',
      position: 'relative',
      justifyContent: 'center'
    },
    sectionHeaderAddon: {
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      textDecoration: 'none',
      color: '#a0a0a2',
      fontWeight: 500,
      fontSize: 15
    },
    appBarHeaderTitle: {
      display: 'flex',
      position: 'relative',
      justifyContent: 'center',
      alignItems: 'center'
    },
    appBarHeaderTitleText: {
      color: '#2c2d30',
      fontSize: 18,
      fontWeight: 900,
      marginLeft: 7
    },
    avatar: {
      width: 36,
      height: 36,
      borderRadius: 4
    },
    button: {
      height: 40,
      width: 40,
      color: theme.palette.primary[500]
    },
    buttonFooter: {
      width: '100%',
      minHeight: 45
    },
    titleRoot: {
      height: 45
    },
    formTitle: {
      flexGrow: 1
    },
    header: {
      display: 'flex',
      flexDirection: 'column',
      margin: '0 10px',
      position: 'relative'
    },
    headerTitle: {
      fontSize: 15,
      color: '#2c2d30',
      fontWeight: 900,
      display: 'flex',
      lineHeight: 'normal'
    },
    titleContainer: {
      display: 'flex'
    },
    closeBtn: {
      '&::after': {
        display: 'block',
        position: 'absolute',
        top: '50%',
        right: 'auto',
        bottom: 'auto',
        left: -4,
        height: 20,
        transform: 'translateY(-50%)',
        borderRadius: 0,
        borderRight: '1px solid #e5e5e5',
        content: '""',
        color: '#2c2d30'
      }
    },
    loading: {
      display: 'flex',
      justifyContent: 'center'
    },
    alertContainer: {
      marginBottom: 20
    }
  };
};

export class DumbLoginForm extends React.Component {
  state = {
    loading: false
  };
  form = null;

  closeForm = () => {
    this.form.close();
  };

  handleSubmit = () => {
    const { formData, valid } = this.props;
    // context if transformation (transform a comment in to idea)
    if (valid) {
      this.setState({ loading: true }, () => {
        this.props
          .userLogin(formData.values.login, formData.values.password)
          .then(({ value }) => {
            // update the user token (see the history reducer)
            // this.props.updateUserToken(value.token);
            if (value.status) {
              this.setState({ loading: false }, () => {
                this.props.client.resetStore();
                this.initializeForm();
              });
            } else {
              this.setState({ loading: false, error: true });
            }
          })
          .catch(() => {
            this.setState({ loading: false });
          });
      });
    }
  };

  initializeForm = () => {
    const { form, context } = this.props;
    this.props.dispatch(
      initialize(
        form,
        !context
          ? {
            login: '',
            password: ''
          }
          : undefined
      )
    );
    this.closeForm();
  };

  render() {
    const { action, message, messageType, globalProps: { site }, onClose, classes, theme } = this.props;
    const { loading, error } = this.state;
    const picture = site && site.logo;
    return (
      <Form
        initRef={(form) => {
          this.form = form;
        }}
        open
        fullScreen
        transition={Zoom}
        onClose={onClose}
        appBar={
          <div className={classes.appBarHeaderTitle}>
            <Avatar className={classes.avatar} src={picture ? `${picture.url}/profil` : DEFAULT_LOGO} />
            <div className={classes.appBarHeaderTitleText}>
              {site && site.title}
            </div>
          </div>
        }
        classes={{
          closeBtn: classes.closeBtn,
          maxContainer: classes.maxContainer,
          paper: classes.paper
        }}
      >
        {error &&
          <Alert type="danger" classes={{ container: classes.alertContainer }}>
            {I18n.t('common.failedLogin')}
          </Alert>}
        {message &&
          <Alert type={messageType} classes={{ container: classes.alertContainer }}>
            {message}
          </Alert>}
        <div className={classes.form}>
          <div className={classes.formContainer}>
            <div className={classes.formTitle}>
              <div className={classes.siteTitle}>
                <div>
                  <Translate value={action.title} siteTitle={site.title} />
                </div>
                <div className={classes.sectionHeaderTitle}>
                  <div className={classes.sectionHeaderAddon}>
                    {window.location.host}
                  </div>
                </div>
              </div>
              <div className={classes.description}>
                Enter your <strong>identifier</strong> and <strong>password</strong>
              </div>
            </div>
            <Field
              props={{
                placeholder: 'votre.email@test.com',
                classes: {
                  root: classes.titleRoot
                },
                autoFocus: true
              }}
              name="login"
              component={renderTextInput}
              onChange={() => {}}
            />
            <Field
              props={{
                placeholder: 'password',
                type: 'password',
                autoComplete: 'current-password',
                classes: {
                  root: classes.titleRoot
                }
              }}
              name="password"
              component={renderTextInput}
              onChange={() => {}}
            />
            {loading
              ? <div className={classes.loading}>
                <CircularProgress size={30} style={{ color: theme.palette.success[500] }} />
              </div>
              : <Button onClick={this.handleSubmit} background={theme.palette.success[500]} className={classes.buttonFooter}>
                {I18n.t('common.signIn')}
              </Button>}
          </div>
        </div>
      </Form>
    );
  }
}

const validate = (values) => {
  const errors = {};
  if (!values.login) {
    errors.login = 'Required';
  }
  if (!values.password) {
    errors.password = 'Required';
  }
  return errors;
};

const asyncValidate = (values /* , dispatch */) => {
  return asyncValidateLogin(values.login).then((value) => {
    // simulate server latency
    if (!value.status) {
      throw { login: 'That login is not valid' };
    }
  });
};

// Decorate the form component
const LoginReduxForm = reduxForm({
  destroyOnUnmount: false,
  validate: validate,
  asyncValidate: asyncValidate,
  asyncChangeFields: ['login'],
  touchOnChange: true
})(DumbLoginForm);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    globalProps: state.globalProps
  };
};

export const mapDispatchToProps = {
  userLogin: userLogin,
  updateUserToken: updateUserToken
};

export default withStyles(styles, { withTheme: true })(withApollo(connect(mapStateToProps, mapDispatchToProps)(LoginReduxForm)));