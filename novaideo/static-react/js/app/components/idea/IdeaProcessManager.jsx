/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';
import { Translate } from 'react-redux-i18n';

import Delete from '../forms/processes/ideaProcess/Delete';
import { goTo, get } from '../../utils/routeMap';
import { PROCESSES } from '../../processes';
import { select, deselect } from '../../graphql/processes/abstractProcess';
import { selectMutation } from '../../graphql/processes/abstractProcess/select';
import { deselectMutation } from '../../graphql/processes/abstractProcess/deselect';
import { support, oppose, withdraw } from '../../graphql/processes/ideaProcess';
import { supportMutation } from '../../graphql/processes/ideaProcess/support';
import { opposeMutation } from '../../graphql/processes/ideaProcess/oppose';
import { withdrawMutation } from '../../graphql/processes/ideaProcess/withdraw';

export function getExaminationValue(idea) {
  if (idea.state.includes('favorable')) return 'bottom';
  if (idea.state.includes('to_study')) return 'middle';
  if (idea.state.includes('unfavorable')) return 'top';
  return undefined;
}

export function getEvaluationActions(idea) {
  const actions = PROCESSES.ideamanagement.nodes;
  const withdrawAction = actions.withdrawToken;
  const supportAction = idea.userToken === 'support' ? withdrawAction : actions.support;
  const opposeAction = idea.userToken === 'oppose' ? withdrawAction : actions.oppose;
  const result = {
    top: supportAction,
    down: opposeAction
  };
  return result;
}

export class DumbIdeaProcessManager extends React.Component {
  state = {
    action: null
  };

  onActionPerformed = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
  };

  evaluationClick = (action) => {
    const { idea, network, globalProps } = this.props;
    const processNodes = PROCESSES.ideamanagement.nodes;
    if (!network.isLogged) {
      globalProps.showMessage(<Translate value="LogInToPerformThisAction" />);
    } else if (!action) {
      globalProps.showMessage(<Translate value="AuthorizationFailed" />);
    } else {
      const { supportIdea, opposeIdea, withdrawIdea } = this.props;
      switch (action.nodeId) {
      case processNodes.withdrawToken.nodeId:
        withdrawIdea({
          context: idea,
          availableTokens: globalProps.account.availableTokens
        })
          .then(this.onActionPerformed)
          .catch(globalProps.showError);
        break;
      case processNodes.support.nodeId:
        if (globalProps.account.availableTokens || idea.userToken === 'oppose') {
          supportIdea({
            context: idea,
            availableTokens: globalProps.account.availableTokens
          })
            .then(this.onActionPerformed)
            .catch(globalProps.showError);
        } else {
          globalProps.showMessage(<Translate value="AuthorizationFailed" />);
        }
        break;
      case processNodes.oppose.nodeId:
        if (globalProps.account.availableTokens || idea.userToken === 'support') {
          opposeIdea({
            context: idea,
            availableTokens: globalProps.account.availableTokens
          })
            .then(this.onActionPerformed)
            .catch(globalProps.showError);
        } else {
          globalProps.showMessage(<Translate value="AuthorizationFailed" />);
        }
        break;
      default:
        globalProps.showMessage(<Translate value="comingSoon" />);
      }
    }
  };

  performAction = (action) => {
    const { idea, network, globalProps } = this.props;
    const ideaProcessNodes = PROCESSES.ideamanagement.nodes;
    if (action.nodeId === ideaProcessNodes.comment.nodeId) {
      this.onActionPerformed();
      setTimeout(() => {
        goTo(get('messages', { channelId: idea.channel.id }, { right: 'info' }));
      }, 200);
    } else if (!network.isLogged) {
      globalProps.showMessage(<Translate value="LogInToPerformThisAction" />);
    } else {
      const { selectIdea, deselectIdea } = this.props;
      const processNodes = PROCESSES.novaideoabstractprocess.nodes;

      switch (action.behaviorId) {
      case processNodes.select.nodeId:
        selectIdea({ context: idea }).then(this.onActionPerformed).catch(globalProps.showError);
        break;
      case processNodes.deselect.nodeId:
        deselectIdea({ context: idea }).then(this.onActionPerformed).catch(globalProps.showError);
        break;
      case ideaProcessNodes.delete.nodeId:
        this.displayForm(action);
        break;
      default:
        this.displayForm(action);
      }
    }
  };

  onFormClose = () => {
    this.setState({ action: null });
  };

  displayForm = (action) => {
    this.setState({ action: action });
  };

  renderForm = () => {
    const { action } = this.state;
    const { idea } = this.props;
    if (!action) return null;
    const ideaProcessNodes = PROCESSES.ideamanagement.nodes;
    switch (action.id) {
    case ideaProcessNodes.delete.nodeId:
      return <Delete idea={idea} action={action} onClose={this.onFormClose} />;
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

const IdeaProcessManagerWithActions = graphql(supportMutation, {
  props: function (props) {
    return {
      supportIdea: support(props)
    };
  }
})(
  graphql(opposeMutation, {
    props: function (props) {
      return {
        opposeIdea: oppose(props)
      };
    }
  })(
    graphql(withdrawMutation, {
      props: function (props) {
        return {
          withdrawIdea: withdraw(props)
        };
      }
    })(
      graphql(selectMutation, {
        props: function (props) {
          return {
            selectIdea: select(props)
          };
        }
      })(
        graphql(deselectMutation, {
          props: function (props) {
            return {
              deselectIdea: deselect(props)
            };
          }
        })(DumbIdeaProcessManager)
      )
    )
  )
);

export const mapStateToProps = (state) => {
  return {
    globalProps: state.globalProps,
    network: state.network
  };
};

export default connect(mapStateToProps, null, null, { withRef: true })(IdeaProcessManagerWithActions);