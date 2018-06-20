/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { connect } from 'react-redux';
import { I18n } from 'react-redux-i18n';
import { withStyles } from '@material-ui/core/styles';

import Login from '../forms/processes/userProcess/Login';
import { filterActions } from '../../utils/processes';
import { ACTIONS, PROCESSES } from '../../processes';
import CreateIdeaForm from '../forms/processes/ideaProcess/Create';
import UserAvatar from '../user/UserAvatar';
import { getFormId } from '../../utils/globalFunctions';

const styles = {
  fromContainer: {
    padding: '15px 11px',
    backgroundColor: 'whitesmoke',
    border: 'solid 1px rgba(0,0,0,.1)',
    borderBottom: 'none',
    display: 'flex'
  },
  inputContainer: {
    display: 'flex',
    justifyContent: 'center',
    height: 'auto',
    outline: 0,
    border: '1px solid #a0a0a2',
    borderRadius: 4,
    resize: 'none',
    color: '#2c2d30',
    fontSize: 15,
    lineHeight: '1.2rem',
    maxHeight: 'none',
    minHeight: 40,
    position: 'relative',
    backgroundColor: 'white',
    flex: 1,
    flexDirection: 'column',
    marginLeft: 15,
    paddingLeft: 10
  },
  placeholder: {
    color: '#000',
    opacity: '.375',
    textOverflow: 'ellipsis',
    overflow: 'hidden',
    whiteSpace: 'nowrap',
    fontStyle: 'normal',
    pointerEvents: 'none',
    maxHeight: '100%'
  },
  avatar: {
    borderRadius: 4,
    marginTop: 1
  }
};

export class DumbCreateIdeaHome extends React.Component {
  state = {
    open: false
  };

  openForm = () => {
    this.setState({ open: true });
  };

  closeForm = () => {
    this.setState({ open: false });
  };

  render() {
    const { rootActions, account, classes } = this.props;
    const { open } = this.state;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const loginAction = filterActions(rootActions, {
      tags: [ACTIONS.mainMenu, ACTIONS.site],
      behaviorId: userProcessNodes.login.nodeId
    })[0];
    const authorPicture = account && account.picture;
    const authorTitle = account && account.title;
    const form = account ? (
      <CreateIdeaForm onClose={this.closeForm} key="create-proposal-form" form={getFormId('create-proposal-form')} />
    ) : (
      <Login action={loginAction} onClose={this.closeForm} messageType="warning" message={I18n.t('common.needLogin')} />
    );
    return [
      <div className={classes.fromContainer}>
        <div className={classes.left}>
          <UserAvatar
            isAnonymous={!account}
            anonymousIcon="account"
            picture={authorPicture}
            title={authorTitle}
            classes={{ avatar: classes.avatar }}
          />
        </div>
        <div className={classes.inputContainer} onClick={this.openForm}>
          <div className={classes.placeholder}>{I18n.t('forms.idea.textPlaceholder')}</div>
        </div>
      </div>,
      open ? form : null
    ];
  }
}

const mapStateToProps = (state) => {
  return {
    account: state.globalProps.account,
    rootActions: state.globalProps.rootActions
  };
};

export default withStyles(styles)(connect(mapStateToProps)(DumbCreateIdeaHome));