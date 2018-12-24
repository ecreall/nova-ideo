/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { withApollo, graphql } from 'react-apollo';
import { I18n } from 'react-redux-i18n';

import { goTo, get } from '../../utils/routeMap';
import { ACTIONS, PROCESSES } from '../../processes';
import { select, deselect } from '../../graphql/processes/abstractProcess';
import Select from '../../graphql/processes/abstractProcess/mutations/Select.graphql';
import Deselect from '../../graphql/processes/abstractProcess/mutations/Deselect.graphql';
import Login, { LOGIN_VIEWS } from '../forms/processes/userProcess/Login';
import EditPreferences from '../forms/processes/userProcess/Preferences';
import Activate from '../forms/processes/userProcess/Activate';
import Deactivate from '../forms/processes/userProcess/Deactivate';
import Paramters, { PARAMETERS_TABS } from '../forms/processes/userProcess/Paramters';
import { userLogout } from '../../actions/authActions';
import { filterActions } from '../../utils/processes';
import { openCollaborationRight } from '../../actions/collaborationAppActions';
import { CONTENTS_IDS } from '../collaborationApp/collaborationAppRight';
import { getFormId } from '../../utils/globalFunctions';

export class DumbUserProcessManager extends React.Component {
  state = {
    action: null,
    originalAction: null
  };

  onActionExecuted = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
  };

  beforeFormOpened = () => {
    const { onFormOpened } = this.props;
    if (onFormOpened) onFormOpened();
  };

  afterFormClosed = () => {
    const { onFormClosed } = this.props;
    if (onFormClosed) onFormClosed();
    // this.onActionExecuted();
  };

  openChannel = () => {
    const { chatAppIntegreted, person, openRight } = this.props;
    this.onActionExecuted();
    if (chatAppIntegreted) {
      openRight({
        componentId: CONTENTS_IDS.chat,
        props: { channel: person.channel.id, channelTitle: person.channel.title }
      });
    } else {
      setTimeout(() => {
        goTo(get('messages', { channelId: person.channel.id }, { right: 'info' }));
      }, 200);
    }
  };

  execute = (action) => {
    const { person, network, globalProps } = this.props;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const registrationNodes = PROCESSES.registrationmanagement.nodes;
    if (action.nodeId === userProcessNodes.discuss.nodeId) {
      this.openChannel();
    } else if (!network.isLogged) {
      const { globalProps: { rootActions } } = this.props;
      const loginAction = filterActions(rootActions, {
        tags: [ACTIONS.mainMenu, ACTIONS.site],
        behaviorId: userProcessNodes.login.nodeId
      })[0];
      switch (action.behaviorId) {
      case userProcessNodes.login.nodeId:
        this.displayForm(loginAction);
        break;
      case registrationNodes.registration.nodeId:
        this.displayForm(action);
        break;
      default:
        this.displayForm(loginAction, action);
      }
    } else {
      const { selectUser, deselectUser, client } = this.props;
      const processNodes = PROCESSES.novaideoabstractprocess.nodes;
      switch (action.behaviorId) {
      case processNodes.select.nodeId:
        selectUser({ context: person })
          .then(this.onActionExecuted)
          .catch(globalProps.showError);
        break;
      case processNodes.deselect.nodeId:
        deselectUser({ context: person })
          .then(this.onActionExecuted)
          .catch(globalProps.showError);
        break;
      case userProcessNodes.see.nodeId:
        this.onActionExecuted();
        setTimeout(() => {
          goTo(get('users', { userId: person.id }));
        }, 200);
        break;
      case userProcessNodes.logout.nodeId:
        this.props
          .userLogout()
          .then(({ value }) => {
            if (value.status) {
              client.resetStore();
            }
          })
          .catch(() => {
            return null;
          });
        break;
      default:
        this.displayForm(action);
      }
    }
  };

  onFormClose = () => {
    this.setState({ action: null });
    this.afterFormClosed();
  };

  displayForm = (action, originalAction) => {
    this.beforeFormOpened();
    this.setState({ action: action, originalAction: originalAction });
  };

  renderForm = () => {
    const { action, originalAction } = this.state;
    const { person, globalProps: { account } } = this.props;
    if (!action) return null;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    const registrationNodes = PROCESSES.registrationmanagement.nodes;
    switch (action.behaviorId) {
    case userProcessNodes.login.nodeId:
      return (
        <Login
          action={action}
          onClose={this.onFormClose}
          messageType="warning"
          message={originalAction && originalAction !== action && I18n.t('common.needLogin')}
        />
      );
    case registrationNodes.registration.nodeId:
      return <Login action={action} onClose={this.onFormClose} view={LOGIN_VIEWS.registration} />;
    case userProcessNodes.edit.nodeId:
      return <Paramters onClose={this.onFormClose} account={person} />;
    case userProcessNodes.assignRoles.nodeId:
      return <Paramters onClose={this.onFormClose} account={person} activeTab={PARAMETERS_TABS.assignRoles} />;
    case userProcessNodes.activate.nodeId:
      return <Activate onClose={this.onFormClose} account={person} action={action} />;
    case userProcessNodes.deactivate.nodeId:
      return <Deactivate onClose={this.onFormClose} account={person} action={action} />;
    case userProcessNodes.editPreferences.nodeId: {
      const formId = getFormId(`${person.id}-preferences`);
      return (
        <EditPreferences
          form={formId}
          key={formId}
          onClose={this.onFormClose}
          user={person}
          account={account}
          action={action}
        />
      );
    }
    default:
      return null;
    }
  };

  render() {
    const children = React.Children.map(this.props.children, (child) => {
      return React.cloneElement(child, {
        processManager: this
      });
    });
    return [children, this.renderForm()];
  }
}

const UserProcessManagerWithActions = graphql(Select, {
  props: function (props) {
    return {
      selectUser: select(props)
    };
  }
})(
  graphql(Deselect, {
    props: function (props) {
      return {
        deselectUser: deselect(props)
      };
    }
  })(DumbUserProcessManager)
);

export const mapDispatchToProps = {
  userLogout: userLogout,
  openRight: openCollaborationRight
};

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    network: state.network,
    chatAppIntegreted: state.apps.chatApp.integrations
  };
};

export default withApollo(connect(mapStateToProps, mapDispatchToProps, null, { withRef: true })(UserProcessManagerWithActions));