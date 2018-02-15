/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { Translate } from 'react-redux-i18n';

import { goTo, get } from '../../utils/routeMap';
import { PROCESSES } from '../../constants';
import { select, deselect } from '../../graphql/processes/abstractProcess';
import { selectMutation } from '../../graphql/processes/abstractProcess/select';
import { deselectMutation } from '../../graphql/processes/abstractProcess/deselect';

export class DumbUserActionsManager extends React.Component {
  onActionPerformed = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
  };

  performAction = (action) => {
    const { person, network, globalProps } = this.props;
    const userProcessNodes = PROCESSES.usermanagement.nodes;
    if (action.nodeId === userProcessNodes.discuss.nodeId) {
      this.onActionPerformed();
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
        selectUser({ context: person }).then(this.onActionPerformed).catch(globalProps.showError);
        break;
      case processNodes.deselect.nodeId:
        deselectUser({ context: person }).then(this.onActionPerformed).catch(globalProps.showError);
        break;
      default:
        globalProps.showMessage(<Translate value="comingSoon" />);
      }
    }
  };

  render() {
    const children = React.Children.map(this.props.children, (child) => {
      return React.cloneElement(child, {
        actionsManager: this
      });
    });
    return children;
  }
}

const DumbUserActions = graphql(selectMutation, {
  props: function (props) {
    return {
      selectUser: select(props)
    };
  }
})(
  graphql(deselectMutation, {
    props: function (props) {
      return {
        deselectUser: deselect(props)
      };
    }
  })(DumbUserActionsManager)
);

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    network: state.network
  };
};

export default connect(mapStateToProps, null, null, { withRef: true })(DumbUserActions);