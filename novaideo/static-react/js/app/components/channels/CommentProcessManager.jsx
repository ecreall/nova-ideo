/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';
import { connect } from 'react-redux';

import Delete from '../forms/processes/commentProcess/Delete';
import Pin from '../forms/processes/commentProcess/Pin';
import Unpin from '../forms/processes/commentProcess/Unpin';
import { updateApp } from '../../actions/actions';
import { PROCESSES } from '../../processes';
import { CONTENTS_IDS } from './chatAppRight';

export class DumbCommentProcessManager extends React.Component {
  state = {
    action: null
  };

  openRight = (id, props) => {
    this.props.updateApp('chatApp', { right: { open: true, componentId: id, props: props } });
  };

  onActionPerformed = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
  };

  performAction = (action) => {
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    const { comment } = this.props;
    switch (action.behaviorId) {
    case commentProcessNodes.respond.nodeId:
      this.openRight(CONTENTS_IDS.reply, { id: comment.id });
      break;
    case commentProcessNodes.delete.nodeId:
      this.displayForm(action);
      break;
    default:
      this.displayForm(action);
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
  updateApp: updateApp
};

export default connect(null, mapDispatchToProps)(DumbCommentProcessManager);