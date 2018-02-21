/* eslint-disable react/no-array-index-key, no-undef */
import React from 'react';

import Delete from '../forms/processes/commentProcess/Delete';
import Pin from '../forms/processes/commentProcess/Pin';
import Unpin from '../forms/processes/commentProcess/Unpin';
import { PROCESSES } from '../../processes';

export class DumbCommentProcessManager extends React.Component {
  state = {
    action: null
  };

  onActionPerformed = () => {
    const { onActionClick } = this.props;
    if (onActionClick) onActionClick();
  };

  performAction = (action) => {
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    switch (action.behaviorId) {
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
    const { comment } = this.props;
    if (!action) return null;
    const commentProcessNodes = PROCESSES.commentmanagement.nodes;
    switch (action.behaviorId) {
    case commentProcessNodes.delete.nodeId:
      return <Delete comment={comment} action={action} onClose={this.onFormClose} />;
    case commentProcessNodes.pin.nodeId:
      return <Pin comment={comment} action={action} onClose={this.onFormClose} />;
    case commentProcessNodes.unpin.nodeId:
      return <Unpin comment={comment} action={action} onClose={this.onFormClose} />;
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

export default DumbCommentProcessManager;