/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';
import { graphql } from 'react-apollo';

import Delete from '../forms/processes/commentProcess/Delete';
import Pin from '../forms/processes/commentProcess/Pin';
import Unpin from '../forms/processes/commentProcess/Unpin';
import { addReactionMutation } from '../../graphql/processes/abstractProcess/addReaction';
import { addReaction } from '../../graphql/processes/abstractProcess';
import { updateChatAppRight } from '../../actions/actions';
import { PROCESSES } from '../../processes';
import { CONTENTS_IDS } from './chatAppRight';

export class DumbCommentProcessManager extends React.Component {
  state = {
    action: null
  };

  openRight = (id, props) => {
    this.props.updateChatAppRight({ open: true, componentId: id, props: props });
  };

  onActionPerformed = () => {
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
    this.onActionPerformed();
  };

  performAction = (action, data) => {
    const abstractProcessNodes = PROCESSES.novaideoabstractprocess.nodes;
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    const { comment, account, addReactionComment, channel } = this.props;
    switch (action.behaviorId) {
    case commentProcessNodes.respond.nodeId:
      this.openRight(CONTENTS_IDS.reply, { id: comment.id, channelTitle: channel.title, channelId: channel.id });
      break;
    case commentProcessNodes.delete.nodeId:
      this.displayForm(action);
      break;
    case abstractProcessNodes.addreaction.nodeId:
      addReactionComment({
        context: comment,
        emoji: data.emoji,
        user: account
      }).then(this.onActionPerformed);
      break;
    default:
      this.displayForm(action);
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
    if (!action) return null;
    const { comment, channel } = this.props;
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    switch (action.behaviorId) {
    case commentProcessNodes.delete.nodeId:
      return <Delete comment={comment} channel={channel} action={action} onClose={this.onFormClose} />;
    case commentProcessNodes.pin.nodeId:
      return <Pin comment={comment} channel={channel} action={action} onClose={this.onFormClose} />;
    case commentProcessNodes.unpin.nodeId:
      return <Unpin comment={comment} channel={channel} action={action} onClose={this.onFormClose} />;
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

export const mapDispatchToProps = {
  updateChatAppRight: updateChatAppRight
};

export const mapStateToProps = (state) => {
  return {
    account: state.globalProps.account
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(
  graphql(addReactionMutation, {
    props: function (props) {
      return {
        addReactionComment: addReaction(props)
      };
    }
  })(DumbCommentProcessManager)
);