/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { withApollo, graphql } from 'react-apollo';
import { Translate, I18n } from 'react-redux-i18n';

import { goTo, get } from '../../utils/routeMap';
import { ACTIONS, PROCESSES } from '../../processes';
import { select, deselect } from '../../graphql/processes/abstractProcess';
import Select from '../../graphql/processes/abstractProcess/mutations/Select.graphql';
import Deselect from '../../graphql/processes/abstractProcess/mutations/Deselect.graphql';
import Login from '../forms/processes/userProcess/Login';
import Paramters from '../forms/processes/userProcess/Paramters';
import { userLogout } from '../../actions/authActions';
import { filterActions } from '../../utils/processes';

export class DumbUserProcessManager extends React.Component {
  state = {
    action: null
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

  execute = (action) => {
    const { person, network, globalProps } = this.props;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    if (action.nodeId === userProcessNodes.discuss.nodeId) {
      this.onActionExecuted();
      setTimeout(() => {
        goTo(get('messages', { channelId: person.channel.id }, { right: 'info' }));
      }, 200);
    } else if (!network.isLogged) {
      const {
        globalProps: { rootActions }
      } = this.props;
      const loginAction = filterActions(rootActions, {
        tags: [ACTIONS.mainMenu, ACTIONS.site],
        behaviorId: userProcessNodes.login.nodeId
      })[0];
      const processNodes = PROCESSES.novaideoabstractprocess.nodes;
      switch (action.behaviorId) {
      case processNodes.selectAnonymous.behaviorId:
        this.displayForm(loginAction);
        break;
      default:
        this.displayForm(loginAction);
      }
    } else {
      const { selectUser, deselectUser } = this.props;
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
      case userProcessNodes.edit.nodeId:
        this.displayForm(action);
        break;
      case userProcessNodes.logout.nodeId:
        this.props
          .userLogout()
          .then(({ value }) => {
            if (value.status) {
              this.props.client.resetStore();
            }
          })
          .catch(() => {
            return null;
          });
        break;
      default:
        globalProps.showMessage(<Translate value="comingSoon" />);
      }
    }
  };
  onFormClose = () => {
    this.setState({ action: null });
    this.afterFormClosed();
  };

  displayForm = (action) => {
    this.beforeFormOpened();
    this.setState({ action: action });
  };

  renderForm = () => {
    const { action } = this.state;
    const { person } = this.props;
    if (!action) return null;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    switch (action.behaviorId) {
    case userProcessNodes.login.nodeId:
      return <Login action={action} onClose={this.onFormClose} messageType="warning" message={I18n.t('common.needLogin')} />;
    case userProcessNodes.edit.nodeId:
      return <Paramters onClose={this.onFormClose} account={person} />;
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
  userLogout: userLogout
};

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    network: state.network
  };
};

export default withApollo(
  connect(
    mapStateToProps,
    mapDispatchToProps,
    null,
    { withRef: true }
  )(UserProcessManagerWithActions)
);