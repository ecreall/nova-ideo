/* eslint-disable react/no-array-index-key */
import React from 'react';
import Idea from '../idea/IdeaPopover';

export class DumbIdea extends React.Component {
  render() {
    const { subject, onActionClick } = this.props;
    return <Idea id={subject} onActionClick={onActionClick} />;
  }
}

export default DumbIdea;