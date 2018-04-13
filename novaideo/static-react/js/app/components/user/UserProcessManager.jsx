/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { Translate } from 'react-redux-i18n';

import { goTo, get } from '../../utils/routeMap';
import { PROCESSES } from '../../processes';
import { select, deselect } from '../../graphql/processes/abstractProcess';
import Select from '../../graphql/processes/abstractProcess/mutations/Select.graphql';
import Deselect from '../../graphql/processes/abstractProcess/mutations/Deselect.graphql';

export class DumbUserProcessManager extends React.Component {
  onActionExecuted = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
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
      globalProps.showMessage(<Translate value="LogInToPerformThisAction" />);
    } else {
      const { selectUser, deselectUser } = this.props;
      const processNodes = PROCESSES.novaideoabstractprocess.nodes;
      switch (action.behaviorId) {
      case processNodes.select.nodeId:
        selectUser({ context: person }).then(this.onActionExecuted).catch(globalProps.showError);
        break;
      case processNodes.deselect.nodeId:
        deselectUser({ context: person }).then(this.onActionExecuted).catch(globalProps.showError);
        break;
      default:
        globalProps.showMessage(<Translate value="comingSoon" />);
      }
    }
  };

  render() {
    const children = React.Children.map(this.props.children, (child) => {
      return React.cloneElement(child, {
        processManager: this
      });
    });
    return children;
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

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    network: state.network
  };
};

export default connect(mapStateToProps, null, null, { withRef: true })(UserProcessManagerWithActions);