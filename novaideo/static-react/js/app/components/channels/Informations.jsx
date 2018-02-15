/* eslint-disable no-underscore-dangle */
import React from 'react';
import Idea from '../idea/IdeaPopover';
import User from '../user/UserPopover';

export class DumbInformations extends React.Component {
  render() {
    const { subject, onActionClick, channel } = this.props;
    switch (channel.subject.__typename) {
    case 'Idea':
      return <Idea id={subject} onActionClick={onActionClick} />;
    case 'Person':
      return <User id={subject} onActionClick={onActionClick} />;
    default:
      return null;
    }
  }
}

export default DumbInformations;